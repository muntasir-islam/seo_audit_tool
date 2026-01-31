"""
Advanced Batch SEO Audit Tool - 200+ Parameters
Audit multiple URLs at once with comprehensive analysis
Author: Muntasir Islam
Version: 2.0
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from typing import List, Dict, Optional
import time

from seo_auditor import AdvancedSEOAuditor, SEOAuditResult
from report_generator import AdvancedReportGenerator


class BatchAuditor:
    """Run SEO audits on multiple URLs"""
    
    def __init__(self, 
                 urls: List[str], 
                 target_keyword: str = None,
                 max_workers: int = 3,
                 output_dir: str = "batch_reports"):
        self.urls = urls
        self.target_keyword = target_keyword
        self.max_workers = max_workers
        self.output_dir = output_dir
        self.results: List[SEOAuditResult] = []
        self.failed_urls: List[Dict] = []
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def audit_single_url(self, url: str) -> Optional[SEOAuditResult]:
        """Audit a single URL"""
        try:
            print(f"\n🔍 Auditing: {url}")
            auditor = AdvancedSEOAuditor(url, target_keyword=self.target_keyword)
            result = auditor.run_audit()
            
            if result:
                print(f"   ✅ Score: {result.score}/100 (Grade: {result.grade})")
                return result
            else:
                print(f"   ❌ Failed to audit")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None
    
    def run_batch_audit(self, parallel: bool = False) -> List[SEOAuditResult]:
        """
        Run batch audit on all URLs
        
        Args:
            parallel: Run audits in parallel (faster but may trigger rate limits)
        """
        print(f"\n{'='*60}")
        print(f"🚀 Starting Batch SEO Audit")
        print(f"📊 URLs to audit: {len(self.urls)}")
        print(f"🎯 Target keyword: {self.target_keyword or 'None'}")
        print(f"💾 Output directory: {self.output_dir}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        if parallel and self.max_workers > 1:
            self._run_parallel()
        else:
            self._run_sequential()
        
        elapsed = time.time() - start_time
        
        print(f"\n{'='*60}")
        print(f"✅ Batch Audit Complete!")
        print(f"⏱️  Total time: {elapsed:.2f} seconds")
        print(f"📊 Successful: {len(self.results)}/{len(self.urls)}")
        print(f"❌ Failed: {len(self.failed_urls)}")
        print(f"{'='*60}\n")
        
        return self.results
    
    def _run_sequential(self):
        """Run audits sequentially"""
        for i, url in enumerate(self.urls, 1):
            print(f"\n[{i}/{len(self.urls)}]", end="")
            result = self.audit_single_url(url)
            
            if result:
                self.results.append(result)
            else:
                self.failed_urls.append({"url": url, "error": "Failed to audit"})
            
            # Small delay to avoid rate limiting
            if i < len(self.urls):
                time.sleep(1)
    
    def _run_parallel(self):
        """Run audits in parallel"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self.audit_single_url, url): url 
                for url in self.urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        self.results.append(result)
                    else:
                        self.failed_urls.append({"url": url, "error": "Failed to audit"})
                except Exception as e:
                    self.failed_urls.append({"url": url, "error": str(e)})
    
    def generate_summary_report(self) -> Dict:
        """Generate a summary report of all audits"""
        if not self.results:
            return {"error": "No successful audits"}
        
        scores = [r.score for r in self.results]
        
        summary = {
            "audit_date": datetime.now().isoformat(),
            "total_urls": len(self.urls),
            "successful_audits": len(self.results),
            "failed_audits": len(self.failed_urls),
            "target_keyword": self.target_keyword,
            "overall_statistics": {
                "average_score": round(sum(scores) / len(scores), 1),
                "highest_score": max(scores),
                "lowest_score": min(scores),
                "median_score": sorted(scores)[len(scores)//2],
            },
            "grade_distribution": {
                "A+": len([r for r in self.results if r.grade == "A+"]),
                "A": len([r for r in self.results if r.grade == "A"]),
                "B": len([r for r in self.results if r.grade == "B"]),
                "C": len([r for r in self.results if r.grade == "C"]),
                "D": len([r for r in self.results if r.grade == "D"]),
                "F": len([r for r in self.results if r.grade == "F"]),
            },
            "common_issues": self._get_common_issues(),
            "category_averages": self._get_category_averages(),
            "individual_results": [
                {
                    "url": r.url,
                    "score": r.score,
                    "grade": r.grade,
                    "critical_issues": len(r.critical_issues),
                    "warnings": len(r.warnings),
                    "word_count": r.word_count,
                    "response_time": r.response_time,
                }
                for r in self.results
            ],
            "failed_urls": self.failed_urls
        }
        
        return summary
    
    def _get_common_issues(self) -> List[Dict]:
        """Get most common issues across all audited URLs"""
        issue_counts = {}
        
        for result in self.results:
            for issue in result.critical_issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
            for warning in result.warnings:
                issue_counts[warning] = issue_counts.get(warning, 0) + 1
        
        # Sort by count and return top 20
        sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        return [{"issue": k, "count": v, "percentage": round(v/len(self.results)*100, 1)} 
                for k, v in sorted_issues]
    
    def _get_category_averages(self) -> Dict:
        """Get average scores for each category"""
        if not self.results:
            return {}
        
        categories = {
            "meta_tags_score": [],
            "og_score": [],
            "twitter_score": [],
            "headings_score": [],
            "images_score": [],
            "links_score": [],
            "technical_seo_score": [],
            "content_score": [],
            "ux_score": [],
            "i18n_score": [],
            "ecommerce_score": [],
            "accessibility_score": [],
            "performance_hints_score": [],
            "security_headers_score": [],
        }
        
        for result in self.results:
            for cat in categories.keys():
                categories[cat].append(getattr(result, cat, 0))
        
        return {
            cat.replace("_score", "").replace("_", " ").title(): 
            round(sum(scores)/len(scores), 1) if scores else 0
            for cat, scores in categories.items()
        }
    
    def save_reports(self, formats: List[str] = ["html", "json", "csv"]):
        """
        Save all reports in specified formats
        
        Args:
            formats: List of formats to save ('html', 'json', 'csv')
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save individual HTML reports
        if "html" in formats:
            html_dir = os.path.join(self.output_dir, "html_reports")
            os.makedirs(html_dir, exist_ok=True)
            
            for result in self.results:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(result.url).netloc.replace(".", "_")
                    filepath = os.path.join(html_dir, f"{domain}_{timestamp}.html")
                    generator = AdvancedReportGenerator(result)
                    generator.save_html_report(filepath)
                except Exception as e:
                    print(f"❌ Error saving HTML for {result.url}: {e}")
            
            print(f"📄 HTML reports saved to: {html_dir}")
        
        # Save JSON reports
        if "json" in formats:
            json_dir = os.path.join(self.output_dir, "json_reports")
            os.makedirs(json_dir, exist_ok=True)
            
            # Individual reports
            for result in self.results:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(result.url).netloc.replace(".", "_")
                    filepath = os.path.join(json_dir, f"{domain}_{timestamp}.json")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(asdict(result), f, indent=2, default=str)
                except Exception as e:
                    print(f"❌ Error saving JSON for {result.url}: {e}")
            
            # Summary report
            summary_path = os.path.join(self.output_dir, f"batch_summary_{timestamp}.json")
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(self.generate_summary_report(), f, indent=2, default=str)
            
            print(f"📊 JSON reports saved to: {json_dir}")
            print(f"📋 Summary saved to: {summary_path}")
        
        # Save CSV summary
        if "csv" in formats:
            csv_path = os.path.join(self.output_dir, f"batch_audit_{timestamp}.csv")
            self._save_csv_report(csv_path)
            print(f"📈 CSV report saved to: {csv_path}")
        
        # Save combined HTML summary
        self._save_batch_html_summary(timestamp)
    
    def _save_csv_report(self, filepath: str):
        """Save CSV report with key metrics"""
        if not self.results:
            return
        
        headers = [
            "URL", "Score", "Grade", "Response Time (s)", "Page Size (KB)",
            "Word Count", "Title", "Title Length", "Meta Description Length",
            "H1 Count", "Total Images", "Images Without Alt", "Total Links",
            "Internal Links", "External Links", "Has SSL", "Has Viewport",
            "Has Schema", "Critical Issues", "Warnings", "Recommendations"
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for r in self.results:
                row = [
                    r.url,
                    r.score,
                    r.grade,
                    round(r.response_time, 2),
                    r.page_size_kb,
                    r.word_count,
                    r.title[:50] if r.title else "",
                    r.title_length,
                    r.meta_description_length,
                    r.h1_count,
                    r.total_images,
                    r.images_without_alt,
                    r.total_links,
                    r.internal_links,
                    r.external_links,
                    "Yes" if r.has_ssl else "No",
                    "Yes" if r.has_viewport else "No",
                    "Yes" if r.has_schema_markup else "No",
                    len(r.critical_issues),
                    len(r.warnings),
                    len(r.recommendations)
                ]
                writer.writerow(row)
    
    def _save_batch_html_summary(self, timestamp: str):
        """Generate and save batch HTML summary report"""
        summary = self.generate_summary_report()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Batch SEO Audit Summary</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
            color: #e2e8f0;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ text-align: center; margin-bottom: 30px; color: #f1f5f9; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #1e293b;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #f1f5f9;
        }}
        .stat-label {{ color: #94a3b8; margin-top: 5px; }}
        .section {{
            background: #1e293b;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }}
        .section h2 {{
            color: #f1f5f9;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #334155;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #334155;
        }}
        th {{ background: #0f172a; }}
        .grade-a {{ color: #22c55e; }}
        .grade-b {{ color: #84cc16; }}
        .grade-c {{ color: #eab308; }}
        .grade-d {{ color: #f97316; }}
        .grade-f {{ color: #ef4444; }}
        .chart {{ display: flex; gap: 5px; align-items: flex-end; height: 150px; }}
        .bar {{
            flex: 1;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-radius: 5px 5px 0 0;
            position: relative;
        }}
        .bar-label {{
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.8rem;
            color: #94a3b8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Batch SEO Audit Summary</h1>
        <p style="text-align: center; color: #94a3b8; margin-bottom: 30px;">
            Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 
            Target Keyword: {self.target_keyword or 'None'}
        </p>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{summary['successful_audits']}</div>
                <div class="stat-label">URLs Audited</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary['overall_statistics']['average_score']}</div>
                <div class="stat-label">Average Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary['overall_statistics']['highest_score']}</div>
                <div class="stat-label">Highest Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary['overall_statistics']['lowest_score']}</div>
                <div class="stat-label">Lowest Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary['failed_audits']}</div>
                <div class="stat-label">Failed Audits</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Grade Distribution</h2>
            <div style="display: flex; justify-content: space-around; text-align: center;">
                {''.join([f'<div><div class="stat-value grade-{g.lower()}">{c}</div><div class="stat-label">{g}</div></div>' 
                          for g, c in summary['grade_distribution'].items()])}
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Category Averages</h2>
            <div class="stats-grid">
                {''.join([f'<div class="stat-card"><div class="stat-value">{v}</div><div class="stat-label">{k}</div></div>' 
                          for k, v in summary['category_averages'].items()])}
            </div>
        </div>
        
        <div class="section">
            <h2>🔗 Individual Results</h2>
            <table>
                <tr>
                    <th>URL</th>
                    <th>Score</th>
                    <th>Grade</th>
                    <th>Critical</th>
                    <th>Warnings</th>
                    <th>Words</th>
                    <th>Response</th>
                </tr>
                {''.join([f'''<tr>
                    <td><a href="{r['url']}" style="color: #6366f1;">{r['url'][:50]}...</a></td>
                    <td>{r['score']}</td>
                    <td class="grade-{r['grade'].lower().replace('+', '')}">{r['grade']}</td>
                    <td>{r['critical_issues']}</td>
                    <td>{r['warnings']}</td>
                    <td>{r['word_count']}</td>
                    <td>{r['response_time']:.2f}s</td>
                </tr>''' for r in summary['individual_results']])}
            </table>
        </div>
        
        <div class="section">
            <h2>⚠️ Most Common Issues</h2>
            <table>
                <tr><th>Issue</th><th>Count</th><th>Percentage</th></tr>
                {''.join([f'<tr><td>{i["issue"]}</td><td>{i["count"]}</td><td>{i["percentage"]}%</td></tr>' 
                          for i in summary['common_issues'][:15]])}
            </table>
        </div>
        
        <p style="text-align: center; color: #64748b; margin-top: 30px;">
            Generated by Advanced SEO Audit Tool v2.0 | 
            <a href="https://muntasir-islam.github.io" style="color: #6366f1;">Muntasir Islam</a>
        </p>
    </div>
</body>
</html>
"""
        
        filepath = os.path.join(self.output_dir, f"batch_summary_{timestamp}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"📊 Batch summary HTML saved to: {filepath}")


def load_urls_from_file(filepath: str) -> List[str]:
    """Load URLs from a text file (one URL per line)"""
    urls = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            if url and not url.startswith('#'):
                urls.append(url)
    return urls


def main():
    parser = argparse.ArgumentParser(
        description="Advanced Batch SEO Audit Tool - 200+ Parameters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_audit.py -u https://example.com https://another.com
  python batch_audit.py -f urls.txt -k "seo audit" -o reports
  python batch_audit.py -f urls.txt --parallel -w 5
        """
    )
    
    parser.add_argument("-u", "--urls", nargs="+", help="URLs to audit")
    parser.add_argument("-f", "--file", help="File containing URLs (one per line)")
    parser.add_argument("-k", "--keyword", help="Target keyword to check")
    parser.add_argument("-o", "--output", default="batch_reports", help="Output directory")
    parser.add_argument("--parallel", action="store_true", help="Run audits in parallel")
    parser.add_argument("-w", "--workers", type=int, default=3, help="Max parallel workers")
    parser.add_argument("--formats", nargs="+", default=["html", "json", "csv"],
                       help="Output formats (html, json, csv)")
    
    args = parser.parse_args()
    
    # Get URLs
    urls = []
    if args.urls:
        urls.extend(args.urls)
    if args.file:
        urls.extend(load_urls_from_file(args.file))
    
    if not urls:
        print("❌ No URLs provided. Use -u or -f to specify URLs.")
        parser.print_help()
        sys.exit(1)
    
    # Run batch audit
    auditor = BatchAuditor(
        urls=urls,
        target_keyword=args.keyword,
        max_workers=args.workers,
        output_dir=args.output
    )
    
    results = auditor.run_batch_audit(parallel=args.parallel)
    
    # Save reports
    if results:
        auditor.save_reports(formats=args.formats)
        
        # Print summary
        summary = auditor.generate_summary_report()
        print(f"\n📊 Summary:")
        print(f"   Average Score: {summary['overall_statistics']['average_score']}")
        print(f"   Highest: {summary['overall_statistics']['highest_score']}")
        print(f"   Lowest: {summary['overall_statistics']['lowest_score']}")
    else:
        print("❌ No successful audits to report.")


if __name__ == "__main__":
    main()
