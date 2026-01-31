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
    PageBreak, Image, HRFlowable, ListFlowable, ListItem, Flowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Wedge, Line
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from dataclasses import asdict
import math


class ScoreGauge(Flowable):
    """Custom flowable for a colorful score gauge"""
    
    def __init__(self, score, width=200, height=200):
        Flowable.__init__(self)
        self.score = score
        self.width = width
        self.height = height
        
    def draw(self):
        canvas = self.canv
        cx, cy = self.width / 2, self.height / 2
        radius = min(self.width, self.height) / 2 - 10
        
        # Determine color based on score
        if self.score >= 80:
            main_color = colors.HexColor('#10b981')  # Green
            bg_color = colors.HexColor('#d1fae5')
        elif self.score >= 60:
            main_color = colors.HexColor('#f59e0b')  # Amber
            bg_color = colors.HexColor('#fef3c7')
        elif self.score >= 40:
            main_color = colors.HexColor('#f97316')  # Orange
            bg_color = colors.HexColor('#ffedd5')
        else:
            main_color = colors.HexColor('#ef4444')  # Red
            bg_color = colors.HexColor('#fee2e2')
        
        # Draw background circle
        canvas.setFillColor(bg_color)
        canvas.setStrokeColor(colors.HexColor('#e5e7eb'))
        canvas.setLineWidth(2)
        canvas.circle(cx, cy, radius, fill=1, stroke=1)
        
        # Draw progress arc
        canvas.setStrokeColor(main_color)
        canvas.setLineWidth(12)
        start_angle = 90
        extent = -3.6 * self.score  # 360 degrees = 100%
        
        # Draw arc using wedge
        canvas.setFillColor(colors.white)
        canvas.circle(cx, cy, radius - 15, fill=1, stroke=0)
        
        # Draw colored ring
        canvas.setStrokeColor(main_color)
        canvas.setLineWidth(15)
        
        # Draw arc segments
        for i in range(int(self.score)):
            angle = math.radians(90 - i * 3.6)
            x1 = cx + (radius - 7) * math.cos(angle)
            y1 = cy + (radius - 7) * math.sin(angle)
            canvas.setFillColor(main_color)
            canvas.circle(x1, y1, 6, fill=1, stroke=0)
        
        # Draw inner white circle
        canvas.setFillColor(colors.white)
        canvas.circle(cx, cy, radius - 25, fill=1, stroke=0)
        
        # Draw score text
        canvas.setFillColor(main_color)
        canvas.setFont('Helvetica-Bold', 48)
        canvas.drawCentredString(cx, cy + 5, str(self.score))
        
        # Draw "out of 100" text
        canvas.setFillColor(colors.HexColor('#6b7280'))
        canvas.setFont('Helvetica', 12)
        canvas.drawCentredString(cx, cy - 25, 'out of 100')


class ColorfulHeader(Flowable):
    """Custom flowable for colorful header with gradient effect"""
    
    def __init__(self, width=500, height=80):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        
    def draw(self):
        canvas = self.canv
        
        # Draw gradient-like background with rectangles
        gradient_colors = [
            colors.HexColor('#6366f1'),
            colors.HexColor('#8b5cf6'),
            colors.HexColor('#a855f7'),
        ]
        
        stripe_width = self.width / len(gradient_colors)
        for i, color in enumerate(gradient_colors):
            canvas.setFillColor(color)
            canvas.rect(i * stripe_width, 0, stripe_width + 1, self.height, fill=1, stroke=0)
        
        # Draw title text
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica-Bold', 28)
        canvas.drawCentredString(self.width / 2, self.height / 2 - 5, 'SEO HEALTH REPORT')


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
        
        # Body text - use custom name to avoid conflict
        self.styles.add(ParagraphStyle(
            name='CustomBody',
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
    
    def _create_stat_card(self, label, value, text_color, bg_color):
        """Create a colorful stat card as a table"""
        card = Table([
            [Paragraph(f'<font color="{text_color}" size="28"><b>{value}</b></font>', 
                      ParagraphStyle('StatValue', alignment=TA_CENTER))],
            [Paragraph(f'<font color="{text_color}" size="10"><b>{label}</b></font>', 
                      ParagraphStyle('StatLabel', alignment=TA_CENTER))]
        ], colWidths=[150])
        card.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg_color)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, 0), 15),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('TOPPADDING', (0, 1), (-1, 1), 0),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(text_color)),
        ]))
        return card
    
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
            return f"CRITICAL: You have {count} critical issue(s) that need immediate attention. These are hurting your search rankings right now."
        elif issue_type == 'warning' and count > 0:
            return f"WARNING: You have {count} warning(s) that should be fixed soon. These could be affecting your visibility."
        elif issue_type == 'recommendation' and count > 0:
            return f"TIP: You have {count} suggestion(s) for improvement. These are nice-to-have optimizations."
        return ""
    
    def generate_pdf(self):
        """Generate the PDF report"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=30,
            bottomMargin=40
        )
        
        story = []
        r = self.result
        
        # ===== COVER PAGE =====
        # Colorful Header Banner
        story.append(ColorfulHeader(width=515, height=70))
        story.append(Spacer(1, 25))
        
        # Website info in a nice box
        url_table = Table([
            [Paragraph(f'<font color="#6366f1"><b>Website Analyzed</b></font>', self.styles['Normal'])],
            [Paragraph(f'<font color="#1e293b" size="14">{r.url}</font>', self.styles['Normal'])],
            [Paragraph(f'<font color="#64748b" size="9">Report generated on {r.audit_date}</font>', self.styles['Normal'])]
        ], colWidths=[515])
        url_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ]))
        story.append(url_table)
        story.append(Spacer(1, 30))
        
        # Score Gauge - Centered
        score_gauge = ScoreGauge(r.score, width=180, height=180)
        score_table = Table([[score_gauge]], colWidths=[515])
        score_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 15))
        
        # Grade Badge
        grade_color = self._get_score_color(r.score)
        grade_text = f'Grade: {r.grade}'
        grade_table = Table([[Paragraph(
            f'<font color="white" size="16"><b>{grade_text}</b></font>',
            ParagraphStyle('GradeBadge', alignment=TA_CENTER)
        )]], colWidths=[120])
        grade_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), grade_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ]))
        grade_wrapper = Table([[grade_table]], colWidths=[515])
        grade_wrapper.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
        story.append(grade_wrapper)
        story.append(Spacer(1, 15))
        
        # Grade explanation
        story.append(Paragraph(
            f'<font color="#475569">{self._get_grade_explanation(r.grade, r.score)}</font>',
            ParagraphStyle('GradeExplain', alignment=TA_CENTER, fontSize=12, leading=18)
        ))
        story.append(Spacer(1, 30))
        
        # Quick Stats - Colorful Cards
        stats_data = [
            [
                self._create_stat_card('PASSED', str(r.checks_passed), '#10b981', '#d1fae5'),
                self._create_stat_card('WARNINGS', str(r.checks_warnings), '#f59e0b', '#fef3c7'),
                self._create_stat_card('CRITICAL', str(r.checks_failed), '#ef4444', '#fee2e2'),
            ]
        ]
        
        stats_table = Table(stats_data, colWidths=[165, 165, 165])
        stats_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(stats_table)
        
        story.append(PageBreak())
        
        # ===== EXECUTIVE SUMMARY =====
        story.append(Paragraph('<font color="#6366f1"><b>EXECUTIVE SUMMARY</b></font>', 
                              ParagraphStyle('SectionHead', fontSize=16, spaceAfter=10)))
        story.append(Paragraph(
            "This section provides a quick overview of your website's SEO health in plain English.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 10))
        
        # What's Working Well - Green header
        working_header = Table([[Paragraph('<font color="white"><b>WHAT\'S WORKING WELL</b></font>', 
                                          ParagraphStyle('GreenHeader', alignment=TA_LEFT, fontSize=11))]], 
                               colWidths=[515])
        working_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#10b981')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(working_header)
        story.append(Spacer(1, 5))
        
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
                story.append(Paragraph(f'<font color="#10b981"><b>+</b></font> {item}', self.styles['CustomBody']))
        else:
            story.append(Paragraph('<font color="#10b981"><b>+</b></font> Your website has potential - let\'s work on improvements!', self.styles['CustomBody']))
        
        story.append(Spacer(1, 15))
        
        # What Needs Attention - Orange/Red header
        attention_header = Table([[Paragraph('<font color="white"><b>WHAT NEEDS ATTENTION</b></font>', 
                                            ParagraphStyle('OrangeHeader', alignment=TA_LEFT, fontSize=11))]], 
                                 colWidths=[515])
        attention_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f59e0b')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(attention_header)
        story.append(Spacer(1, 5))
        
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
                story.append(Paragraph(f'<font color="#f59e0b"><b>!</b></font> {item}', self.styles['CustomBody']))
        else:
            story.append(Paragraph('<font color="#10b981"><b>+</b></font> Great job! No major issues found.', self.styles['CustomBody']))
        
        story.append(PageBreak())
        
        # ===== CATEGORY SCORES =====
        story.append(Paragraph('<font color="#6366f1"><b>SCORE BREAKDOWN BY CATEGORY</b></font>', 
                              ParagraphStyle('SectionHead2', fontSize=16, spaceAfter=10)))
        story.append(Paragraph(
            "See how your website performs in different areas. Higher scores are better (out of 100).",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 15))
        
        # Category scores table with explanations - no emojis
        categories_data = [
            ['Category', 'Score', 'Status', 'What This Means'],
            ['Page Information', f'{r.meta_tags_score}/100', self._get_status_text(r.meta_tags_score), 'Title & description for search results'],
            ['Content Quality', f'{r.content_score}/100', self._get_status_text(r.content_score), 'How good your written content is'],
            ['Technical Setup', f'{r.technical_seo_score}/100', self._get_status_text(r.technical_seo_score), 'Behind-the-scenes optimization'],
            ['Mobile Experience', f'{r.ux_score}/100', self._get_status_text(r.ux_score), 'How well it works on phones'],
            ['Links', f'{r.links_score}/100', self._get_status_text(r.links_score), 'Internal & external linking'],
            ['Images', f'{r.images_score}/100', self._get_status_text(r.images_score), 'Image optimization'],
            ['Security', f'{r.security_headers_score}/100', self._get_status_text(r.security_headers_score), 'Website security setup'],
            ['Accessibility', f'{r.accessibility_score}/100', self._get_status_text(r.accessibility_score), 'Usability for all visitors'],
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
        story.append(Paragraph('<font color="#6366f1"><b>DETAILED FINDINGS</b></font>', 
                              ParagraphStyle('SectionHead3', fontSize=16, spaceAfter=10)))
        
        # Page Title & Description
        title_header = Table([[Paragraph('<font color="white"><b>PAGE TITLE &amp; DESCRIPTION</b></font>', 
                                        ParagraphStyle('BlueHeader', alignment=TA_LEFT, fontSize=11))]], 
                            colWidths=[515])
        title_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#3b82f6')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(title_header)
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            "Your page title and description appear in search results. They're like a mini-advertisement for your page.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 8))
        
        title_data = [
            ['Element', 'Your Value', 'Status'],
            ['Page Title', (r.title[:50] + '...' if r.title and len(r.title) > 50 else r.title) or 'Missing', 
             'Good' if r.title and 30 <= len(r.title) <= 60 else 'Needs Work'],
            ['Title Length', f'{r.title_length} characters', 
             'Good' if 30 <= r.title_length <= 60 else 'Adjust'],
            ['Page Description', (r.meta_description[:50] + '...' if r.meta_description and len(r.meta_description) > 50 else r.meta_description) or 'Missing',
             'Good' if r.meta_description and 120 <= len(r.meta_description) <= 160 else 'Needs Work'],
            ['Description Length', f'{r.meta_description_length} characters',
             'Good' if 120 <= r.meta_description_length <= 160 else 'Adjust'],
        ]
        
        title_table = Table(title_data, colWidths=[120, 250, 100])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(title_table)
        
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            "<b>Tip:</b> Keep titles between 30-60 characters and descriptions between 120-160 characters for best display in search results.",
            self.styles['Explanation']
        ))
        
        story.append(Spacer(1, 20))
        
        # Content Analysis
        content_header = Table([[Paragraph('<font color="white"><b>CONTENT ANALYSIS</b></font>', 
                                          ParagraphStyle('PurpleHeader', alignment=TA_LEFT, fontSize=11))]], 
                              colWidths=[515])
        content_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#8b5cf6')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(content_header)
        story.append(Spacer(1, 5))
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
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(content_table)
        
        story.append(Spacer(1, 20))
        
        # Technical Checklist
        tech_header = Table([[Paragraph('<font color="white"><b>TECHNICAL CHECKLIST</b></font>', 
                                       ParagraphStyle('TealHeader', alignment=TA_LEFT, fontSize=11))]], 
                           colWidths=[515])
        tech_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0d9488')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(tech_header)
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            "These technical elements help search engines understand and trust your website.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 8))
        
        tech_checks = [
            ['Check', 'Status', 'Why It Matters'],
            ['Secure Connection (HTTPS)', 'YES' if r.has_ssl else 'NO', 'Required for trust & rankings'],
            ['Mobile-Ready', 'YES' if r.has_viewport else 'NO', 'Most searches are on mobile'],
            ['Page Language Set', 'YES' if r.html_lang else 'NO', 'Helps with language targeting'],
            ['Favicon (Site Icon)', 'YES' if r.has_favicon else 'NO', 'Branding in browser tabs'],
            ['Canonical URL', 'YES' if r.canonical_url else 'NO', 'Prevents duplicate content'],
            ['Structured Data', 'YES' if r.has_schema_markup else 'NO', 'Enhanced search results'],
        ]
        
        tech_table = Table(tech_checks, colWidths=[150, 80, 240])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(tech_table)
        
        story.append(PageBreak())
        
        # ===== ACTION PLAN =====
        action_header = Table([[Paragraph('<font color="white"><b>YOUR ACTION PLAN</b></font>', 
                                         ParagraphStyle('ActionHeader', alignment=TA_LEFT, fontSize=14))]], 
                             colWidths=[515])
        action_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#6366f1')),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(action_header)
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            "Here's what to focus on to improve your SEO, listed in order of importance.",
            self.styles['Explanation']
        ))
        story.append(Spacer(1, 15))
        
        # Priority 1: Critical Issues
        if r.critical_issues:
            critical_header = Table([[Paragraph('<font color="white"><b>PRIORITY 1: FIX THESE FIRST (CRITICAL)</b></font>', 
                                               ParagraphStyle('CriticalHead', alignment=TA_LEFT, fontSize=10))]], 
                                   colWidths=[515])
            critical_header.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dc2626')),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(critical_header)
            story.append(Spacer(1, 3))
            story.append(Paragraph(
                "These issues are likely hurting your search rankings right now.",
                self.styles['Explanation']
            ))
            story.append(Spacer(1, 8))
            
            for i, issue in enumerate(r.critical_issues[:8], 1):
                story.append(Paragraph(
                    f"<b>{i}.</b> {self._format_issue_for_non_technical(issue)}",
                    self.styles['CustomBody']
                ))
            story.append(Spacer(1, 15))
        
        # Priority 2: Warnings
        if r.warnings:
            warning_header = Table([[Paragraph('<font color="white"><b>PRIORITY 2: ADDRESS SOON (WARNINGS)</b></font>', 
                                              ParagraphStyle('WarningHead', alignment=TA_LEFT, fontSize=10))]], 
                                  colWidths=[515])
            warning_header.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f97316')),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(warning_header)
            story.append(Spacer(1, 3))
            story.append(Paragraph(
                "These could be affecting your visibility and should be fixed when possible.",
                self.styles['Explanation']
            ))
            story.append(Spacer(1, 8))
            
            for i, warning in enumerate(r.warnings[:8], 1):
                story.append(Paragraph(
                    f"<b>{i}.</b> {self._format_issue_for_non_technical(warning)}",
                    self.styles['CustomBody']
                ))
            story.append(Spacer(1, 15))
        
        # Priority 3: Recommendations
        if r.recommendations:
            rec_header = Table([[Paragraph('<font color="white"><b>PRIORITY 3: NICE TO HAVE (SUGGESTIONS)</b></font>', 
                                          ParagraphStyle('RecHead', alignment=TA_LEFT, fontSize=10))]], 
                              colWidths=[515])
            rec_header.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#22c55e')),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(rec_header)
            story.append(Spacer(1, 3))
            story.append(Paragraph(
                "These are optimizations that can give you an extra edge over competitors.",
                self.styles['Explanation']
            ))
            story.append(Spacer(1, 8))
            
            for i, rec in enumerate(r.recommendations[:6], 1):
                story.append(Paragraph(
                    f"<b>{i}.</b> {self._format_issue_for_non_technical(rec)}",
                    self.styles['CustomBody']
                ))
        
        story.append(PageBreak())
        
        # ===== GLOSSARY =====
        glossary_header = Table([[Paragraph('<font color="white"><b>SEO GLOSSARY</b></font>', 
                                           ParagraphStyle('GlossaryHead', alignment=TA_LEFT, fontSize=14))]], 
                               colWidths=[515])
        glossary_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(glossary_header)
        story.append(Spacer(1, 5))
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
            return 'GREAT'
        elif score >= 60:
            return 'GOOD'
        elif score >= 40:
            return 'FAIR'
        else:
            return 'NEEDS WORK'
    
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
