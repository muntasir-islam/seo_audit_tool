"""
HTML Report Generator for SEO Audits
Generates professional client-ready reports
"""

from seo_auditor import SEOAuditor, SEOAuditResult
from dataclasses import asdict
from datetime import datetime
from urllib.parse import urlparse
import json


def generate_html_report(result: SEOAuditResult) -> str:
    """Generate a professional HTML report"""
    
    # Score color
    if result.score >= 80:
        score_color = "#22c55e"  # Green
        score_label = "Excellent"
    elif result.score >= 60:
        score_color = "#eab308"  # Yellow
        score_label = "Needs Improvement"
    else:
        score_color = "#ef4444"  # Red
        score_label = "Poor"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Audit Report - {urlparse(result.url).netloc}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e4e4e7;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            color: #fff;
            margin-bottom: 10px;
        }}
        
        .header .url {{
            color: #94a3b8;
            font-size: 1.1rem;
        }}
        
        .header .date {{
            color: #64748b;
            font-size: 0.9rem;
            margin-top: 5px;
        }}
        
        .score-card {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        
        .score-circle {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 8px solid {score_color};
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            background: rgba(0,0,0,0.3);
        }}
        
        .score-number {{
            font-size: 3rem;
            font-weight: bold;
            color: {score_color};
        }}
        
        .score-label {{
            font-size: 1.3rem;
            color: {score_color};
            font-weight: 600;
        }}
        
        .section {{
            background: #1e293b;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }}
        
        .section-title {{
            font-size: 1.3rem;
            color: #fff;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-title .icon {{
            font-size: 1.5rem;
        }}
        
        .item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #334155;
        }}
        
        .item:last-child {{
            border-bottom: none;
        }}
        
        .item-label {{
            color: #94a3b8;
        }}
        
        .item-value {{
            font-weight: 600;
        }}
        
        .status-good {{
            color: #22c55e;
        }}
        
        .status-warning {{
            color: #eab308;
        }}
        
        .status-bad {{
            color: #ef4444;
        }}
        
        .issues-section {{
            margin-top: 30px;
        }}
        
        .issue-card {{
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #ef4444;
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 0 10px 10px 0;
        }}
        
        .issue-card.warning {{
            background: rgba(234, 179, 8, 0.1);
            border-left-color: #eab308;
        }}
        
        .issue-card.recommendation {{
            background: rgba(59, 130, 246, 0.1);
            border-left-color: #3b82f6;
        }}
        
        .issue-title {{
            font-weight: 600;
            margin-bottom: 5px;
        }}
        
        .meta-preview {{
            background: #0f172a;
            border-radius: 10px;
            padding: 20px;
            margin-top: 15px;
        }}
        
        .meta-preview-title {{
            color: #1a0dab;
            font-size: 1.2rem;
            margin-bottom: 5px;
            text-decoration: underline;
        }}
        
        .meta-preview-url {{
            color: #006621;
            font-size: 0.9rem;
            margin-bottom: 5px;
        }}
        
        .meta-preview-desc {{
            color: #545454;
            font-size: 0.95rem;
            line-height: 1.4;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #334155;
            color: #64748b;
        }}
        
        .footer a {{
            color: #3b82f6;
            text-decoration: none;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .stat-card {{
            background: #0f172a;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #fff;
        }}
        
        .stat-label {{
            color: #64748b;
            font-size: 0.9rem;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 SEO Audit Report</h1>
            <div class="url">{result.url}</div>
            <div class="date">Generated on {result.audit_date}</div>
        </div>
        
        <div class="score-card">
            <div class="score-circle">
                <span class="score-number">{result.score}</span>
            </div>
            <div class="score-label">{score_label}</div>
        </div>
        
        <div class="section">
            <div class="section-title">
                <span class="icon">📊</span>
                Quick Overview
            </div>
            <div class="grid">
                <div class="stat-card">
                    <div class="stat-number">{result.h1_count}</div>
                    <div class="stat-label">H1 Tags</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{result.total_images}</div>
                    <div class="stat-label">Images</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{result.internal_links}</div>
                    <div class="stat-label">Internal Links</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{result.word_count}</div>
                    <div class="stat-label">Words</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">
                <span class="icon">🏷️</span>
                Meta Tags Analysis
            </div>
            
            <div class="item">
                <span class="item-label">Title Tag</span>
                <span class="item-value {'status-good' if '✅' in result.title_status else 'status-warning' if '⚠️' in result.title_status else 'status-bad'}">{result.title_status}</span>
            </div>
            <div class="item">
                <span class="item-label">Title Length</span>
                <span class="item-value">{result.title_length} characters</span>
            </div>
            <div class="item">
                <span class="item-label">Meta Description</span>
                <span class="item-value {'status-good' if '✅' in result.meta_description_status else 'status-warning' if '⚠️' in result.meta_description_status else 'status-bad'}">{result.meta_description_status}</span>
            </div>
            <div class="item">
                <span class="item-label">Description Length</span>
                <span class="item-value">{result.meta_description_length} characters</span>
            </div>
            <div class="item">
                <span class="item-label">Canonical URL</span>
                <span class="item-value {'status-good' if result.canonical_url else 'status-warning'}">{'✅ Set' if result.canonical_url else '⚠️ Missing'}</span>
            </div>
            
            <div class="meta-preview">
                <div class="meta-preview-title">{result.title or 'No title set'}</div>
                <div class="meta-preview-url">{result.url}</div>
                <div class="meta-preview-desc">{result.meta_description or 'No description set'}</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">
                <span class="icon">📝</span>
                Heading Structure
            </div>
            <div class="item">
                <span class="item-label">H1 Tags</span>
                <span class="item-value">{result.h1_count} {result.heading_structure_status}</span>
            </div>
            <div class="item">
                <span class="item-label">H2 Tags</span>
                <span class="item-value">{result.h2_count}</span>
            </div>
            <div class="item">
                <span class="item-label">H3 Tags</span>
                <span class="item-value">{result.h3_count}</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">
                <span class="icon">🖼️</span>
                Images
            </div>
            <div class="item">
                <span class="item-label">Total Images</span>
                <span class="item-value">{result.total_images}</span>
            </div>
            <div class="item">
                <span class="item-label">Missing Alt Text</span>
                <span class="item-value {'status-good' if result.images_without_alt == 0 else 'status-warning' if result.images_without_alt < result.total_images / 2 else 'status-bad'}">{result.images_without_alt}</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">
                <span class="icon">🔗</span>
                Links
            </div>
            <div class="item">
                <span class="item-label">Internal Links</span>
                <span class="item-value">{result.internal_links}</span>
            </div>
            <div class="item">
                <span class="item-label">External Links</span>
                <span class="item-value">{result.external_links}</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">
                <span class="icon">⚙️</span>
                Technical SEO
            </div>
            <div class="item">
                <span class="item-label">HTTPS</span>
                <span class="item-value {'status-good' if result.has_ssl else 'status-bad'}">{'✅ Yes' if result.has_ssl else '❌ No'}</span>
            </div>
            <div class="item">
                <span class="item-label">Mobile Viewport</span>
                <span class="item-value {'status-good' if result.has_viewport else 'status-bad'}">{'✅ Yes' if result.has_viewport else '❌ No'}</span>
            </div>
            <div class="item">
                <span class="item-label">Charset Defined</span>
                <span class="item-value {'status-good' if result.has_charset else 'status-warning'}">{'✅ Yes' if result.has_charset else '⚠️ No'}</span>
            </div>
            <div class="item">
                <span class="item-label">Favicon</span>
                <span class="item-value {'status-good' if result.has_favicon else 'status-warning'}">{'✅ Yes' if result.has_favicon else '⚠️ No'}</span>
            </div>
            <div class="item">
                <span class="item-label">Schema Markup</span>
                <span class="item-value {'status-good' if result.has_schema_markup else 'status-warning'}">{'✅ ' + ', '.join(result.schema_types) if result.has_schema_markup else '⚠️ Not Found'}</span>
            </div>
        </div>
        
        <div class="issues-section">
"""
    
    # Critical Issues
    if result.critical_issues:
        html += """
            <div class="section">
                <div class="section-title">
                    <span class="icon">🚨</span>
                    Critical Issues
                </div>
"""
        for issue in result.critical_issues:
            html += f"""
                <div class="issue-card">
                    <div class="issue-title">❌ {issue}</div>
                </div>
"""
        html += "</div>"
    
    # Warnings
    if result.warnings:
        html += """
            <div class="section">
                <div class="section-title">
                    <span class="icon">⚠️</span>
                    Warnings
                </div>
"""
        for warning in result.warnings:
            html += f"""
                <div class="issue-card warning">
                    <div class="issue-title">⚠️ {warning}</div>
                </div>
"""
        html += "</div>"
    
    # Recommendations
    if result.recommendations:
        html += """
            <div class="section">
                <div class="section-title">
                    <span class="icon">💡</span>
                    Recommendations
                </div>
"""
        for rec in result.recommendations:
            html += f"""
                <div class="issue-card recommendation">
                    <div class="issue-title">💡 {rec}</div>
                </div>
"""
        html += "</div>"
    
    html += f"""
        </div>
        
        <div class="footer">
            <p>Report generated by <strong>Muntasir Islam</strong> - SEO Specialist</p>
            <p><a href="https://muntasir-islam.github.io">muntasir-islam.github.io</a></p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def save_html_report(result: SEOAuditResult, filename: str = None) -> str:
    """Save HTML report to file"""
    if filename is None:
        domain = urlparse(result.url).netloc.replace('.', '_')
        filename = f"audit_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    html = generate_html_report(result)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"📄 HTML Report saved to: {filename}")
    return filename


if __name__ == "__main__":
    # Example usage
    url = input("Enter URL to audit and generate HTML report: ").strip()
    
    if url:
        auditor = SEOAuditor(url)
        result = auditor.run_audit()
        
        if result:
            filename = save_html_report(result)
            print(f"\n✅ Open {filename} in your browser to view the report!")
