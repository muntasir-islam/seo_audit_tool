"""
SEO Audit Tool - Streamlit Web App
Author: Muntasir Islam
Deploy this FREE on Streamlit Cloud!
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import json
import re
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional
import time

# Page config
st.set_page_config(
    page_title="SEO Audit Tool - Muntasir Islam",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
    }
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
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 1.1rem;
        border-radius: 10px;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    }
</style>
""", unsafe_allow_html=True)


@dataclass
class SEOAuditResult:
    """Data class to store audit results"""
    url: str
    audit_date: str
    score: int
    title: Optional[str]
    title_length: int
    title_status: str
    meta_description: Optional[str]
    meta_description_length: int
    meta_description_status: str
    meta_keywords: Optional[str]
    canonical_url: Optional[str]
    robots_meta: Optional[str]
    h1_count: int
    h1_tags: list
    h2_count: int
    h3_count: int
    heading_structure_status: str
    total_images: int
    images_without_alt: int
    images_status: str
    internal_links: int
    external_links: int
    broken_links: list
    has_ssl: bool
    has_viewport: bool
    has_charset: bool
    has_favicon: bool
    has_schema_markup: bool
    schema_types: list
    word_count: int
    critical_issues: list
    warnings: list
    recommendations: list


class SEOAuditor:
    """Main SEO Audit class"""
    
    def __init__(self, url: str):
        self.url = self._normalize_url(url)
        self.soup = None
        self.response = None
        self.issues = {"critical": [], "warnings": [], "recommendations": []}
        
    def _normalize_url(self, url: str) -> str:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def fetch_page(self) -> bool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            self.response = requests.get(self.url, headers=headers, timeout=30)
            self.response.raise_for_status()
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            return True
        except requests.RequestException as e:
            st.error(f"Error fetching {self.url}: {e}")
            return False
    
    def analyze_title(self) -> dict:
        title_tag = self.soup.find('title')
        title = title_tag.get_text().strip() if title_tag else None
        length = len(title) if title else 0
        
        if not title:
            status = "❌ Missing"
            self.issues["critical"].append("Missing page title")
        elif length < 30:
            status = "⚠️ Too Short"
            self.issues["warnings"].append(f"Title too short ({length} chars). Aim for 50-60 characters.")
        elif length > 60:
            status = "⚠️ Too Long"
            self.issues["warnings"].append(f"Title too long ({length} chars). Keep under 60 characters.")
        else:
            status = "✅ Good"
            
        return {"title": title, "length": length, "status": status}
    
    def analyze_meta_description(self) -> dict:
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '').strip() if meta_desc else None
        length = len(description) if description else 0
        
        if not description:
            status = "❌ Missing"
            self.issues["critical"].append("Missing meta description")
        elif length < 120:
            status = "⚠️ Too Short"
            self.issues["warnings"].append(f"Meta description too short ({length} chars). Aim for 150-160 characters.")
        elif length > 160:
            status = "⚠️ Too Long"
            self.issues["warnings"].append(f"Meta description too long ({length} chars). Keep under 160 characters.")
        else:
            status = "✅ Good"
            
        return {"description": description, "length": length, "status": status}
    
    def analyze_meta_keywords(self) -> Optional[str]:
        meta_kw = self.soup.find('meta', attrs={'name': 'keywords'})
        return meta_kw.get('content', '').strip() if meta_kw else None
    
    def analyze_canonical(self) -> Optional[str]:
        canonical = self.soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            self.issues["warnings"].append("Missing canonical URL tag")
        return canonical.get('href') if canonical else None
    
    def analyze_robots_meta(self) -> Optional[str]:
        robots = self.soup.find('meta', attrs={'name': 'robots'})
        return robots.get('content') if robots else None
    
    def analyze_headings(self) -> dict:
        h1_tags = [h.get_text().strip() for h in self.soup.find_all('h1')]
        h2_count = len(self.soup.find_all('h2'))
        h3_count = len(self.soup.find_all('h3'))
        h1_count = len(h1_tags)
        
        if h1_count == 0:
            status = "❌ Missing H1"
            self.issues["critical"].append("Missing H1 tag")
        elif h1_count > 1:
            status = "⚠️ Multiple H1s"
            self.issues["warnings"].append(f"Multiple H1 tags found ({h1_count}). Use only one H1 per page.")
        else:
            status = "✅ Good"
            
        return {
            "h1_count": h1_count,
            "h1_tags": h1_tags,
            "h2_count": h2_count,
            "h3_count": h3_count,
            "status": status
        }
    
    def analyze_images(self) -> dict:
        images = self.soup.find_all('img')
        total = len(images)
        without_alt = sum(1 for img in images if not img.get('alt', '').strip())
        
        if total == 0:
            status = "ℹ️ No Images"
        elif without_alt == 0:
            status = "✅ All Have Alt"
        elif without_alt / total > 0.5:
            status = "❌ Many Missing Alt"
            self.issues["critical"].append(f"{without_alt} of {total} images missing alt text")
        else:
            status = "⚠️ Some Missing Alt"
            self.issues["warnings"].append(f"{without_alt} of {total} images missing alt text")
            
        return {"total": total, "without_alt": without_alt, "status": status}
    
    def analyze_links(self) -> dict:
        links = self.soup.find_all('a', href=True)
        parsed_url = urlparse(self.url)
        base_domain = parsed_url.netloc
        
        internal = 0
        external = 0
        
        for link in links:
            href = link.get('href', '')
            if href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:'):
                continue
                
            full_url = urljoin(self.url, href)
            link_domain = urlparse(full_url).netloc
            
            if link_domain == base_domain or not link_domain:
                internal += 1
            else:
                external += 1
                
        if internal < 3:
            self.issues["recommendations"].append("Add more internal links to improve site structure")
            
        return {"internal": internal, "external": external, "broken": []}
    
    def analyze_technical(self) -> dict:
        has_ssl = self.url.startswith('https://')
        if not has_ssl:
            self.issues["critical"].append("Website not using HTTPS")
        
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        has_viewport = viewport is not None
        if not has_viewport:
            self.issues["critical"].append("Missing viewport meta tag (mobile responsiveness)")
        
        charset = self.soup.find('meta', attrs={'charset': True}) or self.soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        has_charset = charset is not None
        
        favicon = self.soup.find('link', attrs={'rel': lambda x: x and 'icon' in x.lower()})
        has_favicon = favicon is not None
        if not has_favicon:
            self.issues["warnings"].append("Missing favicon")
        
        schema_scripts = self.soup.find_all('script', attrs={'type': 'application/ld+json'})
        has_schema = len(schema_scripts) > 0
        schema_types = []
        
        for script in schema_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and '@type' in data:
                    schema_types.append(data['@type'])
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and '@type' in item:
                            schema_types.append(item['@type'])
            except:
                pass
                
        if not has_schema:
            self.issues["recommendations"].append("Add Schema.org structured data markup")
        
        return {
            "has_ssl": has_ssl,
            "has_viewport": has_viewport,
            "has_charset": has_charset,
            "has_favicon": has_favicon,
            "has_schema": has_schema,
            "schema_types": schema_types
        }
    
    def analyze_content(self) -> dict:
        soup_copy = BeautifulSoup(str(self.soup), 'html.parser')
        for element in soup_copy(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        text = soup_copy.get_text()
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        
        if word_count < 300:
            self.issues["warnings"].append(f"Low word count ({word_count}). Aim for 300+ words for better SEO.")
        
        return {"word_count": word_count}
    
    def calculate_score(self) -> int:
        score = 100
        score -= len(self.issues["critical"]) * 15
        score -= len(self.issues["warnings"]) * 5
        score -= len(self.issues["recommendations"]) * 2
        return max(0, min(100, score))
    
    def run_audit(self) -> Optional[SEOAuditResult]:
        if not self.fetch_page():
            return None
        
        title_data = self.analyze_title()
        meta_desc_data = self.analyze_meta_description()
        headings_data = self.analyze_headings()
        images_data = self.analyze_images()
        links_data = self.analyze_links()
        technical_data = self.analyze_technical()
        content_data = self.analyze_content()
        
        score = self.calculate_score()
        
        return SEOAuditResult(
            url=self.url,
            audit_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            score=score,
            title=title_data["title"],
            title_length=title_data["length"],
            title_status=title_data["status"],
            meta_description=meta_desc_data["description"],
            meta_description_length=meta_desc_data["length"],
            meta_description_status=meta_desc_data["status"],
            meta_keywords=self.analyze_meta_keywords(),
            canonical_url=self.analyze_canonical(),
            robots_meta=self.analyze_robots_meta(),
            h1_count=headings_data["h1_count"],
            h1_tags=headings_data["h1_tags"],
            h2_count=headings_data["h2_count"],
            h3_count=headings_data["h3_count"],
            heading_structure_status=headings_data["status"],
            total_images=images_data["total"],
            images_without_alt=images_data["without_alt"],
            images_status=images_data["status"],
            internal_links=links_data["internal"],
            external_links=links_data["external"],
            broken_links=links_data["broken"],
            has_ssl=technical_data["has_ssl"],
            has_viewport=technical_data["has_viewport"],
            has_charset=technical_data["has_charset"],
            has_favicon=technical_data["has_favicon"],
            has_schema_markup=technical_data["has_schema"],
            schema_types=technical_data["schema_types"],
            word_count=content_data["word_count"],
            critical_issues=self.issues["critical"],
            warnings=self.issues["warnings"],
            recommendations=self.issues["recommendations"]
        )


def display_results(result: SEOAuditResult):
    """Display audit results in Streamlit"""
    
    # Score display
    if result.score >= 80:
        score_color = "#22c55e"
        score_label = "Excellent"
    elif result.score >= 60:
        score_color = "#eab308"
        score_label = "Needs Improvement"
    else:
        score_color = "#ef4444"
        score_label = "Poor"
    
    # Header with score
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); border-radius: 20px; margin-bottom: 30px;">
            <div style="width: 150px; height: 150px; border-radius: 50%; border: 8px solid {score_color}; 
                        display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;
                        background: rgba(0,0,0,0.3);">
                <span style="font-size: 3rem; font-weight: bold; color: {score_color};">{result.score}</span>
            </div>
            <p style="font-size: 1.3rem; color: {score_color}; font-weight: 600;">{score_label}</p>
            <p style="color: #94a3b8; margin-top: 10px;">Audited: {result.audit_date}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Meta Tags Section
    st.subheader("📋 Meta Tags")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Title Tag**")
        st.info(f"{result.title_status}")
        st.text(result.title or "Not found")
        st.caption(f"Length: {result.title_length} characters (ideal: 50-60)")
    
    with col2:
        st.markdown("**Meta Description**")
        st.info(f"{result.meta_description_status}")
        st.text(result.meta_description[:150] + "..." if result.meta_description and len(result.meta_description) > 150 else result.meta_description or "Not found")
        st.caption(f"Length: {result.meta_description_length} characters (ideal: 150-160)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Canonical URL**")
        st.text(result.canonical_url or "⚠️ Missing")
    with col2:
        st.markdown("**Robots Meta**")
        st.text(result.robots_meta or "Not specified (defaults to index, follow)")
    
    st.divider()
    
    # Headings Section
    st.subheader("📝 Heading Structure")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("H1 Tags", result.h1_count, delta=result.heading_structure_status)
    col2.metric("H2 Tags", result.h2_count)
    col3.metric("H3 Tags", result.h3_count)
    col4.metric("Status", "✅" if result.h1_count == 1 else "⚠️")
    
    if result.h1_tags:
        with st.expander("View H1 Tags"):
            for h1 in result.h1_tags:
                st.write(f"• {h1}")
    
    st.divider()
    
    # Images & Links
    st.subheader("🖼️ Images & 🔗 Links")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Images", result.total_images)
    col2.metric("Missing Alt", result.images_without_alt, delta=result.images_status)
    col3.metric("Internal Links", result.internal_links)
    col4.metric("External Links", result.external_links)
    
    st.divider()
    
    # Technical SEO
    st.subheader("⚙️ Technical SEO")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Security & Mobile**")
        st.write(f"{'✅' if result.has_ssl else '❌'} HTTPS (SSL)")
        st.write(f"{'✅' if result.has_viewport else '❌'} Viewport Meta (Mobile)")
        st.write(f"{'✅' if result.has_charset else '⚠️'} Character Encoding")
    
    with col2:
        st.markdown("**Branding & Structure**")
        st.write(f"{'✅' if result.has_favicon else '⚠️'} Favicon")
        st.write(f"{'✅' if result.has_schema_markup else '❌'} Schema Markup")
    
    with col3:
        st.markdown("**Content**")
        st.metric("Word Count", result.word_count)
        if result.schema_types:
            st.write(f"Schema Types: {', '.join(result.schema_types)}")
    
    st.divider()
    
    # Issues Section
    if result.critical_issues or result.warnings or result.recommendations:
        st.subheader("🚨 Issues & Recommendations")
        
        if result.critical_issues:
            st.markdown("**Critical Issues**")
            for issue in result.critical_issues:
                st.markdown(f"""<div class="issue-critical">❌ {issue}</div>""", unsafe_allow_html=True)
        
        if result.warnings:
            st.markdown("**Warnings**")
            for warning in result.warnings:
                st.markdown(f"""<div class="issue-warning">⚠️ {warning}</div>""", unsafe_allow_html=True)
        
        if result.recommendations:
            st.markdown("**Recommendations**")
            for rec in result.recommendations:
                st.markdown(f"""<div class="issue-recommendation">💡 {rec}</div>""", unsafe_allow_html=True)
    
    # Download Report
    st.divider()
    st.subheader("📥 Export Report")
    
    col1, col2 = st.columns(2)
    with col1:
        json_data = json.dumps(asdict(result), indent=2)
        st.download_button(
            label="📄 Download JSON Report",
            data=json_data,
            file_name=f"seo_audit_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col2:
        # Generate simple text report
        text_report = f"""
SEO AUDIT REPORT
================
URL: {result.url}
Date: {result.audit_date}
Score: {result.score}/100 ({score_label})

META TAGS
---------
Title: {result.title or 'Missing'} ({result.title_length} chars)
Meta Description: {result.meta_description or 'Missing'} ({result.meta_description_length} chars)
Canonical: {result.canonical_url or 'Missing'}

HEADINGS
--------
H1 Tags: {result.h1_count}
H2 Tags: {result.h2_count}
H3 Tags: {result.h3_count}

IMAGES
------
Total: {result.total_images}
Missing Alt: {result.images_without_alt}

LINKS
-----
Internal: {result.internal_links}
External: {result.external_links}

TECHNICAL
---------
HTTPS: {'Yes' if result.has_ssl else 'No'}
Viewport: {'Yes' if result.has_viewport else 'No'}
Schema: {'Yes' if result.has_schema_markup else 'No'}

ISSUES
------
Critical: {len(result.critical_issues)}
Warnings: {len(result.warnings)}
Recommendations: {len(result.recommendations)}

---
Report generated by SEO Audit Tool
By Muntasir Islam - muntasir-islam.github.io
        """
        st.download_button(
            label="📝 Download Text Report",
            data=text_report,
            file_name=f"seo_audit_{urlparse(result.url).netloc}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )


# Main App
def main():
    # Sidebar
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/muntasir-islam/muntasir-islam.github.io/main/assets/logo.png", width=100)
        st.title("🔍 SEO Audit Tool")
        st.markdown("---")
        st.markdown("""
        **Free SEO Audit Tool**
        
        Analyze any website for:
        - Meta Tags & Titles
        - Heading Structure
        - Image Alt Tags
        - Internal/External Links
        - Technical SEO
        - Schema Markup
        
        ---
        
        **Created by:**
        [Muntasir Islam](https://muntasir-islam.github.io)
        
        💼 SEO Specialist  
        🌐 Web Strategist
        
        ---
        
        📧 Contact for professional audits
        """)
    
    # Main content
    st.title("🔍 Free SEO Audit Tool")
    st.markdown("Get instant SEO insights for any website. Enter a URL below to start.")
    
    # URL Input
    url = st.text_input(
        "Website URL",
        placeholder="example.com or https://example.com",
        help="Enter the full URL of the page you want to audit"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        audit_button = st.button("🚀 Run SEO Audit", use_container_width=True)
    
    if audit_button and url:
        with st.spinner("🔍 Analyzing website... This may take a few seconds."):
            auditor = SEOAuditor(url)
            result = auditor.run_audit()
            
            if result:
                st.success(f"✅ Audit complete for {result.url}")
                st.balloons()
                display_results(result)
            else:
                st.error("❌ Failed to audit the website. Please check the URL and try again.")
    
    elif audit_button and not url:
        st.warning("⚠️ Please enter a URL to audit")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 20px;">
        <p>Made with ❤️ by <a href="https://muntasir-islam.github.io" target="_blank">Muntasir Islam</a></p>
        <p>© 2026 | SEO Specialist & Web Strategist</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
