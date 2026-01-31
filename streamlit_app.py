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
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/muntasir-islam/seo_audit_tool',
        'Report a bug': 'https://github.com/muntasir-islam/seo_audit_tool/issues',
        'About': '### 🔍 Advanced SEO Audit Tool\n\n**300+ SEO parameters analyzed**\n\nCreated by Muntasir Islam'
    }
)

# Custom CSS
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%); }
    .stApp { background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%); }
    .score-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: #1e293b;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    .status-good { color: #22c55e; }
    .status-warning { color: #eab308; }
    .status-bad { color: #ef4444; }
    .issue-critical {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    .issue-warning {
        background: rgba(234, 179, 8, 0.1);
        border-left: 4px solid #eab308;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    .issue-recommendation {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    .issue-passed {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 1.1rem;
        border-radius: 10px;
        width: 100%;
    }
    .category-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 15px 20px;
        border-radius: 10px;
        margin: 20px 0 10px 0;
    }
    .param-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)


# Import the auditor
from seo_auditor import AdvancedSEOAuditor, SEOAuditResult, print_audit_report


def display_score_card(result):
    """Display the main score card"""
    if result.score >= 80:
        score_color = "#22c55e"
        score_label = "Excellent"
        grade_emoji = "🏆"
    elif result.score >= 60:
        score_color = "#eab308"
        score_label = "Needs Improvement"
        grade_emoji = "📈"
    else:
        score_color = "#ef4444"
        score_label = "Poor"
        grade_emoji = "⚠️"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); border-radius: 20px; margin-bottom: 30px;">
            <div style="width: 180px; height: 180px; border-radius: 50%; border: 10px solid {score_color}; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;
                        background: rgba(0,0,0,0.3); flex-direction: column;">
                <span style="font-size: 3.5rem; font-weight: bold; color: {score_color};">{result.score}</span>
                <span style="font-size: 1.2rem; color: {score_color};">Grade: {result.grade}</span>
            </div>
            <p style="font-size: 1.5rem; color: {score_color}; font-weight: 600;">{grade_emoji} {score_label}</p>
            <p style="color: #94a3b8; margin-top: 10px;">Audited: {result.audit_date}</p>
            <p style="color: #64748b; font-size: 0.9rem;">300+ Parameters Analyzed</p>
        </div>
        """, unsafe_allow_html=True)


def display_quick_stats(result):
    """Display quick stats row"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ Passed", result.checks_passed, delta="checks")
    with col2:
        st.metric("⚠️ Warnings", result.checks_warnings, delta="issues", delta_color="off")
    with col3:
        st.metric("❌ Critical", result.checks_failed, delta="issues", delta_color="inverse")
    with col4:
        st.metric("⏱️ Response", f"{result.response_time:.2f}s", delta=f"{result.page_size_kb}KB")


def display_meta_tags(result):
    """Display meta tags analysis"""
    st.markdown("### 📋 Meta Tags Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Title Tag**")
        st.info(f"{result.title_status}")
        st.text(result.title[:80] if result.title else "Not found")
        
        tcol1, tcol2, tcol3 = st.columns(3)
        tcol1.metric("Length", f"{result.title_length}ch")
        tcol2.metric("Pixel Width", f"~{result.title_pixel_width}px")
        tcol3.metric("Has Numbers", "✅" if result.title_has_numbers else "❌")
        
        st.caption(f"Power Words: {'✅' if result.title_has_power_words else '❌'} | Keyword: {'✅' if result.title_has_keyword else '❌'}")
    
    with col2:
        st.markdown("**Meta Description**")
        st.info(f"{result.meta_description_status}")
        st.text(result.meta_description[:100] + "..." if result.meta_description and len(result.meta_description) > 100 else result.meta_description or "Not found")
        
        dcol1, dcol2, dcol3 = st.columns(3)
        dcol1.metric("Length", f"{result.meta_description_length}ch")
        dcol2.metric("Has CTA", "✅" if result.meta_description_has_cta else "❌")
        dcol3.metric("Keyword", "✅" if result.meta_description_has_keyword else "❌")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Canonical URL**")
        st.text(result.canonical_url[:50] + "..." if result.canonical_url and len(result.canonical_url) > 50 else result.canonical_url or "⚠️ Missing")
    with col2:
        st.markdown("**Robots Meta**")
        st.text(result.robots_meta or "Not specified")
        st.caption(f"Index: {'✅' if result.robots_index else '❌'} | Follow: {'✅' if result.robots_follow else '❌'}")
    with col3:
        st.markdown("**Meta Keywords**")
        st.text(f"{result.meta_keywords_count} keywords" if result.meta_keywords else "Not set")


def display_social_tags(result):
    """Display social media tags"""
    st.markdown("### 🌐 Social Media Tags")
    
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
            status = "✅" if value else "❌"
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
            status = "✅" if value else "❌"
            st.text(f"{status} {name}: {(value[:40] + '...' if value and len(str(value)) > 40 else value) or 'Missing'}")


def display_headings(result):
    """Display headings analysis"""
    st.markdown("### 📝 Heading Structure")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("H1", result.h1_count, delta=result.heading_structure_status)
    col2.metric("H2", result.h2_count)
    col3.metric("H3", result.h3_count)
    col4.metric("H4", result.h4_count)
    col5.metric("H5", result.h5_count)
    col6.metric("H6", result.h6_count)
    
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("Total", result.total_headings)
    mcol2.metric("Hierarchy", "✅ Valid" if result.heading_hierarchy_valid else "❌ Invalid")
    mcol3.metric("Empty", result.empty_headings)
    mcol4.metric("Duplicates", result.duplicate_headings)
    
    if result.h1_tags:
        with st.expander(f"View H1 Tags ({len(result.h1_tags)})"):
            for h1 in result.h1_tags:
                st.write(f"• {h1}")
    
    if result.h2_tags:
        with st.expander(f"View H2 Tags ({len(result.h2_tags)})"):
            for h2 in result.h2_tags[:10]:
                st.write(f"• {h2}")


def display_images(result):
    """Display images analysis"""
    st.markdown("### 🖼️ Images Analysis")
    
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
    st.markdown("### 🔗 Links Analysis")
    
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
        st.warning(f"⚠️ {result.links_without_noopener} links with target='_blank' missing rel='noopener' (security issue)")


def display_technical(result):
    """Display technical SEO"""
    st.markdown("### ⚙️ Technical SEO")
    
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
            st.write(f"{'✅' if value else '❌'} {name}")
    
    with col2:
        st.markdown("**Branding & PWA**")
        items = [
            ("Favicon", result.has_favicon),
            ("Apple Touch Icon", result.has_apple_touch_icon),
            ("Web Manifest", result.has_manifest),
            ("Theme Color", result.has_theme_color),
        ]
        for name, value in items:
            st.write(f"{'✅' if value else '❌'} {name}")
    
    with col3:
        st.markdown("**Schema Markup**")
        st.write(f"{'✅' if result.has_schema_markup else '❌'} Schema.org: {result.schema_count} schemas")
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
        st.write(f"Gzip: {'✅' if result.has_gzip else '❌'} ({result.content_encoding or 'None'})")
        st.write(f"Cache Headers: {'✅' if result.has_cache_headers else '❌'}")
    
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
            st.write(f"{'✅' if value else '❌'} {name}")


def display_content(result):
    """Display content analysis"""
    st.markdown("### 📖 Content Analysis")
    
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
            st.dataframe(df, use_container_width=True)


def display_mobile_ux(result):
    """Display mobile & UX"""
    st.markdown("### 📱 Mobile & UX")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mobile Friendly", "✅ Yes" if result.is_mobile_friendly else "❌ No")
    col2.metric("AMP Version", "✅ Yes" if result.has_amp_version else "❌ No")
    col3.metric("Touch Icons", result.touch_icons_count)
    col4.metric("UX Score", f"{result.ux_score}/100")


def display_i18n(result):
    """Display internationalization"""
    st.markdown("### 🌍 Internationalization")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Hreflang Tags", result.hreflang_count)
    col2.metric("X-Default", "✅" if result.has_x_default else "❌")
    col3.metric("HTML Lang", result.detected_language or "Not set")
    col4.metric("Score", f"{result.i18n_score}/100")


def display_ecommerce(result):
    """Display e-commerce & rich snippets"""
    st.markdown("### 🏪 E-Commerce & Rich Snippets")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Product Schema**")
        st.write(f"{'✅' if result.has_product_schema else '❌'} Product Schema")
        if result.has_product_schema:
            st.caption(f"Name: {result.product_name}")
            st.caption(f"Price: {result.product_price} {result.product_currency}")
    
    with col2:
        st.markdown("**Navigation**")
        st.write(f"{'✅' if result.has_breadcrumbs else '❌'} Breadcrumbs ({result.breadcrumb_levels} levels)")
        st.write(f"{'✅' if result.has_breadcrumb_schema else '❌'} Breadcrumb Schema")
    
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
            st.write(f"{'✅' if has_it else '❌'} {name}{extra}")


def display_accessibility(result):
    """Display accessibility"""
    st.markdown("### ♿ Accessibility")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.accessibility_score}/100")
    col2.metric("ARIA Labels", result.aria_labels_count)
    col3.metric("ARIA Roles", result.aria_roles_count)
    col4.metric("Form Issues", result.forms_without_labels)
    
    st.markdown("**Landmarks**")
    col1, col2, col3, col4 = st.columns(4)
    col1.write(f"{'✅' if result.has_skip_link else '❌'} Skip Link")
    col2.write(f"{'✅' if result.has_main_landmark else '❌'} Main")
    col3.write(f"{'✅' if result.has_nav_landmark else '❌'} Navigation")
    col4.write(f"{'✅' if result.has_footer_landmark else '❌'} Footer")


def display_performance(result):
    """Display performance hints"""
    st.markdown("### ⚡ Performance Hints")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.performance_hints_score}/100")
    col2.write(f"{'✅' if result.has_preload else '❌'} Preload")
    col3.write(f"{'✅' if result.has_preconnect else '❌'} Preconnect")
    col4.write(f"{'✅' if result.has_dns_prefetch else '❌'} DNS Prefetch")
    
    if result.preconnect_domains:
        with st.expander("Preconnect Domains"):
            for domain in result.preconnect_domains[:5]:
                st.write(f"• {domain}")


def display_issues(result):
    """Display all issues"""
    st.markdown("### 🚨 Issues & Recommendations")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        f"❌ Critical ({len(result.critical_issues)})",
        f"⚠️ Warnings ({len(result.warnings)})",
        f"💡 Recommendations ({len(result.recommendations)})",
        f"✅ Passed ({len(result.passed_checks)})"
    ])
    
    with tab1:
        if result.critical_issues:
            for issue in result.critical_issues:
                st.markdown(f'<div class="issue-critical">❌ {issue}</div>', unsafe_allow_html=True)
        else:
            st.success("No critical issues found! 🎉")
    
    with tab2:
        if result.warnings:
            for warning in result.warnings:
                st.markdown(f'<div class="issue-warning">⚠️ {warning}</div>', unsafe_allow_html=True)
        else:
            st.success("No warnings! 🎉")
    
    with tab3:
        if result.recommendations:
            for rec in result.recommendations:
                st.markdown(f'<div class="issue-recommendation">💡 {rec}</div>', unsafe_allow_html=True)
        else:
            st.info("No additional recommendations.")
    
    with tab4:
        if result.passed_checks:
            for check in result.passed_checks:
                st.markdown(f'<div class="issue-passed">✅ {check}</div>', unsafe_allow_html=True)


def display_export(result):
    """Display export options"""
    st.markdown("### 📥 Export Report")
    
    st.markdown("**📑 Professional PDF Report (Recommended)**")
    st.caption("Easy-to-understand report perfect for sharing with clients or team members")
    
    try:
        from pdf_report_generator import generate_pdf_report
        pdf_buffer = generate_pdf_report(result)
        st.download_button(
            label="📑 Download PDF Report (Easy to Read)",
            data=pdf_buffer,
            file_name=f"seo_report_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    except ImportError:
        st.warning("PDF generation requires 'reportlab'. Install with: pip install reportlab")
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
    
    st.markdown("---")
    st.markdown("**Other Export Formats**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        json_data = json.dumps(asdict(result), indent=2, default=str)
        st.download_button(
            label="📄 Download JSON",
            data=json_data,
            file_name=f"seo_audit_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Generate text report
        text_report = print_audit_report(result)
        st.download_button(
            label="📝 Download Text Report",
            data=text_report,
            file_name=f"seo_audit_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        # CSV summary
        summary_data = {
            "Metric": ["Score", "Grade", "Words", "Images", "Links", "Critical", "Warnings"],
            "Value": [result.score, result.grade, result.word_count, result.total_images, 
                     result.total_links, len(result.critical_issues), len(result.warnings)]
        }
        df = pd.DataFrame(summary_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📊 Download CSV Summary",
            data=csv,
            file_name=f"seo_summary_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )


def display_crawling_indexing(result):
    """Display crawling & indexing analysis"""
    st.markdown("### 📈 Crawling & Indexing")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.crawling_score}/100")
    col2.metric("Indexable", "✅ Yes" if result.is_indexable else "❌ No")
    col3.metric("URL Depth", result.url_depth)
    col4.metric("URL Length", f"{result.url_length} chars")
    
    st.markdown("**URL Analysis**")
    col1, col2, col3, col4 = st.columns(4)
    col1.write(f"{'✅' if result.url_structure_friendly else '❌'} SEO-Friendly URL")
    col2.write(f"{'✅' if not result.url_has_parameters else '⚠️'} {'No' if not result.url_has_parameters else 'Has'} Query Params")
    col3.write(f"{'✅' if not result.url_has_underscores else '⚠️'} {'No' if not result.url_has_underscores else 'Has'} Underscores")
    col4.write(f"{'✅' if result.url_length <= 75 else '⚠️'} URL Length {'OK' if result.url_length <= 75 else 'Long'}")
    
    st.markdown("**Indexability Signals**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"{'❌ Blocked' if result.robots_txt_blocks_url else '✅ Allowed'} by robots.txt")
        st.write(f"X-Robots-Tag: {result.x_robots_tag or 'Not set'}")
    with col2:
        st.write(f"{'⚠️ Redirect Chain' if result.has_redirect_chain else '✅ No'} Redirect Chain")
        if result.has_redirect_chain:
            st.caption(f"Chain length: {result.redirect_chain_length}")
    with col3:
        st.write(f"{'❌' if result.has_5xx_error else '✅'} {'5xx Error' if result.has_5xx_error else 'No Server Errors'}")
        st.write(f"{'✅' if result.has_noindex_system_pages else '⚠️'} System Pages Noindexed")


def display_content_quality(result):
    """Display content quality analysis"""
    st.markdown("### ✍️ Content Quality & E-E-A-T")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.content_quality_score}/100")
    col2.metric("Thin Content", "❌ Yes" if result.has_thin_content else "✅ No")
    col3.metric("Unique Content", "✅ Yes" if result.content_is_unique else "⚠️ Check")
    col4.metric("E-E-A-T Signals", "✅ Yes" if result.has_eeat_signals else "⚠️ Missing")
    
    st.markdown("**Trust & Authority Signals**")
    col1, col2, col3, col4 = st.columns(4)
    col1.write(f"{'✅' if result.has_privacy_policy else '❌'} Privacy Policy")
    col2.write(f"{'✅' if result.has_contact_page else '❌'} Contact Page")
    col3.write(f"{'✅' if result.has_about_page else '❌'} About Page")
    col4.write(f"{'✅' if result.has_author_info else '❌'} Author Info")
    
    if result.author_name:
        st.caption(f"Author: {result.author_name}")
    
    st.markdown("**Content Dates**")
    col1, col2 = st.columns(2)
    col1.write(f"Published: {result.publication_date or 'Not specified'}")
    col2.write(f"Modified: {result.modified_date or 'Not specified'}")
    
    st.markdown("**Content Issues**")
    col1, col2, col3, col4 = st.columns(4)
    col1.write(f"{'❌ Found' if result.has_hidden_text else '✅ None'} Hidden Text")
    col2.write(f"{'❌ Heavy' if result.has_heavy_above_fold_ads else '✅ OK'} Above-Fold Ads")
    col3.write(f"{'❌ Found' if result.content_in_iframes else '✅ None'} Content in iFrames")
    col4.write(f"{'❌ Found' if result.has_intrusive_interstitials else '✅ None'} Intrusive Popups")
    
    st.markdown("**Content Best Practices**")
    col1, col2 = st.columns(2)
    col1.write(f"{'✅' if result.has_clear_cta else '⚠️'} Clear Call-to-Action")
    col2.write(f"{'✅' if result.uses_semantic_html else '⚠️'} Semantic HTML")


def display_keyword_analysis(result):
    """Display keyword optimization analysis"""
    st.markdown("### 🗝️ Keyword Analysis")
    
    if result.target_keyword:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Score", f"{result.keyword_analysis_score}/100")
        col2.metric("Target Keyword", result.target_keyword)
        col3.metric("Occurrences", result.keyword_count_in_body)
        col4.metric("Density", f"{result.keyword_density_percent:.2f}%")
        
        st.markdown("**Keyword Placement**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"{'✅' if result.keyword_in_title else '❌'} In Title Tag")
            if result.keyword_in_title:
                pos_text = "Front" if result.keyword_in_title_position == 1 else "Middle/End"
                st.caption(f"Position: {pos_text}")
            st.write(f"{'✅' if result.title_starts_with_keyword else '⚠️'} Title Starts with Keyword")
        
        with col2:
            st.write(f"{'✅' if result.keyword_in_meta_desc else '❌'} In Meta Description")
            st.write(f"{'✅' if result.keyword_in_h1 else '❌'} In H1 Tag")
        
        with col3:
            st.write(f"{'✅' if result.keyword_in_h2 else '❌'} In H2 Tags")
            st.write(f"{'✅' if result.keyword_in_first_paragraph else '❌'} In First 100 Words")
        
        st.markdown("**Keyword Usage**")
        if result.keyword_overuse:
            st.warning("⚠️ Keyword may be overused (density > 3%). Consider reducing for natural content.")
        elif result.keyword_density_percent < 0.5:
            st.info("💡 Consider using keyword more naturally in content (current density < 0.5%)")
        else:
            st.success("✅ Keyword density appears optimal (0.5-3%)")
    else:
        st.info("💡 Enter a target keyword when running the audit to see keyword optimization analysis")


def display_mobile_advanced(result):
    """Display advanced mobile analysis"""
    st.markdown("### 📱 Advanced Mobile Optimization")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.mobile_advanced_score}/100")
    col2.metric("Page Weight", f"{result.mobile_page_weight_kb:.0f} KB")
    col3.metric("Heavy Page", "❌ Yes" if result.mobile_page_heavy else "✅ No")
    col4.metric("Mobile Friendly", "✅ Yes" if result.is_mobile_friendly else "❌ No")
    
    st.markdown("**Mobile Usability**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"{'✅' if result.tap_targets_sized_correctly else '❌'} Tap Targets Sized")
        if result.tap_target_issues > 0:
            st.caption(f"Issues: {result.tap_target_issues} elements")
    
    with col2:
        st.write(f"{'✅' if result.font_sizes_readable else '❌'} Readable Font Sizes")
        if result.small_font_elements > 0:
            st.caption(f"Small fonts: {result.small_font_elements}")
    
    with col3:
        st.write(f"{'✅' if result.content_width_fits_viewport else '⚠️'} Content Fits Viewport")
    
    st.markdown("**Mobile Navigation & Images**")
    col1, col2, col3 = st.columns(3)
    col1.write(f"{'✅' if result.mobile_navigation_friendly else '⚠️'} Mobile-Friendly Navigation")
    col2.write(f"{'✅' if result.thumb_friendly_navigation else '⚠️'} Thumb-Friendly Nav")
    col3.write(f"{'✅' if result.has_responsive_images else '⚠️'} Responsive Images")
    
    st.markdown("**Mobile-Desktop Parity**")
    col1, col2, col3 = st.columns(3)
    col1.write(f"{'✅' if result.mobile_desktop_parity else '⚠️'} Content Parity")
    col2.write(f"{'✅' if result.mobile_meta_parity else '⚠️'} Meta Tags Parity")
    col3.write(f"{'✅' if result.mobile_directives_parity else '⚠️'} Directives Parity")
    col4 = st.columns(1)[0]
    col4.write(f"{'✅' if result.favicon_in_mobile_serps else '⚠️'} Favicon for Mobile SERPs")


def display_page_elements(result):
    """Display page elements analysis"""
    st.markdown("### 💡 Page Elements Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{result.page_elements_score}/100")
    col2.metric("Multiple H1s", "❌ Yes" if result.has_multiple_h1 else "✅ No")
    col3.metric("Title-Content Match", "✅ Yes" if result.title_matches_content else "⚠️ Check")
    col4.metric("Unique Meta Desc", "✅ Yes" if result.meta_desc_is_unique else "⚠️ Check")
    
    st.markdown("**Content Structure**")
    col1, col2, col3 = st.columns(3)
    col1.write(f"{'✅' if result.primary_content_clear else '⚠️'} Primary Content Clear")
    col2.write(f"{'✅' if result.supplementary_content_marked else '⚠️'} Supplementary Content Marked")
    col3.write(f"{'✅' if result.meta_desc_compelling else '⚠️'} Compelling Meta Description")
    
    st.markdown("**Visual & Accessibility**")
    col1, col2 = st.columns(2)
    col1.write(f"{'✅' if result.text_contrast_sufficient else '⚠️'} Sufficient Text Contrast")
    col2.write(f"{'✅' if result.links_distinguishable else '⚠️'} Links Distinguishable")


def main():
    # Sidebar
    with st.sidebar:
        st.title("🔍 SEO Audit Tool")
        st.markdown("**Version 3.0 - 300+ Parameters**")
        st.markdown("---")
        
        st.markdown("""
        **Comprehensive Analysis:**
        - 📋 Meta Tags (20+ checks)
        - 🌐 Social Tags (25+ checks)
        - 📝 Headings (20+ checks)
        - 🖼️ Images (25+ checks)
        - 🔗 Links (30+ checks)
        - ⚙️ Technical (40+ checks)
        - 📖 Content (35+ checks)
        - 📱 Mobile/UX (15+ checks)
        - 🌍 i18n (10+ checks)
        - 🏪 E-commerce (15+ checks)
        - ♿ Accessibility (15+ checks)
        - ⚡ Performance (10+ checks)
        - 📈 Crawling & Indexing (15+ checks)
        - ✍️ Content Quality/E-E-A-T (20+ checks)
        - 🗝️ Keyword Analysis (15+ checks)
        - 📱 Advanced Mobile (20+ checks)
        - 💡 Page Elements (15+ checks)
        
        ---
        
        **Plerdy Checklist Compliant**
        
        ---
        
        **Created by:**
        [Muntasir Islam](https://muntasir-islam.github.io)
        
        💼 SEO Specialist  
        🌐 Web Strategist
        """)
    
    # Main content
    st.title("🔍 Advanced SEO Audit Tool")
    st.markdown("Enterprise-grade SEO analysis with **300+ parameters** - Plerdy Checklist Compliant. Enter a URL below to start.")
    
    # Input row
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input(
            "Website URL",
            placeholder="example.com or https://example.com",
            help="Enter the full URL of the page you want to audit"
        )
    
    with col2:
        keyword = st.text_input(
            "Target Keyword (optional)",
            placeholder="seo audit",
            help="Enter your target keyword to check optimization"
        )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        audit_button = st.button("🚀 Run Advanced SEO Audit", use_container_width=True)
    
    if audit_button and url:
        with st.spinner("🔍 Analyzing 300+ SEO parameters... This may take 10-20 seconds."):
            progress = st.progress(0)
            status = st.empty()
            
            status.text("Initializing audit...")
            progress.progress(10)
            
            auditor = AdvancedSEOAuditor(url, target_keyword=keyword if keyword else None)
            
            status.text("Fetching page content...")
            progress.progress(20)
            
            result = auditor.run_audit()
            
            progress.progress(100)
            status.empty()
            
            if result:
                st.success(f"✅ Audit complete for {result.url}")
                st.balloons()
                
                # Display all sections
                display_score_card(result)
                display_quick_stats(result)
                
                st.divider()
                
                # Use tabs for organization - 7 tabs now
                tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                    "📋 Meta & Social",
                    "📝 Content & Structure",
                    "⚙️ Technical",
                    "📱 Mobile & A11y",
                    "📈 Crawling & Indexing",
                    "🗝️ Keywords & Quality",
                    "🚨 Issues"
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
                
            else:
                st.error("❌ Failed to audit the website. Please check the URL and try again.")
                st.info("💡 **Tips:**\n- Make sure the URL is accessible\n- Try with 'https://' prefix\n- Some websites block automated requests")
    
    elif audit_button and not url:
        st.warning("⚠️ Please enter a URL to audit")
    
    # Footer
    st.markdown("---")
    
    # Social sharing and GitHub
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <a href="https://github.com/muntasir-islam/seo_audit_tool" target="_blank" style="text-decoration: none;">
                ⭐ Star on GitHub
            </a>
            &nbsp;|&nbsp;
            <a href="https://twitter.com/intent/tweet?text=Check%20out%20this%20free%20SEO%20Audit%20Tool%20with%20300%2B%20parameters!&url=https://seo-audit-tool.streamlit.app" target="_blank" style="text-decoration: none;">
                🐦 Share on Twitter
            </a>
            &nbsp;|&nbsp;
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://seo-audit-tool.streamlit.app" target="_blank" style="text-decoration: none;">
                💼 Share on LinkedIn
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 20px;">
        <p>Made with ❤️ by <a href="https://muntasir-islam.github.io" target="_blank" style="color: #6366f1;">Muntasir Islam</a></p>
        <p>© 2026 | Advanced SEO Audit Tool v3.0 - 300+ Parameters</p>
        <p style="font-size: 0.8rem;">🔒 No data stored • 🚀 Powered by Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
