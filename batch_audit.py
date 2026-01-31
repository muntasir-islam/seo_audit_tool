"""
Batch SEO Audit Tool
Audit multiple URLs at once - perfect for competitor analysis
"""

from seo_auditor import SEOAuditor, SEOAuditResult, print_audit_report, save_report_json
from report_generator import save_html_report
from dataclasses import asdict
import json
import csv
from datetime import datetime
import time
import os


def audit_multiple_urls(urls: list, delay: float = 2.0) -> list:
    """
    Audit multiple URLs with a delay between requests
    
    Args:
        urls: List of URLs to audit
        delay: Seconds to wait between audits (be nice to servers)
    
    Returns:
        List of SEOAuditResult objects
    """
    results = []
    total = len(urls)
    
    print(f"\n🚀 Starting batch audit of {total} URLs...")
    print("=" * 60)
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{total}] Auditing: {url}")
        
        try:
            auditor = SEOAuditor(url)
            result = auditor.run_audit()
            
            if result:
                results.append(result)
                print(f"✅ Score: {result.score}/100")
            else:
                print(f"❌ Failed to audit")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Delay between requests
        if i < total:
            time.sleep(delay)
    
    print(f"\n{'=' * 60}")
    print(f"✅ Completed {len(results)}/{total} audits")
    
    return results


def generate_comparison_report(results: list) -> str:
    """Generate a comparison report for multiple URLs"""
    
    if not results:
        return "No results to compare"
    
    report = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         BATCH SEO AUDIT COMPARISON                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
    
    # Sort by score (highest first)
    sorted_results = sorted(results, key=lambda x: x.score, reverse=True)
    
    # Summary table
    report += "📊 SCORE RANKING\n"
    report += "─" * 80 + "\n"
    report += f"{'Rank':<6}{'Score':<8}{'URL':<66}\n"
    report += "─" * 80 + "\n"
    
    for i, r in enumerate(sorted_results, 1):
        score_icon = "🟢" if r.score >= 80 else "🟡" if r.score >= 60 else "🔴"
        report += f"{i:<6}{score_icon} {r.score:<5}{r.url[:63]:<63}\n"
    
    report += "─" * 80 + "\n\n"
    
    # Detailed comparison
    report += "📋 DETAILED COMPARISON\n"
    report += "─" * 80 + "\n"
    report += f"{'Metric':<25}"
    for r in sorted_results[:5]:  # Top 5 only
        domain = r.url.replace('https://', '').replace('http://', '')[:12]
        report += f"{domain:<12}"
    report += "\n"
    report += "─" * 80 + "\n"
    
    metrics = [
        ("SEO Score", lambda r: str(r.score)),
        ("Title Length", lambda r: str(r.title_length)),
        ("Meta Desc Length", lambda r: str(r.meta_description_length)),
        ("H1 Count", lambda r: str(r.h1_count)),
        ("Images", lambda r: str(r.total_images)),
        ("Images w/o Alt", lambda r: str(r.images_without_alt)),
        ("Internal Links", lambda r: str(r.internal_links)),
        ("External Links", lambda r: str(r.external_links)),
        ("Word Count", lambda r: str(r.word_count)),
        ("Has HTTPS", lambda r: "✅" if r.has_ssl else "❌"),
        ("Has Schema", lambda r: "✅" if r.has_schema_markup else "❌"),
        ("Critical Issues", lambda r: str(len(r.critical_issues))),
        ("Warnings", lambda r: str(len(r.warnings))),
    ]
    
    for metric_name, metric_func in metrics:
        report += f"{metric_name:<25}"
        for r in sorted_results[:5]:
            report += f"{metric_func(r):<12}"
        report += "\n"
    
    report += "─" * 80 + "\n"
    
    # Common issues
    all_critical = []
    all_warnings = []
    
    for r in results:
        all_critical.extend(r.critical_issues)
        all_warnings.extend(r.warnings)
    
    if all_critical:
        report += "\n🚨 COMMON CRITICAL ISSUES\n"
        report += "─" * 40 + "\n"
        issue_counts = {}
        for issue in all_critical:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"  [{count}x] {issue}\n"
    
    return report


def export_to_csv(results: list, filename: str = None) -> str:
    """Export audit results to CSV"""
    
    if filename is None:
        filename = f"batch_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    fieldnames = [
        'url', 'score', 'audit_date',
        'title', 'title_length', 'meta_description_length',
        'h1_count', 'h2_count', 'h3_count',
        'total_images', 'images_without_alt',
        'internal_links', 'external_links',
        'has_ssl', 'has_viewport', 'has_schema_markup',
        'word_count', 'critical_issues_count', 'warnings_count'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in results:
            writer.writerow({
                'url': r.url,
                'score': r.score,
                'audit_date': r.audit_date,
                'title': r.title,
                'title_length': r.title_length,
                'meta_description_length': r.meta_description_length,
                'h1_count': r.h1_count,
                'h2_count': r.h2_count,
                'h3_count': r.h3_count,
                'total_images': r.total_images,
                'images_without_alt': r.images_without_alt,
                'internal_links': r.internal_links,
                'external_links': r.external_links,
                'has_ssl': r.has_ssl,
                'has_viewport': r.has_viewport,
                'has_schema_markup': r.has_schema_markup,
                'word_count': r.word_count,
                'critical_issues_count': len(r.critical_issues),
                'warnings_count': len(r.warnings)
            })
    
    print(f"📊 CSV exported to: {filename}")
    return filename


def main():
    """Main entry point for batch auditing"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         🔍 BATCH SEO AUDIT TOOL - By Muntasir Islam       ║
    ║               Competitor Analysis Made Easy                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("Enter URLs to audit (one per line, empty line to finish):")
    
    urls = []
    while True:
        url = input().strip()
        if not url:
            break
        urls.append(url)
    
    if not urls:
        print("No URLs provided. Exiting.")
        return
    
    # Run batch audit
    results = audit_multiple_urls(urls)
    
    if not results:
        print("No successful audits. Exiting.")
        return
    
    # Print comparison
    comparison = generate_comparison_report(results)
    print(comparison)
    
    # Export options
    print("\n📁 Export Options:")
    print("1. Export to CSV")
    print("2. Generate individual HTML reports")
    print("3. Save as JSON")
    print("4. All of the above")
    print("5. Skip")
    
    choice = input("\nChoose option (1-5): ").strip()
    
    if choice in ['1', '4']:
        export_to_csv(results)
    
    if choice in ['2', '4']:
        os.makedirs('reports', exist_ok=True)
        for r in results:
            domain = r.url.replace('https://', '').replace('http://', '').replace('/', '_')[:30]
            save_html_report(r, f"reports/{domain}.html")
    
    if choice in ['3', '4']:
        for r in results:
            save_report_json(r)
    
    print("\n✅ Batch audit complete!")


if __name__ == "__main__":
    main()
