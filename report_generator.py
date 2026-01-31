"""
Advanced SEO Audit Report Generator - 200+ Parameters
Generates professional HTML reports from SEO audit results
Author: Muntasir Islam
Version: 2.0
"""

from dataclasses import asdict
from datetime import datetime
from typing import Optional
import json
from seo_auditor import SEOAuditResult


class AdvancedReportGenerator:
    """Generate comprehensive HTML reports for SEO audits"""
    
    def __init__(self, result: SEOAuditResult):
        self.result = result
        
    def _get_grade_color(self, score: int) -> str:
        """Get color based on score"""
        if score >= 80:
            return "#22c55e"  # Green
        elif score >= 60:
            return "#eab308"  # Yellow
        elif score >= 40:
            return "#f97316"  # Orange
        else:
            return "#ef4444"  # Red
    
    def _get_status_icon(self, value: bool) -> str:
        """Get icon for boolean status"""
        return "✅" if value else "❌"
    
    def _get_status_class(self, value: bool) -> str:
        """Get CSS class for status"""
        return "status-good" if value else "status-bad"
    
    def generate_html_report(self) -> str:
        """Generate comprehensive HTML report"""
        r = self.result
        grade_color = self._get_grade_color(r.score)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Audit Report - {r.url}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            color: #e2e8f0;
            line-height: 1.6;
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{ font-size: 2rem; margin-bottom: 10px; color: #f1f5f9; }}
        .header p {{ color: #94a3b8; }}
        .score-circle {{
            width: 200px;
            height: 200px;
            border-radius: 50%;
            border: 10px solid {grade_color};
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 30px auto;
            background: rgba(0,0,0,0.3);
        }}
        .score-number {{ font-size: 4rem; font-weight: bold; color: {grade_color}; }}
        .score-grade {{ font-size: 1.5rem; color: {grade_color}; }}
        .stats-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: #1e293b;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-value {{ font-size: 2rem; font-weight: bold; color: #f1f5f9; }}
        .stat-label {{ color: #94a3b8; font-size: 0.9rem; }}
        .section {{
            background: #1e293b;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }}
        .section-title {{
            font-size: 1.5rem;
            color: #f1f5f9;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #334155;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .metric-item {{
            background: #0f172a;
            padding: 15px;
            border-radius: 8px;
        }}
        .metric-label {{ color: #94a3b8; font-size: 0.85rem; }}
        .metric-value {{ font-size: 1.2rem; font-weight: 600; color: #f1f5f9; }}
        .status-good {{ color: #22c55e; }}
        .status-warning {{ color: #eab308; }}
        .status-bad {{ color: #ef4444; }}
        .issue-list {{ list-style: none; }}
        .issue-item {{
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 8px;
        }}
        .issue-critical {{
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #ef4444;
        }}
        .issue-warning {{
            background: rgba(234, 179, 8, 0.1);
            border-left: 4px solid #eab308;
        }}
        .issue-recommendation {{
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid #3b82f6;
        }}
        .issue-passed {{
            background: rgba(34, 197, 94, 0.1);
            border-left: 4px solid #22c55e;
        }}
        .two-column {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        @media (max-width: 768px) {{
            .two-column {{ grid-template-columns: 1fr; }}
        }}
        .tag {{ 
            display: inline-block; 
            padding: 2px 8px; 
            border-radius: 4px; 
            font-size: 0.85rem; 
            margin: 2px;
        }}
        .tag-good {{ background: rgba(34, 197, 94, 0.2); color: #22c55e; }}
        .tag-bad {{ background: rgba(239, 68, 68, 0.2); color: #ef4444; }}
        .footer {{
            text-align: center;
            padding: 30px;
            color: #64748b;
            margin-top: 40px;
        }}
        .progress-bar {{
            background: #0f172a;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #334155;
        }}
        th {{ background: #0f172a; color: #f1f5f9; }}
        .collapsible {{ cursor: pointer; }}
        .collapsible:after {{ content: ' ▼'; font-size: 0.8rem; }}
        .print-button {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1rem;
        }}
        @media print {{
            .print-button {{ display: none; }}
            body {{ background: white; color: black; }}
            .section {{ break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Advanced SEO Audit Report</h1>
            <p><strong>URL:</strong> {r.url}</p>
            <p><strong>Audited:</strong> {r.audit_date}</p>
            <p><strong>Parameters Checked:</strong> 200+</p>
            
            <div class="score-circle">
                <span class="score-number">{r.score}</span>
                <span class="score-grade">Grade: {r.grade}</span>
            </div>
        </div>
        
        <!-- Quick Stats -->
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-value status-good">{r.checks_passed}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value status-warning">{r.checks_warnings}</div>
                <div class="stat-label">Warnings</div>
            </div>
            <div class="stat-card">
                <div class="stat-value status-bad">{r.checks_failed}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{r.response_time:.2f}s</div>
                <div class="stat-label">Response Time</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{r.page_size_kb}KB</div>
                <div class="stat-label">Page Size</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{r.word_count}</div>
                <div class="stat-label">Words</div>
            </div>
        </div>
        
        <!-- Category Scores -->
        <div class="section">
            <h2 class="section-title">📊 Category Scores</h2>
            {self._generate_category_scores()}
        </div>
        
        <!-- Meta Tags -->
        <div class="section">
            <h2 class="section-title">📋 Meta Tags Analysis</h2>
            <div class="two-column">
                <div>
                    <h3>Title Tag</h3>
                    <p class="{self._get_status_class(30 <= r.title_length <= 60)}">{r.title_status}</p>
                    <div class="metric-item">
                        <div class="metric-label">Title</div>
                        <div class="metric-value">{r.title or 'Not found'}</div>
                    </div>
                    <div class="metric-grid">
                        <div class="metric-item">
                            <div class="metric-label">Length</div>
                            <div class="metric-value">{r.title_length} characters</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Pixel Width</div>
                            <div class="metric-value">~{r.title_pixel_width}px</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Has Numbers</div>
                            <div class="metric-value">{self._get_status_icon(r.title_has_numbers)}</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Has Power Words</div>
                            <div class="metric-value">{self._get_status_icon(r.title_has_power_words)}</div>
                        </div>
                    </div>
                </div>
                <div>
                    <h3>Meta Description</h3>
                    <p class="{self._get_status_class(120 <= r.meta_description_length <= 160)}">{r.meta_description_status}</p>
                    <div class="metric-item">
                        <div class="metric-label">Description</div>
                        <div class="metric-value">{(r.meta_description[:150] + '...') if r.meta_description and len(r.meta_description) > 150 else r.meta_description or 'Not found'}</div>
                    </div>
                    <div class="metric-grid">
                        <div class="metric-item">
                            <div class="metric-label">Length</div>
                            <div class="metric-value">{r.meta_description_length} characters</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Has CTA</div>
                            <div class="metric-value">{self._get_status_icon(r.meta_description_has_cta)}</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Has Keyword</div>
                            <div class="metric-value">{self._get_status_icon(r.meta_description_has_keyword)}</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-label">Unique</div>
                            <div class="metric-value">{self._get_status_icon(r.meta_description_unique)}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <h3 style="margin-top: 20px;">Other Meta Tags</h3>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Canonical URL</div>
                    <div class="metric-value">{r.canonical_url or '⚠️ Missing'}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Robots Meta</div>
                    <div class="metric-value">{r.robots_meta or 'Not specified'}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Index</div>
                    <div class="metric-value">{self._get_status_icon(r.robots_index)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Follow</div>
                    <div class="metric-value">{self._get_status_icon(r.robots_follow)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Meta Keywords</div>
                    <div class="metric-value">{r.meta_keywords_count} keywords</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Author</div>
                    <div class="metric-value">{r.meta_author or 'Not set'}</div>
                </div>
            </div>
        </div>
        
        <!-- Social Media Tags -->
        <div class="section">
            <h2 class="section-title">🌐 Social Media Tags</h2>
            <div class="two-column">
                <div>
                    <h3>Open Graph Tags ({r.og_score}% Complete)</h3>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {r.og_score}%; background: {self._get_grade_color(r.og_score)};"></div>
                    </div>
                    <table>
                        <tr><td>og:title</td><td class="{self._get_status_class(bool(r.og_title))}">{r.og_title or '❌ Missing'}</td></tr>
                        <tr><td>og:description</td><td class="{self._get_status_class(bool(r.og_description))}">{(r.og_description[:50] + '...') if r.og_description and len(r.og_description) > 50 else r.og_description or '❌ Missing'}</td></tr>
                        <tr><td>og:image</td><td class="{self._get_status_class(bool(r.og_image))}">{self._get_status_icon(bool(r.og_image))} {'Set' if r.og_image else 'Missing'}</td></tr>
                        <tr><td>og:url</td><td class="{self._get_status_class(bool(r.og_url))}">{self._get_status_icon(bool(r.og_url))} {'Set' if r.og_url else 'Missing'}</td></tr>
                        <tr><td>og:type</td><td class="{self._get_status_class(bool(r.og_type))}">{r.og_type or '❌ Missing'}</td></tr>
                        <tr><td>og:site_name</td><td class="{self._get_status_class(bool(r.og_site_name))}">{r.og_site_name or '❌ Missing'}</td></tr>
                        <tr><td>og:locale</td><td>{r.og_locale or 'Not set'}</td></tr>
                    </table>
                </div>
                <div>
                    <h3>Twitter Cards ({r.twitter_score}% Complete)</h3>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {r.twitter_score}%; background: {self._get_grade_color(r.twitter_score)};"></div>
                    </div>
                    <table>
                        <tr><td>twitter:card</td><td class="{self._get_status_class(bool(r.twitter_card))}">{r.twitter_card or '❌ Missing'}</td></tr>
                        <tr><td>twitter:title</td><td class="{self._get_status_class(bool(r.twitter_title))}">{(r.twitter_title[:40] + '...') if r.twitter_title and len(r.twitter_title) > 40 else r.twitter_title or '❌ Missing'}</td></tr>
                        <tr><td>twitter:description</td><td class="{self._get_status_class(bool(r.twitter_description))}">{self._get_status_icon(bool(r.twitter_description))} {'Set' if r.twitter_description else 'Missing'}</td></tr>
                        <tr><td>twitter:image</td><td class="{self._get_status_class(bool(r.twitter_image))}">{self._get_status_icon(bool(r.twitter_image))} {'Set' if r.twitter_image else 'Missing'}</td></tr>
                        <tr><td>twitter:site</td><td>{r.twitter_site or 'Not set'}</td></tr>
                        <tr><td>twitter:creator</td><td>{r.twitter_creator or 'Not set'}</td></tr>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Headings Structure -->
        <div class="section">
            <h2 class="section-title">📝 Heading Structure</h2>
            <p class="{self._get_status_class(r.heading_hierarchy_valid)}">{r.heading_structure_status}</p>
            
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">H1 Tags</div>
                    <div class="metric-value {self._get_status_class(r.h1_count == 1)}">{r.h1_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">H2 Tags</div>
                    <div class="metric-value">{r.h2_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">H3 Tags</div>
                    <div class="metric-value">{r.h3_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">H4 Tags</div>
                    <div class="metric-value">{r.h4_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">H5 Tags</div>
                    <div class="metric-value">{r.h5_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">H6 Tags</div>
                    <div class="metric-value">{r.h6_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Total Headings</div>
                    <div class="metric-value">{r.total_headings}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Empty Headings</div>
                    <div class="metric-value {self._get_status_class(r.empty_headings == 0)}">{r.empty_headings}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Duplicate Headings</div>
                    <div class="metric-value">{r.duplicate_headings}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Hierarchy Valid</div>
                    <div class="metric-value">{self._get_status_icon(r.heading_hierarchy_valid)}</div>
                </div>
            </div>
            
            {self._generate_h1_list()}
        </div>
        
        <!-- Images Analysis -->
        <div class="section">
            <h2 class="section-title">🖼️ Images Analysis (Score: {r.images_score}/100)</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {r.images_score}%; background: {self._get_grade_color(r.images_score)};"></div>
            </div>
            
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Total Images</div>
                    <div class="metric-value">{r.total_images}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Missing Alt</div>
                    <div class="metric-value {self._get_status_class(r.images_without_alt == 0)}">{r.images_without_alt}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Empty Alt</div>
                    <div class="metric-value">{r.images_with_empty_alt}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Lazy Loading</div>
                    <div class="metric-value">{r.images_with_lazy_loading}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">With Srcset</div>
                    <div class="metric-value">{r.images_with_srcset}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">In Picture</div>
                    <div class="metric-value">{r.images_in_picture}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">WebP Format</div>
                    <div class="metric-value">{r.images_webp}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">PNG</div>
                    <div class="metric-value">{r.images_png}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">JPG/JPEG</div>
                    <div class="metric-value">{r.images_jpg}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">SVG</div>
                    <div class="metric-value">{r.images_svg}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">GIF</div>
                    <div class="metric-value">{r.images_gif}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Avg Alt Length</div>
                    <div class="metric-value">{r.avg_alt_length:.1f} chars</div>
                </div>
            </div>
        </div>
        
        <!-- Links Analysis -->
        <div class="section">
            <h2 class="section-title">🔗 Links Analysis (Score: {r.links_score}/100)</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {r.links_score}%; background: {self._get_grade_color(r.links_score)};"></div>
            </div>
            
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Total Links</div>
                    <div class="metric-value">{r.total_links}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Internal Links</div>
                    <div class="metric-value">{r.internal_links} (Unique: {r.unique_internal_links})</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">External Links</div>
                    <div class="metric-value">{r.external_links} (Unique: {r.unique_external_links})</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">DoFollow</div>
                    <div class="metric-value">{r.dofollow_links}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">NoFollow</div>
                    <div class="metric-value">{r.nofollow_links}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Sponsored</div>
                    <div class="metric-value">{r.sponsored_links}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">UGC Links</div>
                    <div class="metric-value">{r.ugc_links}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Text Links</div>
                    <div class="metric-value">{r.text_links}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Image Links</div>
                    <div class="metric-value">{r.image_links}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Empty Anchor</div>
                    <div class="metric-value {self._get_status_class(r.empty_anchor_links == 0)}">{r.empty_anchor_links}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">JS Links</div>
                    <div class="metric-value">{r.javascript_links}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Missing Noopener</div>
                    <div class="metric-value {self._get_status_class(r.links_without_noopener == 0)}">{r.links_without_noopener}</div>
                </div>
            </div>
        </div>
        
        <!-- Technical SEO -->
        <div class="section">
            <h2 class="section-title">⚙️ Technical SEO (Score: {r.technical_seo_score}/100)</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {r.technical_seo_score}%; background: {self._get_grade_color(r.technical_seo_score)};"></div>
            </div>
            
            <h3>Core Technical</h3>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">HTTPS/SSL</div>
                    <div class="metric-value">{self._get_status_icon(r.has_ssl)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Viewport Meta</div>
                    <div class="metric-value">{self._get_status_icon(r.has_viewport)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Charset</div>
                    <div class="metric-value">{self._get_status_icon(r.has_charset)} {r.charset or ''}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">HTML Lang</div>
                    <div class="metric-value">{self._get_status_icon(bool(r.html_lang))} {r.html_lang or 'Missing'}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Doctype</div>
                    <div class="metric-value">{self._get_status_icon(r.has_doctype)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">HTTP Status</div>
                    <div class="metric-value {self._get_status_class(r.http_status == 200)}">{r.http_status}</div>
                </div>
            </div>
            
            <h3 style="margin-top: 20px;">Branding & PWA</h3>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Favicon</div>
                    <div class="metric-value">{self._get_status_icon(r.has_favicon)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Apple Touch Icon</div>
                    <div class="metric-value">{self._get_status_icon(r.has_apple_touch_icon)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Web Manifest</div>
                    <div class="metric-value">{self._get_status_icon(r.has_manifest)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Theme Color</div>
                    <div class="metric-value">{self._get_status_icon(r.has_theme_color)} {r.theme_color or ''}</div>
                </div>
            </div>
            
            <h3 style="margin-top: 20px;">Schema Markup</h3>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Schema.org</div>
                    <div class="metric-value">{self._get_status_icon(r.has_schema_markup)} {r.schema_count} schemas</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Schema Types</div>
                    <div class="metric-value">{', '.join(r.schema_types[:3]) if r.schema_types else 'None'}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Microdata</div>
                    <div class="metric-value">{r.microdata_items} items</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">RDFa</div>
                    <div class="metric-value">{r.rdfa_items} items</div>
                </div>
            </div>
            
            <h3 style="margin-top: 20px;">Resources</h3>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">CSS Files</div>
                    <div class="metric-value">{r.total_css_files}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">JS Files</div>
                    <div class="metric-value">{r.total_js_files}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Render-Block CSS</div>
                    <div class="metric-value">{r.render_blocking_css}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Render-Block JS</div>
                    <div class="metric-value">{r.render_blocking_js}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Async JS</div>
                    <div class="metric-value">{r.async_js}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Defer JS</div>
                    <div class="metric-value">{r.defer_js}</div>
                </div>
            </div>
            
            <h3 style="margin-top: 20px;">Security Headers (Score: {r.security_headers_score}%)</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {r.security_headers_score}%; background: {self._get_grade_color(r.security_headers_score)};"></div>
            </div>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">HSTS</div>
                    <div class="metric-value">{self._get_status_icon(r.has_hsts)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">XSS Protection</div>
                    <div class="metric-value">{self._get_status_icon(r.has_xss_protection)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Content-Type-Options</div>
                    <div class="metric-value">{self._get_status_icon(r.has_content_type_options)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">X-Frame-Options</div>
                    <div class="metric-value">{self._get_status_icon(r.has_frame_options)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">CSP</div>
                    <div class="metric-value">{self._get_status_icon(r.has_csp)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Referrer Policy</div>
                    <div class="metric-value">{self._get_status_icon(r.has_referrer_policy)}</div>
                </div>
            </div>
        </div>
        
        <!-- Content Analysis -->
        <div class="section">
            <h2 class="section-title">📖 Content Analysis (Score: {r.content_score}/100)</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {r.content_score}%; background: {self._get_grade_color(r.content_score)};"></div>
            </div>
            
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Word Count</div>
                    <div class="metric-value">{r.word_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Sentences</div>
                    <div class="metric-value">{r.sentence_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Paragraphs</div>
                    <div class="metric-value">{r.paragraph_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Avg Sentence Length</div>
                    <div class="metric-value">{r.avg_sentence_length} words</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Unique Words</div>
                    <div class="metric-value">{r.unique_words}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Lexical Density</div>
                    <div class="metric-value">{r.lexical_density}%</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Text/HTML Ratio</div>
                    <div class="metric-value">{r.text_html_ratio}%</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Flesch Reading Ease</div>
                    <div class="metric-value">{r.flesch_reading_ease}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Grade Level</div>
                    <div class="metric-value">{r.flesch_kincaid_grade}</div>
                </div>
            </div>
            
            <h3 style="margin-top: 20px;">Content Elements</h3>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Unordered Lists</div>
                    <div class="metric-value">{r.unordered_lists}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Ordered Lists</div>
                    <div class="metric-value">{r.ordered_lists}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Tables</div>
                    <div class="metric-value">{r.table_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Blockquotes</div>
                    <div class="metric-value">{r.blockquote_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Code Blocks</div>
                    <div class="metric-value">{r.code_block_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Bold Text</div>
                    <div class="metric-value">{r.bold_text_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Italic Text</div>
                    <div class="metric-value">{r.italic_text_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Videos</div>
                    <div class="metric-value">{r.video_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Iframes</div>
                    <div class="metric-value">{r.iframe_count}</div>
                </div>
            </div>
            
            {self._generate_keywords_table()}
        </div>
        
        <!-- Mobile & UX -->
        <div class="section">
            <h2 class="section-title">📱 Mobile & UX (Score: {r.ux_score}/100)</h2>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Mobile Friendly</div>
                    <div class="metric-value">{self._get_status_icon(r.is_mobile_friendly)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Viewport Configured</div>
                    <div class="metric-value">{self._get_status_icon(r.viewport_configured)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">AMP Version</div>
                    <div class="metric-value">{self._get_status_icon(r.has_amp_version)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Touch Icons</div>
                    <div class="metric-value">{r.touch_icons_count}</div>
                </div>
            </div>
        </div>
        
        <!-- Internationalization -->
        <div class="section">
            <h2 class="section-title">🌍 Internationalization (Score: {r.i18n_score}/100)</h2>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Hreflang Tags</div>
                    <div class="metric-value">{r.hreflang_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">X-Default</div>
                    <div class="metric-value">{self._get_status_icon(r.has_x_default)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Content Language</div>
                    <div class="metric-value">{r.content_language or 'Not set'}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Detected Language</div>
                    <div class="metric-value">{r.detected_language or 'Unknown'}</div>
                </div>
            </div>
        </div>
        
        <!-- E-Commerce & Rich Snippets -->
        <div class="section">
            <h2 class="section-title">🏪 E-Commerce & Rich Snippets</h2>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Product Schema</div>
                    <div class="metric-value">{self._get_status_icon(r.has_product_schema)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Breadcrumbs</div>
                    <div class="metric-value">{self._get_status_icon(r.has_breadcrumbs)} ({r.breadcrumb_levels} levels)</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Breadcrumb Schema</div>
                    <div class="metric-value">{self._get_status_icon(r.has_breadcrumb_schema)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">FAQ Schema</div>
                    <div class="metric-value">{self._get_status_icon(r.has_faq_schema)} ({r.faq_questions_count} questions)</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">HowTo Schema</div>
                    <div class="metric-value">{self._get_status_icon(r.has_howto_schema)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Recipe Schema</div>
                    <div class="metric-value">{self._get_status_icon(r.has_recipe_schema)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Event Schema</div>
                    <div class="metric-value">{self._get_status_icon(r.has_event_schema)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">LocalBusiness Schema</div>
                    <div class="metric-value">{self._get_status_icon(r.has_local_business_schema)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Reviews Schema</div>
                    <div class="metric-value">{self._get_status_icon(r.has_reviews_schema)}</div>
                </div>
            </div>
        </div>
        
        <!-- Accessibility -->
        <div class="section">
            <h2 class="section-title">♿ Accessibility (Score: {r.accessibility_score}/100)</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {r.accessibility_score}%; background: {self._get_grade_color(r.accessibility_score)};"></div>
            </div>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">ARIA Labels</div>
                    <div class="metric-value">{r.aria_labels_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">ARIA Roles</div>
                    <div class="metric-value">{r.aria_roles_count}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Skip Link</div>
                    <div class="metric-value">{self._get_status_icon(r.has_skip_link)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Main Landmark</div>
                    <div class="metric-value">{self._get_status_icon(r.has_main_landmark)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Nav Landmark</div>
                    <div class="metric-value">{self._get_status_icon(r.has_nav_landmark)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Footer Landmark</div>
                    <div class="metric-value">{self._get_status_icon(r.has_footer_landmark)}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Forms Without Labels</div>
                    <div class="metric-value {self._get_status_class(r.forms_without_labels == 0)}">{r.forms_without_labels}</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Tabindex Issues</div>
                    <div class="metric-value">{r.tabindex_issues}</div>
                </div>
            </div>
        </div>
        
        <!-- Performance Hints -->
        <div class="section">
            <h2 class="section-title">⚡ Performance Hints (Score: {r.performance_hints_score}/100)</h2>
            <div class="metric-grid">
                <div class="metric-item">
                    <div class="metric-label">Preload</div>
                    <div class="metric-value">{self._get_status_icon(r.has_preload)} ({r.preload_count} resources)</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Preconnect</div>
                    <div class="metric-value">{self._get_status_icon(r.has_preconnect)} ({r.preconnect_count} domains)</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">DNS Prefetch</div>
                    <div class="metric-value">{self._get_status_icon(r.has_dns_prefetch)} ({r.dns_prefetch_count} domains)</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Prefetch</div>
                    <div class="metric-value">{self._get_status_icon(r.has_prefetch)} ({r.prefetch_count} resources)</div>
                </div>
            </div>
        </div>
        
        <!-- Issues -->
        <div class="section">
            <h2 class="section-title">🚨 Issues & Recommendations</h2>
            
            <h3>❌ Critical Issues ({len(r.critical_issues)})</h3>
            <ul class="issue-list">
                {self._generate_issue_list(r.critical_issues, 'critical')}
            </ul>
            
            <h3 style="margin-top: 20px;">⚠️ Warnings ({len(r.warnings)})</h3>
            <ul class="issue-list">
                {self._generate_issue_list(r.warnings, 'warning')}
            </ul>
            
            <h3 style="margin-top: 20px;">💡 Recommendations ({len(r.recommendations)})</h3>
            <ul class="issue-list">
                {self._generate_issue_list(r.recommendations, 'recommendation')}
            </ul>
            
            <h3 style="margin-top: 20px;">✅ Passed Checks ({len(r.passed_checks)})</h3>
            <ul class="issue-list">
                {self._generate_issue_list(r.passed_checks, 'passed')}
            </ul>
        </div>
        
        <div class="footer">
            <p>Generated by <strong>Advanced SEO Audit Tool v2.0</strong></p>
            <p>Created by <a href="https://muntasir-islam.github.io" style="color: #6366f1;">Muntasir Islam</a></p>
            <p>© 2026 | 200+ SEO Parameters Analyzed</p>
        </div>
    </div>
    
    <button class="print-button" onclick="window.print()">🖨️ Print Report</button>
</body>
</html>
"""
        return html
    
    def _generate_category_scores(self) -> str:
        """Generate category scores visualization"""
        r = self.result
        categories = [
            ("Meta Tags", r.meta_tags_score),
            ("Open Graph", r.og_score),
            ("Twitter Cards", r.twitter_score),
            ("Headings", r.headings_score),
            ("Images", r.images_score),
            ("Links", r.links_score),
            ("Technical SEO", r.technical_seo_score),
            ("Content", r.content_score),
            ("Mobile/UX", r.ux_score),
            ("i18n", r.i18n_score),
            ("E-commerce", r.ecommerce_score),
            ("Accessibility", r.accessibility_score),
            ("Performance", r.performance_hints_score),
            ("Security", r.security_headers_score),
        ]
        
        html = '<div class="metric-grid">'
        for name, score in categories:
            color = self._get_grade_color(score)
            html += f'''
            <div class="metric-item">
                <div class="metric-label">{name}</div>
                <div class="metric-value" style="color: {color};">{score}/100</div>
                <div class="progress-bar" style="height: 8px; margin-top: 5px;">
                    <div class="progress-fill" style="width: {score}%; background: {color};"></div>
                </div>
            </div>
            '''
        html += '</div>'
        return html
    
    def _generate_h1_list(self) -> str:
        """Generate H1 tags list"""
        if not self.result.h1_tags:
            return ""
        
        html = '<h3 style="margin-top: 20px;">H1 Tags</h3><ul>'
        for h1 in self.result.h1_tags:
            html += f'<li>{h1}</li>'
        html += '</ul>'
        return html
    
    def _generate_keywords_table(self) -> str:
        """Generate top keywords table"""
        if not self.result.top_keywords:
            return ""
        
        html = '''
        <h3 style="margin-top: 20px;">Top Keywords</h3>
        <table>
            <tr><th>Keyword</th><th>Count</th></tr>
        '''
        for keyword, count in self.result.top_keywords[:15]:
            html += f'<tr><td>{keyword}</td><td>{count}</td></tr>'
        html += '</table>'
        return html
    
    def _generate_issue_list(self, issues: list, issue_type: str) -> str:
        """Generate issue list HTML"""
        if not issues:
            if issue_type == 'critical':
                return '<li class="issue-item issue-passed">No critical issues found! 🎉</li>'
            elif issue_type == 'warning':
                return '<li class="issue-item issue-passed">No warnings! 🎉</li>'
            elif issue_type == 'passed':
                return ''
            else:
                return '<li class="issue-item issue-recommendation">No additional recommendations.</li>'
        
        html = ''
        for issue in issues[:50]:  # Limit to 50 items
            html += f'<li class="issue-item issue-{issue_type}">{issue}</li>'
        return html
    
    def save_html_report(self, filepath: str):
        """Save HTML report to file"""
        html = self.generate_html_report()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Report saved to: {filepath}")
    
    def generate_json_report(self) -> str:
        """Generate JSON report"""
        return json.dumps(asdict(self.result), indent=2, default=str)
    
    def save_json_report(self, filepath: str):
        """Save JSON report to file"""
        json_data = self.generate_json_report()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(json_data)
        print(f"JSON report saved to: {filepath}")


def generate_report(result: SEOAuditResult, output_path: str = None, format: str = "html"):
    """
    Convenience function to generate and save reports
    
    Args:
        result: SEOAuditResult from audit
        output_path: Path to save the report (optional)
        format: 'html' or 'json'
    """
    generator = AdvancedReportGenerator(result)
    
    if output_path:
        if format == "html":
            generator.save_html_report(output_path)
        elif format == "json":
            generator.save_json_report(output_path)
    else:
        if format == "html":
            return generator.generate_html_report()
        elif format == "json":
            return generator.generate_json_report()


if __name__ == "__main__":
    # Example usage
    from seo_auditor import AdvancedSEOAuditor
    
    url = "https://example.com"
    auditor = AdvancedSEOAuditor(url)
    result = auditor.run_audit()
    
    if result:
        # Generate HTML report
        generate_report(result, "seo_report.html", "html")
        
        # Generate JSON report
        generate_report(result, "seo_report.json", "json")
