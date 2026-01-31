"""
Advanced SEO Audit Tool - Streamlit Web App (300+ Parameters)
Author: Muntasir Islam
Version: 3.0
Deployed on: Streamlit Cloud
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import json
import re
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Tuple
import time
from collections import Counter
import pandas as pd

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="SEO Audit Tool - 300+ Checks | Free Online SEO Analyzer",
    page_icon="https://api.iconify.design/carbon/search-advanced.svg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/muntasir-islam/seo_audit_tool',
        'Report a bug': 'https://github.com/muntasir-islam/seo_audit_tool/issues',
        'About': '### Advanced SEO Audit Tool\n\n**300+ SEO parameters analyzed**\n\nCreated by Muntasir Islam'
    }
)

# Font Awesome CDN and Custom CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* Base styling */
    * { font-family: 'Inter', sans-serif; }
    
    .main { 
        background: linear-gradient(180deg, #0a0a0f 0%, #12121a 50%, #0a0a0f 100%);
    }
    .stApp { 
        background: linear-gradient(180deg, #0a0a0f 0%, #12121a 50%, #0a0a0f 100%);
    }
    
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 24px;
        padding: 40px;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    /* Score card styling */
    .score-card-container {
        background: linear-gradient(145deg, #1a1a2e 0%, #16162a 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    .score-card-container::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.5), transparent);
    }
    
    .score-ring {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 25px;
        flex-direction: column;
        position: relative;
        background: rgba(0,0,0,0.4);
    }
    .score-ring::before {
        content: '';
        position: absolute;
        inset: -4px;
        border-radius: 50%;
        padding: 4px;
        background: conic-gradient(from 0deg, var(--score-color) calc(var(--score-percent) * 3.6deg), rgba(255,255,255,0.1) 0);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
    }
    
    /* Stats cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 20px 0;
    }
    .stat-card {
        background: linear-gradient(145deg, #1e1e32 0%, #16162a 100%);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.1);
    }
    .stat-card .stat-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-card .stat-label {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stat-card.passed .stat-value { background: linear-gradient(135deg, #22c55e 0%, #4ade80 100%); -webkit-background-clip: text; }
    .stat-card.warning .stat-value { background: linear-gradient(135deg, #eab308 0%, #fbbf24 100%); -webkit-background-clip: text; }
    .stat-card.critical .stat-value { background: linear-gradient(135deg, #ef4444 0%, #f87171 100%); -webkit-background-clip: text; }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 30px 0 20px 0;
        color: #f1f5f9;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .section-header i {
        color: #6366f1;
        font-size: 1.1rem;
        width: 20px;
        text-align: center;
    }
    
    /* Info cards */
    .info-card {
        background: linear-gradient(145deg, #1e1e32 0%, #16162a 100%);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
    }
    .info-card-header {
        font-size: 0.9rem;
        font-weight: 600;
        color: #94a3b8;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Issue cards */
    .issue-critical {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 4px solid #ef4444;
        padding: 16px 20px;
        margin: 10px 0;
        border-radius: 12px;
        color: #fca5a5;
    }
    .issue-warning {
        background: linear-gradient(135deg, rgba(234, 179, 8, 0.15) 0%, rgba(234, 179, 8, 0.05) 100%);
        border: 1px solid rgba(234, 179, 8, 0.3);
        border-left: 4px solid #eab308;
        padding: 16px 20px;
        margin: 10px 0;
        border-radius: 12px;
        color: #fde047;
    }
    .issue-recommendation {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(59, 130, 246, 0.05) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-left: 4px solid #3b82f6;
        padding: 16px 20px;
        margin: 10px 0;
        border-radius: 12px;
        color: #93c5fd;
    }
    .issue-passed {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-left: 4px solid #22c55e;
        padding: 16px 20px;
        margin: 10px 0;
        border-radius: 12px;
        color: #86efac;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 16px 32px;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 12px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        color: #f1f5f9;
        padding: 14px 16px;
        font-size: 1rem;
    }
    .stTextInput>div>div>input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 30, 50, 0.5);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f1f5f9 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 500;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 30, 50, 0.5);
        border-radius: 10px;
        color: #e2e8f0;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #e2e8f0;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        border-color: #6366f1;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121a 0%, #0a0a0f 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent);
        margin: 30px 0;
    }
    
    /* Footer */
    .footer-container {
        background: linear-gradient(135deg, rgba(30, 30, 50, 0.5) 0%, rgba(20, 20, 40, 0.5) 100%);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 30px;
        margin-top: 40px;
        text-align: center;
    }
    .footer-links a {
        color: #94a3b8;
        text-decoration: none;
        margin: 0 15px;
        transition: color 0.3s ease;
    }
    .footer-links a:hover {
        color: #6366f1;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Status indicators */
    .status-pass { color: #22c55e; }
    .status-fail { color: #ef4444; }
    .status-warn { color: #eab308; }
    
    /* Glow effects */
    .glow-green { text-shadow: 0 0 20px rgba(34, 197, 94, 0.5); }
    .glow-red { text-shadow: 0 0 20px rgba(239, 68, 68, 0.5); }
    .glow-yellow { text-shadow: 0 0 20px rgba(234, 179, 8, 0.5); }
    .glow-purple { text-shadow: 0 0 20px rgba(99, 102, 241, 0.5); }
</style>
""", unsafe_allow_html=True)


# Import the auditor with proper error handling for Streamlit Cloud
import sys
import os

# Ensure the current directory is in the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from seo_auditor import AdvancedSEOAuditor, SEOAuditResult, print_audit_report
except KeyError:
    # Handle Python 3.13 import issue - clear and retry
    if 'seo_auditor' in sys.modules:
        del sys.modules['seo_auditor']
    from seo_auditor import AdvancedSEOAuditor, SEOAuditResult, print_audit_report


def display_score_card(result):
    """Display the main score card"""
    if result.score >= 80:
        score_color = "#22c55e"
        score_label = "Excellent"
        grade_icon = "fa-solid fa-trophy"
        glow_class = "glow-green"
    elif result.score >= 60:
        score_color = "#eab308"
        score_label = "Needs Improvement"
        grade_icon = "fa-solid fa-chart-line"
        glow_class = "glow-yellow"
    else:
        score_color = "#ef4444"
        score_label = "Poor"
        grade_icon = "fa-solid fa-triangle-exclamation"
        glow_class = "glow-red"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="score-card-container animate-in">
            <div class="score-ring" style="--score-color: {score_color}; --score-percent: {result.score};">
                <span style="font-size: 3.5rem; font-weight: 700; color: {score_color}; line-height: 1;" class="{glow_class}">{result.score}</span>
                <span style="font-size: 1.1rem; color: {score_color}; font-weight: 500;">/ 100</span>
            </div>
            <div style="margin-bottom: 15px;">
                <span style="background: linear-gradient(135deg, {score_color} 0%, {score_color}88 100%); padding: 8px 24px; border-radius: 50px; font-weight: 600; font-size: 0.9rem; color: #0a0a0f;">
                    Grade {result.grade}
                </span>
            </div>
            <p style="font-size: 1.4rem; color: {score_color}; font-weight: 600; margin: 15px 0;">
                <i class="{grade_icon}" style="margin-right: 8px;"></i>{score_label}
            </p>
            <div style="display: flex; justify-content: center; gap: 30px; margin-top: 20px; color: #64748b; font-size: 0.85rem;">
                <span><i class="fa-regular fa-calendar" style="margin-right: 6px;"></i>{result.audit_date}</span>
                <span><i class="fa-solid fa-list-check" style="margin-right: 6px;"></i>300+ Checks</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def display_quick_stats(result):
    """Display quick stats row"""
    st.markdown(f"""
    <div class="stats-grid animate-in">
        <div class="stat-card passed">
            <div class="stat-value">{result.checks_passed}</div>
            <div class="stat-label"><i class="fa-solid fa-circle-check" style="color: #22c55e; margin-right: 5px;"></i>Passed</div>
        </div>
        <div class="stat-card warning">
            <div class="stat-value">{result.checks_warnings}</div>
            <div class="stat-label"><i class="fa-solid fa-triangle-exclamation" style="color: #eab308; margin-right: 5px;"></i>Warnings</div>
        </div>
        <div class="stat-card critical">
            <div class="stat-value">{result.checks_failed}</div>
            <div class="stat-label"><i class="fa-solid fa-circle-xmark" style="color: #ef4444; margin-right: 5px;"></i>Critical</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{result.response_time:.2f}s</div>
            <div class="stat-label"><i class="fa-solid fa-gauge-high" style="color: #6366f1; margin-right: 5px;"></i>Response</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_meta_tags(result):
    """Display meta tags analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-tags"></i> Meta Tags Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Title Tag**")
        st.info(f"{result.title_status}")
        st.text(result.title[:80] if result.title else "Not found")
        
        tcol1, tcol2, tcol3 = st.columns(3)
        tcol1.metric("Length", f"{result.title_length}ch")
        tcol2.metric("Pixel Width", f"~{result.title_pixel_width}px")
        tcol3.metric("Has Numbers", "Yes" if result.title_has_numbers else "No")
        
        st.caption(f"Power Words: {'Yes' if result.title_has_power_words else 'No'} | Keyword: {'Yes' if result.title_has_keyword else 'No'}")
    
    with col2:
        st.markdown("**Meta Description**")
        st.info(f"{result.meta_description_status}")
        st.text(result.meta_description[:100] + "..." if result.meta_description and len(result.meta_description) > 100 else result.meta_description or "Not found")
        
        dcol1, dcol2, dcol3 = st.columns(3)
        dcol1.metric("Length", f"{result.meta_description_length}ch")
        dcol2.metric("Has CTA", "Yes" if result.meta_description_has_cta else "No")
        dcol3.metric("Keyword", "Yes" if result.meta_description_has_keyword else "No")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Canonical URL**")
        st.text(result.canonical_url[:50] + "..." if result.canonical_url and len(result.canonical_url) > 50 else result.canonical_url or "Missing")
    with col2:
        st.markdown("**Robots Meta**")
        st.text(result.robots_meta or "Not specified")
        st.caption(f"Index: {'Yes' if result.robots_index else 'No'} | Follow: {'Yes' if result.robots_follow else 'No'}")
    with col3:
        st.markdown("**Meta Keywords**")
        st.text(f"{result.meta_keywords_count} keywords" if result.meta_keywords else "Not set")


def display_social_tags(result):
    """Display social media tags"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-share-nodes"></i> Social Media Tags</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Open Graph ({result.og_score}% Complete)**")
        og_items = [
            ("Title", result.og_title),
            ("Description", result.og_description),
            ("Image", result.og_image),
            ("URL", result.og_url),
            ("Type", result.og_type),
            ("Site Name", result.og_site_name),
        ]
        for name, value in og_items:
            status = "[+]" if value else "[-]"
            st.text(f"{status} {name}: {(value[:40] + '...' if value and len(str(value)) > 40 else value) or 'Missing'}")
    
    with col2:
        st.markdown(f"**Twitter Cards ({result.twitter_score}% Complete)**")
        twitter_items = [
            ("Card Type", result.twitter_card),
            ("Title", result.twitter_title),
            ("Description", result.twitter_description),
            ("Image", result.twitter_image),
            ("Site", result.twitter_site),
            ("Creator", result.twitter_creator),
        ]
        for name, value in twitter_items:
            status = "[+]" if value else "[-]"
            st.text(f"{status} {name}: {(value[:40] + '...' if value and len(str(value)) > 40 else value) or 'Missing'}")


def display_headings(result):
    """Display headings analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-heading"></i> Heading Structure</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("H1", result.h1_count, delta=result.heading_structure_status)
    col2.metric("H2", result.h2_count)
    col3.metric("H3", result.h3_count)
    col4.metric("H4", result.h4_count)
    col5.metric("H5", result.h5_count)
    col6.metric("H6", result.h6_count)
    
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("Total", result.total_headings)
    mcol2.metric("Hierarchy", "Valid" if result.heading_hierarchy_valid else "Invalid")
    mcol3.metric("Empty", result.empty_headings)
    mcol4.metric("Duplicates", result.duplicate_headings)
    
    if result.h1_tags:
        with st.expander(f"View H1 Tags ({len(result.h1_tags)})"):
            for h1 in result.h1_tags:
                st.write(f"- {h1}")
    
    if result.h2_tags:
        with st.expander(f"View H2 Tags ({len(result.h2_tags)})"):
            for h2 in result.h2_tags[:10]:
                st.write(f"- {h2}")


def display_images(result):
    """Display images analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-images"></i> Images Analysis</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Images", result.total_images)
    col2.metric("Missing Alt", result.images_without_alt, delta=result.images_status)
    col3.metric("Empty Alt", result.images_with_empty_alt)
    col4.metric("Score", f"{result.images_score}/100")
    
    st.markdown("**Optimization**")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lazy Loading", result.images_with_lazy_loading)
    col2.metric("Srcset", result.images_with_srcset)
    col3.metric("In <picture>", result.images_in_picture)
    col4.metric("Avg Alt Length", f"{result.avg_alt_length:.0f}ch")
    
    st.markdown("**Formats**")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("WebP", result.images_webp)
    col2.metric("PNG", result.images_png)
    col3.metric("JPG", result.images_jpg)
    col4.metric("SVG", result.images_svg)
    col5.metric("GIF", result.images_gif)


def display_links(result):
    """Display links analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-link"></i> Links Analysis</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Links", result.total_links)
    col2.metric("Internal", result.internal_links, delta=f"Unique: {result.unique_internal_links}")
    col3.metric("External", result.external_links, delta=f"Unique: {result.unique_external_links}")
    col4.metric("Score", f"{result.links_score}/100")
    
    st.markdown("**Link Attributes**")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("DoFollow", result.dofollow_links)
    col2.metric("NoFollow", result.nofollow_links)
    col3.metric("Sponsored", result.sponsored_links)
    col4.metric("UGC", result.ugc_links)
    
    st.markdown("**Link Types**")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Text Links", result.text_links)
    col2.metric("Image Links", result.image_links)
    col3.metric("Empty Anchor", result.empty_anchor_links)
    col4.metric("JS Links", result.javascript_links)
    
    if result.links_without_noopener > 0:
        st.warning(f"{result.links_without_noopener} links with target='_blank' missing rel='noopener' (security issue)")


def display_technical(result):
    """Display technical SEO"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-gears"></i> Technical SEO</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Core Technical**")
        items = [
            ("HTTPS/SSL", result.has_ssl),
            ("Viewport", result.has_viewport),
            ("Charset", result.has_charset),
            ("HTML Lang", bool(result.html_lang)),
            ("Doctype", result.has_doctype),
        ]
        for name, value in items:
            st.write(f"{'[+]' if value else '[-]'} {name}")
    
    with col2:
        st.markdown("**Branding & PWA**")
        items = [
            ("Favicon", result.has_favicon),
            ("Apple Touch Icon", result.has_apple_touch_icon),
            ("Web Manifest", result.has_manifest),
            ("Theme Color", result.has_theme_color),
        ]
        for name, value in items:
            st.write(f"{'[+]' if value else '[-]'} {name}")
    
    with col3:
        st.markdown("**Schema Markup**")
        st.write(f"{'[+]' if result.has_schema_markup else '[-]'} Schema.org: {result.schema_count} schemas")
        if result.schema_types:
            st.caption(f"Types: {', '.join(result.schema_types[:5])}")
        st.write(f"Microdata: {result.microdata_items}")
        st.write(f"RDFa: {result.rdfa_items}")
    
    st.markdown("---")
    
    st.markdown("**Resources & Performance**")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CSS Files", result.total_css_files)
    col2.metric("JS Files", result.total_js_files)
    col3.metric("Render Block CSS", result.render_blocking_css)
    col4.metric("Render Block JS", result.render_blocking_js)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Async JS", result.async_js)
    col2.metric("Defer JS", result.defer_js)
    col3.metric("Inline CSS", f"{result.inline_css_count} ({result.inline_css_size}b)")
    col4.metric("Inline JS", f"{result.inline_js_count} ({result.inline_js_size}b)")
    
    st.markdown("---")
    
    st.markdown("**HTTP & Security Headers**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"HTTP Status: {result.http_status}")
        st.write(f"Server: {result.server or 'Not disclosed'}")
        st.write(f"Gzip: {'Yes' if result.has_gzip else 'No'} ({result.content_encoding or 'None'})")
        st.write(f"Cache Headers: {'Yes' if result.has_cache_headers else 'No'}")
    
    with col2:
        st.metric("Security Score", f"{result.security_headers_score}%")
        security_items = [
            ("HSTS", result.has_hsts),
            ("XSS Protection", result.has_xss_protection),
            ("Content-Type-Options", result.has_content_type_options),
            ("X-Frame-Options", result.has_frame_options),
            ("CSP", result.has_csp),
        ]
        for name, value in security_items:
            st.write(f"{'[+]' if value else '[-]'} {name}")


def display_content(result):
    """Display content analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-file-lines"></i> Content Analysis</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Words", result.word_count)
    col2.metric("Sentences", result.sentence_count)
    col3.metric("Paragraphs", result.paragraph_count)
    col4.metric("Score", f"{result.content_score}/100")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Sentence", f"{result.avg_sentence_length} words")
    col2.metric("Unique Words", result.unique_words)
    col3.metric("Lexical Density", f"{result.lexical_density}%")
    col4.metric("Text/HTML Ratio", f"{result.text_html_ratio}%")
    
    st.markdown("**Readability**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Flesch Reading Ease", result.flesch_reading_ease)
    col2.metric("Grade Level", result.flesch_kincaid_grade)
    col3.info(result.readability_status)
    
    st.markdown("**Content Elements**")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lists", f"{result.unordered_lists} UL / {result.ordered_lists} OL")
    col2.metric("Tables", result.table_count)
    col3.metric("Blockquotes", result.blockquote_count)
    col4.metric("Code Blocks", result.code_block_count)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Bold", result.bold_text_count)
    col2.metric("Italic", result.italic_text_count)
    col3.metric("Videos", result.video_count)
    col4.metric("Iframes", result.iframe_count)
    
    if result.top_keywords:
        with st.expander("Top Keywords"):
            df = pd.DataFrame(result.top_keywords, columns=["Keyword", "Count"])
            st.dataframe(df, width=None)


def display_mobile_ux(result):
    """Display mobile & UX"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-mobile-screen"></i> Mobile & UX</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mobile Friendly", "Yes" if result.is_mobile_friendly else "No")
    col2.metric("AMP Version", "Yes" if result.has_amp_version else "No")
    col3.metric("Touch Icons", result.touch_icons_count)
    col4.metric("UX Score", f"{result.ux_score}/100")


def display_i18n(result):
    """Display internationalization"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-globe"></i> Internationalization</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Hreflang Tags", result.hreflang_count)
    col2.metric("X-Default", "Yes" if result.has_x_default else "No")
    col3.metric("HTML Lang", result.detected_language or "Not set")
    col4.metric("Score", f"{result.i18n_score}/100")


def display_ecommerce(result):
    """Display e-commerce & rich snippets"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-store"></i> E-Commerce & Rich Snippets</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Product Schema**")
        st.write(f"{'[+]' if result.has_product_schema else '[-]'} Product Schema")
        if result.has_product_schema:
            st.caption(f"Name: {result.product_name}")
            st.caption(f"Price: {result.product_price} {result.product_currency}")
    
    with col2:
        st.markdown("**Navigation**")
        st.write(f"{'[+]' if result.has_breadcrumbs else '[-]'} Breadcrumbs ({result.breadcrumb_levels} levels)")
        st.write(f"{'[+]' if result.has_breadcrumb_schema else '[-]'} Breadcrumb Schema")
    
    with col3:
        st.markdown("**Rich Snippets**")
        items = [
            ("FAQ Schema", result.has_faq_schema, result.faq_questions_count),
            ("HowTo Schema", result.has_howto_schema, 0),
            ("Recipe Schema", result.has_recipe_schema, 0),
            ("Event Schema", result.has_event_schema, 0),
            ("LocalBusiness", result.has_local_business_schema, 0),
            ("Reviews", result.has_reviews_schema, 0),
        ]
        for name, has_it, count in items:
            extra = f" ({count} items)" if count else ""
            st.write(f"{'[+]' if has_it else '[-]'} {name}{extra}")


def display_accessibility(result):
    """Display accessibility"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-universal-access"></i> Accessibility</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.accessibility_score}/100")
    col2.metric("ARIA Labels", result.aria_labels_count)
    col3.metric("ARIA Roles", result.aria_roles_count)
    col4.metric("Form Issues", result.forms_without_labels)
    
    st.markdown("**Landmarks**")
    col1, col2, col3, col4 = st.columns(4)
    col1.write(f"{'[+]' if result.has_skip_link else '[-]'} Skip Link")
    col2.write(f"{'[+]' if result.has_main_landmark else '[-]'} Main")
    col3.write(f"{'[+]' if result.has_nav_landmark else '[-]'} Navigation")
    col4.write(f"{'[+]' if result.has_footer_landmark else '[-]'} Footer")


def display_performance(result):
    """Display performance hints"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-bolt"></i> Performance Hints</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.performance_hints_score}/100")
    col2.write(f"{'[+]' if result.has_preload else '[-]'} Preload")
    col3.write(f"{'[+]' if result.has_preconnect else '[-]'} Preconnect")
    col4.write(f"{'[+]' if result.has_dns_prefetch else '[-]'} DNS Prefetch")
    
    if result.preconnect_domains:
        with st.expander("Preconnect Domains"):
            for domain in result.preconnect_domains[:5]:
                st.write(f"- {domain}")


def display_issues(result):
    """Display all issues"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-clipboard-list"></i> Issues & Recommendations</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        f"Critical ({len(result.critical_issues)})",
        f"Warnings ({len(result.warnings)})",
        f"Recommendations ({len(result.recommendations)})",
        f"Passed ({len(result.passed_checks)})"
    ])
    
    with tab1:
        if result.critical_issues:
            for issue in result.critical_issues:
                st.markdown(f'<div class="issue-critical"><i class="fa-solid fa-xmark" style="color:#ef4444;"></i> {issue}</div>', unsafe_allow_html=True)
        else:
            st.success("No critical issues found.")
    
    with tab2:
        if result.warnings:
            for warning in result.warnings:
                st.markdown(f'<div class="issue-warning"><i class="fa-solid fa-triangle-exclamation" style="color:#eab308;"></i> {warning}</div>', unsafe_allow_html=True)
        else:
            st.success("No warnings detected.")
    
    with tab3:
        if result.recommendations:
            for rec in result.recommendations:
                st.markdown(f'<div class="issue-recommendation"><i class="fa-solid fa-lightbulb" style="color:#3b82f6;"></i> {rec}</div>', unsafe_allow_html=True)
        else:
            st.info("No additional recommendations.")
    
    with tab4:
        if result.passed_checks:
            for check in result.passed_checks:
                st.markdown(f'<div class="issue-passed"><i class="fa-solid fa-check" style="color:#22c55e;"></i> {check}</div>', unsafe_allow_html=True)


def display_export(result):
    """Display export options"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-download"></i> Export Report</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 20px; margin-bottom: 20px;">
        <p style="color: #a5b4fc; font-weight: 600; margin: 0 0 5px 0;"><i class="fa-solid fa-file-pdf" style="margin-right: 8px;"></i>Professional PDF Report</p>
        <p style="color: #64748b; font-size: 0.9rem; margin: 0;">Perfect for sharing with clients or team members</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        from pdf_report_generator import generate_pdf_report
        pdf_buffer = generate_pdf_report(result)
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name=f"seo_report_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            type="primary"
        )
    except ImportError:
        st.warning("PDF generation requires 'reportlab'. Install with: pip install reportlab")
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
    
    st.markdown("---")
    
    st.markdown("""
    <p style="color: #94a3b8; font-weight: 500; margin-bottom: 15px;"><i class="fa-solid fa-file-export" style="color: #6366f1; margin-right: 8px;"></i>Other Export Formats</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        json_data = json.dumps(asdict(result), indent=2, default=str)
        st.download_button(
            label="JSON Data",
            data=json_data,
            file_name=f"seo_audit_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col2:
        text_report = print_audit_report(result)
        st.download_button(
            label="Text Report",
            data=text_report,
            file_name=f"seo_audit_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    with col3:
        summary_data = {
            "Metric": ["Score", "Grade", "Words", "Images", "Links", "Critical", "Warnings"],
            "Value": [result.score, result.grade, result.word_count, result.total_images, 
                     result.total_links, len(result.critical_issues), len(result.warnings)]
        }
        df = pd.DataFrame(summary_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="CSV Summary",
            data=csv,
            file_name=f"seo_summary_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


def display_crawling_indexing(result):
    """Display crawling & indexing analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-robot"></i> Crawling & Indexing</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.crawling_score}/100")
    col2.metric("Indexable", "Yes" if result.is_indexable else "No")
    col3.metric("URL Depth", result.url_depth)
    col4.metric("URL Length", f"{result.url_length} chars")
    
    st.markdown("**URL Analysis**")
    col1, col2, col3, col4 = st.columns(4)
    col1.write(f"{'[+]' if result.url_structure_friendly else '[-]'} SEO-Friendly URL")
    col2.write(f"{'[+]' if not result.url_has_parameters else '[!]'} {'No' if not result.url_has_parameters else 'Has'} Query Params")
    col3.write(f"{'[+]' if not result.url_has_underscores else '[!]'} {'No' if not result.url_has_underscores else 'Has'} Underscores")
    col4.write(f"{'[+]' if result.url_length <= 75 else '[!]'} URL Length {'OK' if result.url_length <= 75 else 'Long'}")
    
    st.markdown("**Indexability Signals**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"{'[-] Blocked' if result.robots_txt_blocks_url else '[+] Allowed'} by robots.txt")
        st.write(f"X-Robots-Tag: {result.x_robots_tag or 'Not set'}")
    with col2:
        st.write(f"{'[!] Redirect Chain' if result.has_redirect_chain else '[+] No'} Redirect Chain")
        if result.has_redirect_chain:
            st.caption(f"Chain length: {result.redirect_chain_length}")
    with col3:
        st.write(f"{'[-]' if result.has_5xx_error else '[+]'} {'5xx Error' if result.has_5xx_error else 'No Server Errors'}")
        st.write(f"{'[+]' if result.has_noindex_system_pages else '[!]'} System Pages Noindexed")


def display_content_quality(result):
    """Display content quality analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-pen-fancy"></i> Content Quality & E-E-A-T</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.content_quality_score}/100")
    col2.metric("Thin Content", "Yes" if result.has_thin_content else "No")
    col3.metric("Unique Content", "Yes" if result.content_is_unique else "Check")
    col4.metric("E-E-A-T Signals", "Yes" if result.has_eeat_signals else "Missing")
    
    st.markdown("**Trust & Authority Signals**")
    col1, col2, col3, col4 = st.columns(4)
    col1.write(f"{'[+]' if result.has_privacy_policy else '[-]'} Privacy Policy")
    col2.write(f"{'[+]' if result.has_contact_page else '[-]'} Contact Page")
    col3.write(f"{'[+]' if result.has_about_page else '[-]'} About Page")
    col4.write(f"{'[+]' if result.has_author_info else '[-]'} Author Info")
    
    if result.author_name:
        st.caption(f"Author: {result.author_name}")
    
    st.markdown("**Content Dates**")
    col1, col2 = st.columns(2)
    col1.write(f"Published: {result.publication_date or 'Not specified'}")
    col2.write(f"Modified: {result.modified_date or 'Not specified'}")
    
    st.markdown("**Content Issues**")
    col1, col2, col3, col4 = st.columns(4)
    col1.write(f"{'[-] Found' if result.has_hidden_text else '[+] None'} Hidden Text")
    col2.write(f"{'[-] Heavy' if result.has_heavy_above_fold_ads else '[+] OK'} Above-Fold Ads")
    col3.write(f"{'[-] Found' if result.content_in_iframes else '[+] None'} Content in iFrames")
    col4.write(f"{'[-] Found' if result.has_intrusive_interstitials else '[+] None'} Intrusive Popups")
    
    st.markdown("**Content Best Practices**")
    col1, col2 = st.columns(2)
    col1.write(f"{'[+]' if result.has_clear_cta else '[!]'} Clear Call-to-Action")
    col2.write(f"{'[+]' if result.uses_semantic_html else '[!]'} Semantic HTML")


def display_keyword_analysis(result):
    """Display keyword optimization analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-key"></i> Keyword Analysis</div>', unsafe_allow_html=True)
    
    if result.target_keyword:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Score", f"{result.keyword_analysis_score}/100")
        col2.metric("Target Keyword", result.target_keyword)
        col3.metric("Occurrences", result.keyword_count_in_body)
        col4.metric("Density", f"{result.keyword_density_percent:.2f}%")
        
        st.markdown("**Keyword Placement**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"{'[+]' if result.keyword_in_title else '[-]'} In Title Tag")
            if result.keyword_in_title:
                pos_text = "Front" if result.keyword_in_title_position == 1 else "Middle/End"
                st.caption(f"Position: {pos_text}")
            st.write(f"{'[+]' if result.title_starts_with_keyword else '[!]'} Title Starts with Keyword")
        
        with col2:
            st.write(f"{'[+]' if result.keyword_in_meta_desc else '[-]'} In Meta Description")
            st.write(f"{'[+]' if result.keyword_in_h1 else '[-]'} In H1 Tag")
        
        with col3:
            st.write(f"{'[+]' if result.keyword_in_h2 else '[-]'} In H2 Tags")
            st.write(f"{'[+]' if result.keyword_in_first_paragraph else '[-]'} In First 100 Words")
        
        st.markdown("**Keyword Usage**")
        if result.keyword_overuse:
            st.warning("Keyword may be overused (density > 3%). Consider reducing for natural content.")
        elif result.keyword_density_percent < 0.5:
            st.info("Consider using keyword more naturally in content (current density < 0.5%)")
        else:
            st.success("Keyword density appears optimal (0.5-3%)")
    else:
        st.info("Enter a target keyword when running the audit to see keyword optimization analysis")


def display_mobile_advanced(result):
    """Display advanced mobile analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-mobile-retro"></i> Advanced Mobile Optimization</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.mobile_advanced_score}/100")
    col2.metric("Page Weight", f"{result.mobile_page_weight_kb:.0f} KB")
    col3.metric("Heavy Page", "Yes" if result.mobile_page_heavy else "No")
    col4.metric("Mobile Friendly", "Yes" if result.is_mobile_friendly else "No")
    
    st.markdown("**Mobile Usability**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"{'[+]' if result.tap_targets_sized_correctly else '[-]'} Tap Targets Sized")
        if result.tap_target_issues > 0:
            st.caption(f"Issues: {result.tap_target_issues} elements")
    
    with col2:
        st.write(f"{'[+]' if result.font_sizes_readable else '[-]'} Readable Font Sizes")
        if result.small_font_elements > 0:
            st.caption(f"Small fonts: {result.small_font_elements}")
    
    with col3:
        st.write(f"{'[+]' if result.content_width_fits_viewport else '[!]'} Content Fits Viewport")
    
    st.markdown("**Mobile Navigation & Images**")
    col1, col2, col3 = st.columns(3)
    col1.write(f"{'[+]' if result.mobile_navigation_friendly else '[!]'} Mobile-Friendly Navigation")
    col2.write(f"{'[+]' if result.thumb_friendly_navigation else '[!]'} Thumb-Friendly Nav")
    col3.write(f"{'[+]' if result.has_responsive_images else '[!]'} Responsive Images")
    
    st.markdown("**Mobile-Desktop Parity**")
    col1, col2, col3 = st.columns(3)
    col1.write(f"{'[+]' if result.mobile_desktop_parity else '[!]'} Content Parity")
    col2.write(f"{'[+]' if result.mobile_meta_parity else '[!]'} Meta Tags Parity")
    col3.write(f"{'[+]' if result.mobile_directives_parity else '[!]'} Directives Parity")
    col4 = st.columns(1)[0]
    col4.write(f"{'[+]' if result.favicon_in_mobile_serps else '[!]'} Favicon for Mobile SERPs")


def display_page_elements(result):
    """Display page elements analysis"""
    st.markdown('<div class="section-header"><i class="fa-solid fa-puzzle-piece"></i> Page Elements Analysis</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.page_elements_score}/100")
    col2.metric("Multiple H1s", "Yes" if result.has_multiple_h1 else "No")
    col3.metric("Title-Content Match", "Yes" if result.title_matches_content else "Check")
    col4.metric("Unique Meta Desc", "Yes" if result.meta_desc_is_unique else "Check")
    
    st.markdown("**Content Structure**")
    col1, col2, col3 = st.columns(3)
    col1.write(f"{'[+]' if result.primary_content_clear else '[!]'} Primary Content Clear")
    col2.write(f"{'[+]' if result.supplementary_content_marked else '[!]'} Supplementary Content Marked")
    col3.write(f"{'[+]' if result.meta_desc_compelling else '[!]'} Compelling Meta Description")
    
    st.markdown("**Visual & Accessibility**")
    col1, col2 = st.columns(2)
    col1.write(f"{'[+]' if result.text_contrast_sufficient else '[!]'} Sufficient Text Contrast")
    col2.write(f"{'[+]' if result.links_distinguishable else '[!]'} Links Distinguishable")


def main():
    # Initialize session state for storing audit results
    if 'audit_result' not in st.session_state:
        st.session_state.audit_result = None
    if 'audited_url' not in st.session_state:
        st.session_state.audited_url = None
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);">
                <i class="fa-solid fa-magnifying-glass-chart" style="color: white; font-size: 1.5rem;"></i>
            </div>
            <h2 style="margin: 0; font-size: 1.3rem; color: #f1f5f9;">SEO Audit Tool</h2>
            <p style="color: #64748b; font-size: 0.85rem; margin: 5px 0 0 0;">Version 3.0 | 300+ Checks</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="color: #94a3b8; font-size: 0.9rem;">
        <p style="font-weight: 600; color: #e2e8f0; margin-bottom: 12px;">Analysis Categories:</p>
        <ul style="list-style: none; padding: 0; margin: 0;">
            <li style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">Meta Tags <span style="float: right; color: #6366f1;">20+</span></li>
            <li style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">Social Tags <span style="float: right; color: #6366f1;">25+</span></li>
            <li style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">Content & Headings <span style="float: right; color: #6366f1;">55+</span></li>
            <li style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">Images & Links <span style="float: right; color: #6366f1;">55+</span></li>
            <li style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">Technical SEO <span style="float: right; color: #6366f1;">40+</span></li>
            <li style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">Mobile & UX <span style="float: right; color: #6366f1;">35+</span></li>
            <li style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">Accessibility <span style="float: right; color: #6366f1;">15+</span></li>
            <li style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">E-E-A-T & Quality <span style="float: right; color: #6366f1;">35+</span></li>
            <li style="padding: 6px 0;">Performance <span style="float: right; color: #6366f1;">25+</span></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; padding: 15px; text-align: center;">
            <p style="color: #a5b4fc; font-size: 0.8rem; margin: 0;">Plerdy Checklist Compliant</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 0.85rem;">
            <p style="margin-bottom: 8px;">Created by</p>
            <a href="https://muntasir-islam.github.io" target="_blank" style="color: #a5b4fc; text-decoration: none; font-weight: 500;">Muntasir Islam</a>
            <p style="margin-top: 5px; font-size: 0.8rem;">SEO Specialist | Web Strategist</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div style="position: relative; z-index: 1;">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin: 0 0 10px 0; background: linear-gradient(135deg, #f1f5f9 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Advanced SEO Audit Tool
            </h1>
            <p style="color: #94a3b8; font-size: 1.1rem; margin: 0;">
                Enterprise-grade analysis with <span style="color: #a5b4fc; font-weight: 600;">300+ parameters</span> — Plerdy Checklist Compliant
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section with better styling
    st.markdown("""
    <div style="background: linear-gradient(145deg, #1e1e32 0%, #16162a 100%); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; margin-bottom: 20px;">
        <p style="color: #e2e8f0; font-weight: 500; margin-bottom: 15px;"><i class="fa-solid fa-globe" style="color: #6366f1; margin-right: 8px;"></i>Enter Website Details</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input row
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input(
            "Website URL",
            placeholder="example.com or https://example.com",
            help="Enter the full URL of the page you want to audit",
            label_visibility="collapsed",
            key="url_input"
        )
    
    with col2:
        keyword = st.text_input(
            "Target Keyword (optional)",
            placeholder="seo audit",
            help="Enter your target keyword to check optimization",
            key="keyword_input"
        )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        audit_button = st.button("Run SEO Audit")
    
    # Helper function to normalize URL for comparison
    def normalize_url(u):
        if not u:
            return ""
        u = u.strip()
        if not u.startswith(('http://', 'https://')):
            u = 'https://' + u
        return u.rstrip('/')
    
    # Run audit when button is clicked
    if audit_button and url:
        normalized_input_url = normalize_url(url)
        
        # Always run a fresh audit when button is clicked
        with st.spinner("Analyzing 300+ SEO parameters... This may take 10-20 seconds."):
            progress = st.progress(0)
            status = st.empty()
            
            try:
                status.text("Initializing audit...")
                progress.progress(10)
                
                # Create a fresh auditor instance for each audit
                auditor = AdvancedSEOAuditor(url, target_keyword=keyword if keyword else None)
                
                status.text(f"Fetching and analyzing {auditor.url}...")
                progress.progress(30)
                
                # Run the full audit
                result = auditor.run_audit()
                
                progress.progress(90)
                
                if result:
                    # Show debug info about what was found
                    status.text(f"Found: {result.title[:40] if result.title else 'No title'}...")
                    progress.progress(100)
                    status.empty()
                    
                    # Store in session state to persist across reruns
                    st.session_state.audit_result = result
                    st.session_state.audited_url = normalized_input_url
                    
                    # Show the URL and score for verification
                    st.toast(f"✅ Score: {result.score} | {result.url}")
                    st.rerun()  # Rerun to display results cleanly
                else:
                    progress.progress(100)
                    status.empty()
                    st.error(f"Failed to audit: {auditor.url}")
                    st.info("**Possible reasons:**\n- Website blocks automated requests\n- URL is unreachable\n- Network/firewall issues\n- Try a different URL")
                        
            except Exception as e:
                progress.progress(100)
                status.empty()
                st.error(f"Error during audit: {str(e)}")
                import traceback
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())
    
    elif audit_button and not url:
        st.warning("Please enter a URL to audit")
    
    # Display results if available in session state
    if st.session_state.audit_result is not None:
        result = st.session_state.audit_result
        
        # Show info about which URL these results are for
        current_normalized = normalize_url(url) if url else ""
        if url and current_normalized != st.session_state.audited_url:
            st.info(f"💡 Showing results for: **{st.session_state.audited_url}**. Click 'Run SEO Audit' to analyze the new URL.")
        
        st.success(f"✅ Audit complete for **{result.url}**")
        
        # Debug info - show key data that was extracted
        with st.expander("📋 Debug: Extracted Data", expanded=False):
            st.write(f"**URL:** {result.url}")
            st.write(f"**Title:** {result.title or 'Not found'}")
            st.write(f"**Title Length:** {result.title_length} characters")
            st.write(f"**Meta Description:** {result.meta_description[:200] if result.meta_description else 'Not found'}...")
            st.write(f"**Score:** {result.score}")
            st.write(f"**Grade:** {result.grade}")
            st.write(f"**Response Time:** {result.response_time:.2f}s")
            st.write(f"**Word Count:** {result.word_count}")
            st.write(f"**H1 Count:** {result.h1_count}")
        
        # Display all sections
        display_score_card(result)
        display_quick_stats(result)
        
        st.divider()
        
        # Use tabs for organization - 7 tabs now
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Meta & Social",
            "Content & Structure",
            "Technical",
            "Mobile & A11y",
            "Crawling & Indexing",
            "Keywords & Quality",
            "Issues"
        ])
        
        with tab1:
            display_meta_tags(result)
            st.divider()
            display_social_tags(result)
        
        with tab2:
            display_headings(result)
            st.divider()
            display_images(result)
            st.divider()
            display_links(result)
            st.divider()
            display_content(result)
        
        with tab3:
            display_technical(result)
            st.divider()
            display_performance(result)
            st.divider()
            display_page_elements(result)
        
        with tab4:
            display_mobile_ux(result)
            st.divider()
            display_mobile_advanced(result)
            st.divider()
            display_i18n(result)
            st.divider()
            display_ecommerce(result)
            st.divider()
            display_accessibility(result)
        
        with tab5:
            display_crawling_indexing(result)
        
        with tab6:
            display_keyword_analysis(result)
            st.divider()
            display_content_quality(result)
        
        with tab7:
            display_issues(result)
        
        st.divider()
        display_export(result)
        
        # Add a button to clear results and run new audit
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Clear & Run New Audit"):
                st.session_state.audit_result = None
                st.session_state.audited_url = None
                # Clear the input fields by removing their keys
                if 'url_input' in st.session_state:
                    del st.session_state.url_input
                if 'keyword_input' in st.session_state:
                    del st.session_state.keyword_input
                st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer-container">
        <div class="footer-links" style="margin-bottom: 20px;">
            <a href="https://github.com/muntasir-islam/seo_audit_tool" target="_blank">
                <i class="fa-brands fa-github"></i> Star on GitHub
            </a>
            <a href="https://twitter.com/intent/tweet?text=Check%20out%20this%20free%20SEO%20Audit%20Tool%20with%20300%2B%20parameters!&url=https://seo-audit-tool.streamlit.app" target="_blank">
                <i class="fa-brands fa-x-twitter"></i> Share on X
            </a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://seo-audit-tool.streamlit.app" target="_blank">
                <i class="fa-brands fa-linkedin"></i> LinkedIn
            </a>
        </div>
        <div style="color: #64748b;">
            <p style="margin: 0 0 8px 0;">Built by <a href="https://muntasir-islam.github.io" target="_blank" style="color: #a5b4fc; text-decoration: none;">Muntasir Islam</a></p>
            <p style="font-size: 0.85rem; margin: 0 0 8px 0; color: #475569;">&copy; 2026 | Advanced SEO Audit Tool v3.0</p>
            <div style="display: flex; justify-content: center; gap: 20px; font-size: 0.8rem; color: #475569;">
                <span><i class="fa-solid fa-lock" style="color: #22c55e;"></i> No data stored</span>
                <span><i class="fa-solid fa-bolt" style="color: #6366f1;"></i> Powered by Streamlit</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
