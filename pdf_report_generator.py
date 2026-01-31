"""
SEO Audit PDF Report Generator - Easy-to-Understand Reports
Generates professional, non-technical friendly PDF reports
Author: Muntasir Islam
Version: 3.0
"""

from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Circle
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from dataclasses import asdict


class SEOPDFReportGenerator:
    """Generate beautiful, non-technical friendly PDF reports"""
    
    def __init__(self, result):
        self.result = result
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#334155'),
            spaceBefore=20,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection header
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#475569'),
            spaceBefore=15,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#334155'),
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            leading=16
        ))
        
        # Explanation text (simpler language)
        self.styles.add(ParagraphStyle(
            name='Explanation',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=6,
            fontStyle='italic',
            leading=14
        ))
        
        # Good status
        self.styles.add(ParagraphStyle(
            name='StatusGood',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#16a34a'),
            fontName='Helvetica-Bold'
        ))
        
        # Warning status
        self.styles.add(ParagraphStyle(
            name='StatusWarning',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#ca8a04'),
            fontName='Helvetica-Bold'
        ))
        
        # Bad status
        self.styles.add(ParagraphStyle(
            name='StatusBad',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#dc2626'),
            fontName='Helvetica-Bold'
        ))
        
        # Score display
        self.styles.add(ParagraphStyle(
            name='ScoreDisplay',
            parent=self.styles['Normal'],
            fontSize=48,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
    def _get_score_color(self, score):
        """Get color based on score"""
        if score >= 80:
            return colors.HexColor('#16a34a')  # Green
        elif score >= 60:
            return colors.HexColor('#ca8a04')  # Yellow
        elif score >= 40:
            return colors.HexColor('#ea580c')  # Orange
        else:
            return colors.HexColor('#dc2626')  # Red
    
    def _get_grade_explanation(self, grade, score):
        """Get human-friendly grade explanation"""
        explanations = {
            'A+': "Excellent! Your website is very well optimized for search engines.",
            'A': "Great job! Your website has strong SEO foundations with minor improvements possible.",
            'B': "Good work! Your website is doing well but has room for improvement.",
            'C': "Fair performance. Several areas need attention to improve search visibility.",
            'D': "Needs work. Your website has significant SEO issues that should be addressed.",
            'F': "Critical attention needed. Major SEO problems are hurting your search visibility."
        }
        return explanations.get(grade, "Your website needs SEO improvements.")
    
    def _create_score_visual(self, score, size=120):
        """Create a visual score circle"""
        drawing = Drawing(size, size)
        
        # Background circle
        drawing.add(Circle(size/2, size/2, size/2-5, 
                          fillColor=colors.HexColor('#f1f5f9'),
                          strokeColor=colors.HexColor('#e2e8f0'),
                          strokeWidth=2))
        
        # Score color circle (partial based on score)
        score_color = self._get_score_color(score)
        drawing.add(Circle(size/2, size/2, size/2-10,
                          fillColor=colors.white,
                          strokeColor=score_color,
                          strokeWidth=8))
        
        # Score text
        drawing.add(String(size/2, size/2+5, str(score),
                          fontSize=32, fillColor=score_color,
                          textAnchor='middle', fontName='Helvetica-Bold'))
        
        drawing.add(String(size/2, size/2-18, 'out of 100',
                          fontSize=10, fillColor=colors.HexColor('#64748b'),
                          textAnchor='middle'))
        
        return drawing
    
    def _create_category_bar_chart(self):
        """Create a bar chart of category scores"""
        r = self.result
        
        categories = [
            ('Meta', r.meta_tags_score),
            ('Content', r.content_score),
            ('Technical', r.technical_seo_score),
            ('Mobile', r.ux_score),
            ('Links', r.links_score),
            ('Images', r.images_score),
        ]
        
        drawing = Drawing(400, 200)
        
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 320
        bc.data = [[score for _, score in categories]]
        bc.strokeColor = colors.white
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 100
        bc.valueAxis.valueStep = 20
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = -5
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = [name for name, _ in categories]
        bc.bars[0].fillColor = colors.HexColor('#6366f1')
        
        drawing.add(bc)
        return drawing
    
    def _format_issue_for_non_technical(self, issue):
        """Convert technical issues to simple language"""
        # Common translations
        translations = {
            'meta description': 'page summary',
            'canonical': 'main page link',
            'alt text': 'image description',
            'H1': 'main heading',
            'H2': 'sub-heading',
            'SSL': 'security certificate',
            'HTTPS': 'secure connection',
            'viewport': 'mobile display settings',
            'schema': 'structured information',
            'robots': 'search engine instructions',
            'hreflang': 'language tags',
            'nofollow': 'link instruction',
            'noindex': 'hide from search',
            'sitemap': 'page list for search engines',
            'crawl': 'search engine scan',
            'index': 'add to search results',
        }
        
        result = issue
        for tech_term, simple_term in translations.items():
            result = result.lower().replace(tech_term.lower(), simple_term)
        
        return result.capitalize()
    
    def _what_this_means(self, category):
        """Explain what each category means in simple terms"""
        explanations = {
            'meta': "These are hidden tags that tell search engines what your page is about. Think of them as a book's summary on the back cover.",
            'content': "This measures how well-written and organized your content is. Good content helps visitors and search engines understand your page.",
            'technical': "These are behind-the-scenes settings that help search engines find and understand your website properly.",
            'mobile': "This shows how well your website works on phones and tablets. Most people browse on mobile devices now.",
            'links': "Links connect your pages together and to other websites. Good linking helps visitors and search engines navigate.",
            'images': "Images need descriptions (alt text) so search engines know what they show. This also helps visually impaired visitors.",
            'security': "Security protects your visitors' information. Secure websites rank better in search results.",
            'speed': "How fast your website loads. Faster websites rank better and keep visitors happy.",
            'crawling': "Whether search engines can find and access all your important pages.",
            'keywords': "How well your target keywords are placed throughout your content.",
        }
        return explanations.get(category, "This helps search engines understand and rank your website better.")
    
    def _priority_action(self, issue_type, count):
        """Generate priority action based on issue type"""
        if issue_type == 'critical' and count > 0:
            return f"🚨 You have {count} critical issue(s) that need immediate attention. These are hurting your search rankings right now."
        elif issue_type == 'warning' and count > 0:
            return f"⚠️ You have {count} warning(s) that should be fixed soon. These could be affecting your visibility."
        elif issue_type == 'recommendation' and count > 0:
            return f"💡 You have {count} suggestion(s) for improvement. These are nice-to-have optimizations."
        return ""
    
    def generate_pdf(self):
        """Generate the PDF report"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        story = []
        r = self.result
        
        # ===== COVER PAGE =====
        story.append(Spacer(1, 50))
        story.append(Paragraph("🔍 SEO Health Report", self.styles['ReportTitle']))
        story.append(Spacer(1, 20))
        
        # URL
        story.append(Paragraph(f"<b>Website:</b> {r.url}", self.styles['BodyText']))
        story.append(Paragraph(f"<b>Report Date:</b> {r.audit_date}", self.styles['BodyText']))
        story.append(Spacer(1, 30))
        
        # Main Score
        score_color = self._get_score_color(r.score)
        story.append(Paragraph(
            f'<font color="{score_color.hexval()}" size="72"><b>{r.score}</b></font>',
            ParagraphStyle('BigScore', alignment=TA_CENTER)
        ))
        story.append(Paragraph(
            f'<font color="{score_color.hexval()}" size="24">Grade: {r.grade}</font>',
            ParagraphStyle('Grade', alignment=TA_CENTER)
        ))
        story.append(Spacer(1, 20))
        
        # Grade explanation
        story.append(Paragraph(
            self._get_grade_explanation(r.grade, r.score),
            ParagraphStyle('GradeExplain', parent=self.styles['BodyText'], 
                          alignment=TA_CENTER, fontSize=14)
        ))
        
        story.append(Spacer(1, 40))
        
        # Quick Stats Table
        quick_stats = [
            ['✅ Passed Checks', '⚠️ Warnings', '❌ Critical Issues'],
            [str(r.checks_passed), str(r.checks_warnings), str(r.checks_failed)]
        ]
        
        stats_table = Table(quick_stats, colWidths=[150, 150, 150])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#334155')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, 1), 24),
            ('TEXTCOLOR', (0, 1), (0, 1), colors.HexColor('#16a34a')),
            ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor('#ca8a04')),
            ('TEXTCOLOR', (2, 1), (2, 1), colors.HexColor('#dc2626')),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, 1), 15),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 15),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ]))
        story.append(stats_table)
        
        story.append(PageBreak())
        
        # ===== EXECUTIVE SUMMARY =====
        story.append(Paragraph("📋 Executive Summary", self.styles['SectionHeader']))
        story.append(Paragraph(
            "This section provides a quick overview of your website's SEO health in plain English.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 10))
        
        # What's Working Well
        story.append(Paragraph("✅ What's Working Well", self.styles['SubHeader']))
        
        good_items = []
        if r.has_ssl:
            good_items.append("Your website uses secure HTTPS connection (the padlock in browsers)")
        if r.title and 30 <= r.title_length <= 60:
            good_items.append("Your page title is well-optimized for search engines")
        if r.meta_description and 120 <= r.meta_description_length <= 160:
            good_items.append("Your page description is a good length for search results")
        if r.h1_count == 1:
            good_items.append("Your page has a proper main heading structure")
        if r.has_viewport:
            good_items.append("Your website is set up for mobile devices")
        if r.images_without_alt == 0 and r.total_images > 0:
            good_items.append("All your images have descriptions for accessibility")
        if r.word_count >= 300:
            good_items.append(f"Your page has substantial content ({r.word_count} words)")
        if r.has_schema_markup:
            good_items.append("Your page uses structured data to enhance search results")
        
        if good_items:
            for item in good_items[:6]:
                story.append(Paragraph(f"• {item}", self.styles['BodyText']))
        else:
            story.append(Paragraph("• Your website has potential - let's work on improvements!", self.styles['BodyText']))
        
        story.append(Spacer(1, 15))
        
        # What Needs Attention
        story.append(Paragraph("⚠️ What Needs Attention", self.styles['SubHeader']))
        
        attention_items = []
        if not r.has_ssl:
            attention_items.append("Your website needs a security certificate (HTTPS) - this is essential for rankings")
        if not r.title or r.title_length < 30:
            attention_items.append("Your page title is missing or too short - this is crucial for search visibility")
        if not r.meta_description:
            attention_items.append("Add a page description - this appears in search results and encourages clicks")
        if r.h1_count == 0:
            attention_items.append("Add a main heading (H1) to your page - it tells search engines your main topic")
        elif r.h1_count > 1:
            attention_items.append("You have multiple main headings - use only one H1 per page")
        if r.images_without_alt > 0:
            attention_items.append(f"Add descriptions to {r.images_without_alt} image(s) - this helps accessibility and SEO")
        if r.word_count < 300:
            attention_items.append("Add more content - pages with more useful content tend to rank better")
        if not r.canonical_url:
            attention_items.append("Add a canonical URL - this prevents duplicate content issues")
        
        if attention_items:
            for item in attention_items[:6]:
                story.append(Paragraph(f"• {item}", self.styles['BodyText']))
        else:
            story.append(Paragraph("• Great job! No major issues found.", self.styles['BodyText']))
        
        story.append(PageBreak())
        
        # ===== CATEGORY SCORES =====
        story.append(Paragraph("📊 Score Breakdown by Category", self.styles['SectionHeader']))
        story.append(Paragraph(
            "See how your website performs in different areas. Higher scores are better (out of 100).",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 15))
        
        # Category scores table with explanations
        categories_data = [
            ['Category', 'Score', 'Status', 'What This Means'],
            ['📋 Page Information', f'{r.meta_tags_score}/100', self._get_status_text(r.meta_tags_score), 'Title & description for search results'],
            ['📝 Content Quality', f'{r.content_score}/100', self._get_status_text(r.content_score), 'How good your written content is'],
            ['⚙️ Technical Setup', f'{r.technical_seo_score}/100', self._get_status_text(r.technical_seo_score), 'Behind-the-scenes optimization'],
            ['📱 Mobile Experience', f'{r.ux_score}/100', self._get_status_text(r.ux_score), 'How well it works on phones'],
            ['🔗 Links', f'{r.links_score}/100', self._get_status_text(r.links_score), 'Internal & external linking'],
            ['🖼️ Images', f'{r.images_score}/100', self._get_status_text(r.images_score), 'Image optimization'],
            ['🔒 Security', f'{r.security_headers_score}/100', self._get_status_text(r.security_headers_score), 'Website security setup'],
            ['♿ Accessibility', f'{r.accessibility_score}/100', self._get_status_text(r.accessibility_score), 'Usability for all visitors'],
        ]
        
        cat_table = Table(categories_data, colWidths=[120, 70, 80, 180])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(cat_table)
        
        story.append(PageBreak())
        
        # ===== DETAILED FINDINGS =====
        story.append(Paragraph("🔍 Detailed Findings", self.styles['SectionHeader']))
        
        # Page Title & Description
        story.append(Paragraph("📋 Page Title & Description", self.styles['SubHeader']))
        story.append(Paragraph(
            "Your page title and description appear in search results. They're like a mini-advertisement for your page.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 8))
        
        title_data = [
            ['Element', 'Your Value', 'Status'],
            ['Page Title', (r.title[:50] + '...' if r.title and len(r.title) > 50 else r.title) or 'Missing', 
             '✅ Good' if r.title and 30 <= len(r.title) <= 60 else '⚠️ Needs Work'],
            ['Title Length', f'{r.title_length} characters', 
             '✅ Good' if 30 <= r.title_length <= 60 else '⚠️ Adjust'],
            ['Page Description', (r.meta_description[:50] + '...' if r.meta_description and len(r.meta_description) > 50 else r.meta_description) or 'Missing',
             '✅ Good' if r.meta_description and 120 <= len(r.meta_description) <= 160 else '⚠️ Needs Work'],
            ['Description Length', f'{r.meta_description_length} characters',
             '✅ Good' if 120 <= r.meta_description_length <= 160 else '⚠️ Adjust'],
        ]
        
        title_table = Table(title_data, colWidths=[120, 250, 100])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(title_table)
        
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            "<b>Tip:</b> Keep titles between 30-60 characters and descriptions between 120-160 characters for best display in search results.",
            self.styles['Explanation']
        ))
        
        story.append(Spacer(1, 20))
        
        # Content Analysis
        story.append(Paragraph("📝 Content Analysis", self.styles['SubHeader']))
        story.append(Paragraph(
            "Search engines love helpful, well-written content. Here's how your content measures up.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 8))
        
        content_data = [
            ['Metric', 'Your Value', 'What It Means'],
            ['Word Count', str(r.word_count), 'More content usually ranks better (aim for 300+ words)'],
            ['Reading Level', r.readability_status, 'How easy your content is to read'],
            ['Main Headings (H1)', str(r.h1_count), 'Should be exactly 1 per page'],
            ['Sub-headings (H2-H6)', str(r.h2_count + r.h3_count + r.h4_count), 'Help organize your content'],
            ['Paragraphs', str(r.paragraph_count), 'Break up text for easy reading'],
        ]
        
        content_table = Table(content_data, colWidths=[120, 100, 250])
        content_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(content_table)
        
        story.append(Spacer(1, 20))
        
        # Technical Checklist
        story.append(Paragraph("⚙️ Technical Checklist", self.styles['SubHeader']))
        story.append(Paragraph(
            "These technical elements help search engines understand and trust your website.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 8))
        
        tech_checks = [
            ['Check', 'Status', 'Why It Matters'],
            ['Secure Connection (HTTPS)', '✅ Yes' if r.has_ssl else '❌ No', 'Required for trust & rankings'],
            ['Mobile-Ready', '✅ Yes' if r.has_viewport else '❌ No', 'Most searches are on mobile'],
            ['Page Language Set', '✅ Yes' if r.html_lang else '❌ No', 'Helps with language targeting'],
            ['Favicon (Site Icon)', '✅ Yes' if r.has_favicon else '❌ No', 'Branding in browser tabs'],
            ['Canonical URL', '✅ Yes' if r.canonical_url else '❌ No', 'Prevents duplicate content'],
            ['Structured Data', '✅ Yes' if r.has_schema_markup else '❌ No', 'Enhanced search results'],
        ]
        
        tech_table = Table(tech_checks, colWidths=[150, 80, 240])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(tech_table)
        
        story.append(PageBreak())
        
        # ===== ACTION PLAN =====
        story.append(Paragraph("🎯 Your Action Plan", self.styles['SectionHeader']))
        story.append(Paragraph(
            "Here's what to focus on to improve your SEO, listed in order of importance.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 15))
        
        # Priority 1: Critical Issues
        if r.critical_issues:
            story.append(Paragraph("🚨 Priority 1: Fix These First (Critical)", self.styles['SubHeader']))
            story.append(Paragraph(
                "These issues are likely hurting your search rankings right now.",
                self.styles['Explanation']
            ))
            story.append(Spacer(1, 8))
            
            for i, issue in enumerate(r.critical_issues[:8], 1):
                story.append(Paragraph(
                    f"<b>{i}.</b> {self._format_issue_for_non_technical(issue)}",
                    self.styles['BodyText']
                ))
            story.append(Spacer(1, 15))
        
        # Priority 2: Warnings
        if r.warnings:
            story.append(Paragraph("⚠️ Priority 2: Address Soon (Warnings)", self.styles['SubHeader']))
            story.append(Paragraph(
                "These could be affecting your visibility and should be fixed when possible.",
                self.styles['Explanation']
            ))
            story.append(Spacer(1, 8))
            
            for i, warning in enumerate(r.warnings[:8], 1):
                story.append(Paragraph(
                    f"<b>{i}.</b> {self._format_issue_for_non_technical(warning)}",
                    self.styles['BodyText']
                ))
            story.append(Spacer(1, 15))
        
        # Priority 3: Recommendations
        if r.recommendations:
            story.append(Paragraph("💡 Priority 3: Nice to Have (Suggestions)", self.styles['SubHeader']))
            story.append(Paragraph(
                "These are optimizations that can give you an extra edge over competitors.",
                self.styles['Explanation']
            ))
            story.append(Spacer(1, 8))
            
            for i, rec in enumerate(r.recommendations[:6], 1):
                story.append(Paragraph(
                    f"<b>{i}.</b> {self._format_issue_for_non_technical(rec)}",
                    self.styles['BodyText']
                ))
        
        story.append(PageBreak())
        
        # ===== GLOSSARY =====
        story.append(Paragraph("📚 SEO Glossary", self.styles['SectionHeader']))
        story.append(Paragraph(
            "Common SEO terms explained in plain English.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 15))
        
        glossary = [
            ['Term', 'Simple Explanation'],
            ['SEO', 'Search Engine Optimization - making your site easier to find on Google'],
            ['Meta Title', 'The clickable headline that appears in search results'],
            ['Meta Description', 'The summary text below your title in search results'],
            ['H1, H2, H3...', 'Headings that organize your content (H1 is most important)'],
            ['Alt Text', 'A description of an image for search engines and blind users'],
            ['HTTPS/SSL', 'Security that encrypts data - shows as a padlock in browsers'],
            ['Canonical URL', 'Tells search engines which version of a page is the "main" one'],
            ['Schema/Structured Data', 'Code that helps search engines understand your content better'],
            ['Mobile-Friendly', 'Website works well on phones and tablets'],
            ['Page Speed', 'How fast your website loads - faster is better'],
            ['Backlinks', 'Links from other websites pointing to yours (like votes of trust)'],
            ['Indexing', 'When search engines add your page to their database'],
            ['Crawling', 'When search engines scan your website to find content'],
        ]
        
        glossary_table = Table(glossary, colWidths=[120, 350])
        glossary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(glossary_table)
        
        story.append(Spacer(1, 30))
        
        # Footer
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e2e8f0')))
        story.append(Spacer(1, 15))
        story.append(Paragraph(
            f"Report generated by Advanced SEO Audit Tool v3.0 | {datetime.now().strftime('%B %d, %Y')}",
            ParagraphStyle('Footer', parent=self.styles['Normal'], 
                          fontSize=9, textColor=colors.HexColor('#94a3b8'), alignment=TA_CENTER)
        ))
        story.append(Paragraph(
            "Created by Muntasir Islam | 300+ SEO Parameters Analyzed",
            ParagraphStyle('Footer2', parent=self.styles['Normal'],
                          fontSize=9, textColor=colors.HexColor('#94a3b8'), alignment=TA_CENTER)
        ))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _get_status_text(self, score):
        """Get status text based on score"""
        if score >= 80:
            return '✅ Great'
        elif score >= 60:
            return '⚠️ Good'
        elif score >= 40:
            return '⚠️ Fair'
        else:
            return '❌ Needs Work'
    
    def save_pdf(self, filepath):
        """Save PDF to file"""
        buffer = self.generate_pdf()
        with open(filepath, 'wb') as f:
            f.write(buffer.read())
        print(f"PDF report saved to: {filepath}")
        return filepath


def generate_pdf_report(result, output_path=None):
    """
    Convenience function to generate PDF reports
    
    Args:
        result: SEOAuditResult from audit
        output_path: Path to save the PDF (optional)
    
    Returns:
        BytesIO buffer if no output_path, else saves to file
    """
    generator = SEOPDFReportGenerator(result)
    
    if output_path:
        return generator.save_pdf(output_path)
    else:
        return generator.generate_pdf()


if __name__ == "__main__":
    # Example usage
    from seo_auditor import AdvancedSEOAuditor
    
    url = "https://example.com"
    auditor = AdvancedSEOAuditor(url)
    result = auditor.run_audit()
    
    if result:
        generate_pdf_report(result, "seo_report.pdf")
