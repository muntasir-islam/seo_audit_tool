"""
SEO Audit Tool - Freelance Side Hustle
Author: Muntasir Islam
Description: Automated SEO audit tool for client websites
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import json
import re
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional
import time


@dataclass
class SEOAuditResult:
    """Data class to store audit results"""
    url: str
    audit_date: str
    score: int
    
    # Meta Tags
    title: Optional[str]
    title_length: int
    title_status: str
    meta_description: Optional[str]
    meta_description_length: int
    meta_description_status: str
    meta_keywords: Optional[str]
    canonical_url: Optional[str]
    robots_meta: Optional[str]
    
    # Headings
    h1_count: int
    h1_tags: list
    h2_count: int
    h3_count: int
    heading_structure_status: str
    
    # Images
    total_images: int
    images_without_alt: int
    images_status: str
    
    # Links
    internal_links: int
    external_links: int
    broken_links: list
    
    # Technical
    has_ssl: bool
    has_viewport: bool
    has_charset: bool
    has_favicon: bool
    has_schema_markup: bool
    schema_types: list
    
    # Content
    word_count: int
    
    # Issues & Recommendations
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
        """Ensure URL has proper scheme"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def fetch_page(self) -> bool:
        """Fetch the webpage content"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            self.response = requests.get(self.url, headers=headers, timeout=30)
            self.response.raise_for_status()
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            return True
        except requests.RequestException as e:
            print(f"Error fetching {self.url}: {e}")
            return False
    
    def analyze_title(self) -> dict:
        """Analyze page title"""
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
        """Analyze meta description"""
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
        """Get meta keywords (deprecated but still used)"""
        meta_kw = self.soup.find('meta', attrs={'name': 'keywords'})
        return meta_kw.get('content', '').strip() if meta_kw else None
    
    def analyze_canonical(self) -> Optional[str]:
        """Get canonical URL"""
        canonical = self.soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            self.issues["warnings"].append("Missing canonical URL tag")
        return canonical.get('href') if canonical else None
    
    def analyze_robots_meta(self) -> Optional[str]:
        """Get robots meta tag"""
        robots = self.soup.find('meta', attrs={'name': 'robots'})
        return robots.get('content') if robots else None
    
    def analyze_headings(self) -> dict:
        """Analyze heading structure"""
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
        """Analyze images and alt tags"""
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
        """Analyze internal and external links"""
        links = self.soup.find_all('a', href=True)
        parsed_url = urlparse(self.url)
        base_domain = parsed_url.netloc
        
        internal = 0
        external = 0
        broken = []
        
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
            
        return {"internal": internal, "external": external, "broken": broken}
    
    def analyze_technical(self) -> dict:
        """Analyze technical SEO elements"""
        # SSL
        has_ssl = self.url.startswith('https://')
        if not has_ssl:
            self.issues["critical"].append("Website not using HTTPS")
        
        # Viewport
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        has_viewport = viewport is not None
        if not has_viewport:
            self.issues["critical"].append("Missing viewport meta tag (mobile responsiveness)")
        
        # Charset
        charset = self.soup.find('meta', attrs={'charset': True}) or self.soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        has_charset = charset is not None
        
        # Favicon
        favicon = self.soup.find('link', attrs={'rel': lambda x: x and 'icon' in x.lower()})
        has_favicon = favicon is not None
        if not has_favicon:
            self.issues["warnings"].append("Missing favicon")
        
        # Schema markup
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
        """Analyze page content"""
        # Remove script and style elements
        for element in self.soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        text = self.soup.get_text()
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        
        if word_count < 300:
            self.issues["warnings"].append(f"Low word count ({word_count}). Aim for 300+ words for better SEO.")
        
        return {"word_count": word_count}
    
    def calculate_score(self) -> int:
        """Calculate overall SEO score"""
        score = 100
        
        # Deduct points for issues
        score -= len(self.issues["critical"]) * 15
        score -= len(self.issues["warnings"]) * 5
        score -= len(self.issues["recommendations"]) * 2
        
        return max(0, min(100, score))
    
    def run_audit(self) -> Optional[SEOAuditResult]:
        """Run complete SEO audit"""
        print(f"\n🔍 Starting SEO Audit for: {self.url}")
        print("=" * 50)
        
        if not self.fetch_page():
            return None
        
        # Run all analyses
        title_data = self.analyze_title()
        meta_desc_data = self.analyze_meta_description()
        headings_data = self.analyze_headings()
        images_data = self.analyze_images()
        links_data = self.analyze_links()
        technical_data = self.analyze_technical()
        content_data = self.analyze_content()
        
        score = self.calculate_score()
        
        result = SEOAuditResult(
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
        
        return result


def print_audit_report(result: SEOAuditResult):
    """Print a formatted audit report"""
    
    # Score color
    if result.score >= 80:
        score_indicator = "🟢"
    elif result.score >= 60:
        score_indicator = "🟡"
    else:
        score_indicator = "🔴"
    
    report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                      SEO AUDIT REPORT                            ║
╠══════════════════════════════════════════════════════════════════╣
║  URL: {result.url[:55]:<55} ║
║  Date: {result.audit_date:<54} ║
║  Score: {score_indicator} {result.score}/100{' ' * 50} ║
╚══════════════════════════════════════════════════════════════════╝

📋 META TAGS
┌──────────────────────────────────────────────────────────────────┐
│ Title: {result.title_status}
│ → {(result.title or 'Not found')[:60]}
│ → Length: {result.title_length} characters
│
│ Meta Description: {result.meta_description_status}
│ → {(result.meta_description or 'Not found')[:60]}
│ → Length: {result.meta_description_length} characters
│
│ Canonical: {'✅ Set' if result.canonical_url else '⚠️ Missing'}
│ Robots: {result.robots_meta or 'Not specified'}
└──────────────────────────────────────────────────────────────────┘

📝 HEADINGS
┌──────────────────────────────────────────────────────────────────┐
│ H1 Tags: {result.h1_count} {result.heading_structure_status}
│ H2 Tags: {result.h2_count}
│ H3 Tags: {result.h3_count}
└──────────────────────────────────────────────────────────────────┘

🖼️ IMAGES
┌──────────────────────────────────────────────────────────────────┐
│ Total Images: {result.total_images}
│ Missing Alt Text: {result.images_without_alt} {result.images_status}
└──────────────────────────────────────────────────────────────────┘

🔗 LINKS
┌──────────────────────────────────────────────────────────────────┐
│ Internal Links: {result.internal_links}
│ External Links: {result.external_links}
└──────────────────────────────────────────────────────────────────┘

⚙️ TECHNICAL SEO
┌──────────────────────────────────────────────────────────────────┐
│ HTTPS: {'✅ Yes' if result.has_ssl else '❌ No'}
│ Viewport Meta: {'✅ Yes' if result.has_viewport else '❌ No'}
│ Charset: {'✅ Yes' if result.has_charset else '⚠️ Missing'}
│ Favicon: {'✅ Yes' if result.has_favicon else '⚠️ Missing'}
│ Schema Markup: {'✅ Yes (' + ', '.join(result.schema_types) + ')' if result.has_schema_markup else '❌ No'}
└──────────────────────────────────────────────────────────────────┘

📊 CONTENT
┌──────────────────────────────────────────────────────────────────┐
│ Word Count: {result.word_count}
└──────────────────────────────────────────────────────────────────┘
"""
    
    if result.critical_issues:
        report += """
🚨 CRITICAL ISSUES
┌──────────────────────────────────────────────────────────────────┐
"""
        for issue in result.critical_issues:
            report += f"│ ❌ {issue}\n"
        report += "└──────────────────────────────────────────────────────────────────┘"
    
    if result.warnings:
        report += """

⚠️ WARNINGS
┌──────────────────────────────────────────────────────────────────┐
"""
        for warning in result.warnings:
            report += f"│ ⚠️ {warning}\n"
        report += "└──────────────────────────────────────────────────────────────────┘"
    
    if result.recommendations:
        report += """

💡 RECOMMENDATIONS
┌──────────────────────────────────────────────────────────────────┐
"""
        for rec in result.recommendations:
            report += f"│ 💡 {rec}\n"
        report += "└──────────────────────────────────────────────────────────────────┘"
    
    print(report)
    return report


def save_report_json(result: SEOAuditResult, filename: str = None):
    """Save audit result as JSON"""
    if filename is None:
        domain = urlparse(result.url).netloc.replace('.', '_')
        filename = f"audit_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(asdict(result), f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Report saved to: {filename}")
    return filename


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           🔍 SEO AUDIT TOOL - By Muntasir Islam           ║
    ║              Freelance SEO Services                       ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Get URL from user
    url = input("Enter website URL to audit: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    # Run audit
    auditor = SEOAuditor(url)
    result = auditor.run_audit()
    
    if result:
        # Print report
        print_audit_report(result)
        
        # Ask to save
        save = input("\nSave report as JSON? (y/n): ").strip().lower()
        if save == 'y':
            save_report_json(result)
    else:
        print("❌ Failed to complete audit. Please check the URL and try again.")


if __name__ == "__main__":
    main()
