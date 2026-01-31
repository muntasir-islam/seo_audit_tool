# 🔍 Advanced SEO Audit Tool - 200+ Parameters

An enterprise-grade, comprehensive SEO audit tool that analyzes **200+ SEO parameters** for any website. Built with Python and Streamlit, this tool provides detailed insights across 14 major SEO categories.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 🎯 200+ SEO Parameters Analyzed

This tool checks over 200 individual SEO parameters organized into 14 comprehensive categories:

| Category | Parameters | Description |
|----------|------------|-------------|
| 📋 Meta Tags | 20+ | Title, description, canonical, robots, viewport |
| 🌐 Open Graph | 15+ | OG title, description, image, URL, type, locale |
| 🐦 Twitter Cards | 12+ | Card type, title, description, image, creator |
| 📝 Headings | 20+ | H1-H6 structure, hierarchy, duplicates, empty tags |
| 🖼️ Images | 25+ | Alt text, lazy loading, srcset, formats, optimization |
| 🔗 Links | 30+ | Internal/external, nofollow, noopener, anchor text |
| ⚙️ Technical SEO | 40+ | SSL, viewport, schema, resources, security headers |
| 📖 Content | 35+ | Word count, readability, keywords, text/HTML ratio |
| 📱 Mobile & UX | 15+ | Mobile-friendly, viewport, touch icons, AMP |
| 🌍 Internationalization | 10+ | Hreflang, language detection, x-default |
| 🛒 E-commerce | 15+ | Product schema, breadcrumbs, reviews, rich snippets |
| ♿ Accessibility | 15+ | ARIA, landmarks, skip links, form labels |
| ⚡ Performance | 10+ | Preload, preconnect, DNS prefetch, resource hints |
| 🔒 Security | 8+ | HSTS, CSP, X-Frame-Options, XSS protection |

### 📊 Scoring System

- **Overall Score**: 0-100 based on weighted category scores
- **Letter Grades**: A+ (95-100), A (90-94), B (80-89), C (70-79), D (60-69), F (<60)
- **Category Scores**: Individual scores for each of the 14 categories
- **Issue Classification**: Critical issues, warnings, and recommendations

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/seo_audit_tool.git
cd seo_audit_tool

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Web App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Command Line Usage

#### Single URL Audit
```python
from seo_auditor import AdvancedSEOAuditor

# Basic audit
auditor = AdvancedSEOAuditor("https://example.com")
result = auditor.run_audit()

# With target keyword
auditor = AdvancedSEOAuditor("https://example.com", target_keyword="seo tools")
result = auditor.run_audit()

# Print results
print(f"Score: {result.score}/100 (Grade: {result.grade})")
print(f"Critical Issues: {len(result.critical_issues)}")
```

#### Generate Reports
```python
from seo_auditor import AdvancedSEOAuditor
from report_generator import AdvancedReportGenerator

# Run audit
auditor = AdvancedSEOAuditor("https://example.com")
result = auditor.run_audit()

# Generate HTML report
generator = AdvancedReportGenerator(result)
generator.save_html_report("seo_report.html")

# Generate JSON report
generator.save_json_report("seo_report.json")
```

#### Batch Audit
```bash
# Audit multiple URLs
python batch_audit.py -u https://site1.com https://site2.com

# From file
python batch_audit.py -f urls.txt -k "target keyword" -o reports

# Parallel processing
python batch_audit.py -f urls.txt --parallel -w 5
```

## 📁 Project Structure

```
seo_audit_tool/
├── seo_auditor.py       # Core audit engine (200+ parameters)
├── streamlit_app.py     # Web interface
├── report_generator.py  # HTML/JSON report generation
├── batch_audit.py       # Batch URL processing
├── requirements.txt     # Dependencies
├── README.md           # Documentation
└── deploy/             # Deployment configs
```

## 🔍 Full Parameter List

### 📋 Meta Tags (20+ Parameters)
- `title` - Page title text
- `title_length` - Character count
- `title_pixel_width` - Estimated SERP pixel width
- `title_has_numbers` - Contains numbers (engagement)
- `title_has_power_words` - Contains power words
- `title_has_keyword` - Contains target keyword
- `title_starts_with_keyword` - Keyword position
- `meta_description` - Meta description text
- `meta_description_length` - Character count
- `meta_description_has_cta` - Call-to-action presence
- `meta_description_has_keyword` - Keyword presence
- `meta_description_unique` - Uniqueness check
- `canonical_url` - Canonical URL
- `canonical_is_self` - Self-referencing canonical
- `robots_meta` - Robots meta directive
- `robots_index` - Index directive
- `robots_follow` - Follow directive
- `meta_keywords` - Meta keywords (legacy)
- `meta_author` - Author meta tag
- `meta_generator` - Generator meta tag

### 🌐 Open Graph (15+ Parameters)
- `og_title` - OG title
- `og_description` - OG description
- `og_image` - OG image URL
- `og_image_width` - Image width
- `og_image_height` - Image height
- `og_url` - OG URL
- `og_type` - Content type
- `og_site_name` - Site name
- `og_locale` - Locale
- `og_locale_alternate` - Alternate locales
- `og_video` - Video URL
- `og_audio` - Audio URL
- `og_score` - Completeness score

### 🐦 Twitter Cards (12+ Parameters)
- `twitter_card` - Card type
- `twitter_title` - Title
- `twitter_description` - Description
- `twitter_image` - Image URL
- `twitter_image_alt` - Image alt text
- `twitter_site` - Site handle
- `twitter_creator` - Creator handle
- `twitter_player` - Player URL
- `twitter_score` - Completeness score

### 📝 Headings (20+ Parameters)
- `h1_count` - Number of H1 tags
- `h1_tags` - H1 text content
- `h1_length` - Average H1 length
- `h1_has_keyword` - Keyword in H1
- `h2_count` through `h6_count` - Heading counts
- `h2_tags` - H2 text content
- `total_headings` - Total heading count
- `heading_hierarchy_valid` - Proper nesting
- `empty_headings` - Empty heading tags
- `duplicate_headings` - Duplicate content
- `headings_with_keywords` - Keyword presence
- `heading_structure_status` - Structure assessment

### 🖼️ Images (25+ Parameters)
- `total_images` - Image count
- `images_without_alt` - Missing alt text
- `images_with_empty_alt` - Empty alt attribute
- `images_with_alt_keyword` - Keyword in alt
- `images_with_lazy_loading` - Lazy loading
- `images_with_srcset` - Responsive images
- `images_with_sizes` - Sizes attribute
- `images_in_picture` - Picture element
- `images_webp` - WebP format
- `images_png` - PNG format
- `images_jpg` - JPEG format
- `images_svg` - SVG format
- `images_gif` - GIF format
- `images_external` - External images
- `images_with_dimensions` - Width/height set
- `avg_alt_length` - Average alt text length
- `longest_alt` - Maximum alt length
- `images_score` - Overall image score

### 🔗 Links (30+ Parameters)
- `total_links` - Total link count
- `internal_links` - Internal link count
- `external_links` - External link count
- `unique_internal_links` - Unique internal
- `unique_external_links` - Unique external
- `dofollow_links` - DoFollow count
- `nofollow_links` - NoFollow count
- `sponsored_links` - Sponsored count
- `ugc_links` - UGC count
- `text_links` - Text anchor links
- `image_links` - Image links
- `empty_anchor_links` - Empty anchors
- `javascript_links` - JS links
- `hash_links` - Hash/anchor links
- `tel_links` - Telephone links
- `mailto_links` - Email links
- `links_with_title` - Title attribute
- `links_without_noopener` - Security issue
- `links_new_window` - Target blank
- `links_score` - Overall links score

### ⚙️ Technical SEO (40+ Parameters)
- `http_status` - HTTP status code
- `response_time` - Server response time
- `page_size_bytes` - Page size
- `has_ssl` - HTTPS enabled
- `has_viewport` - Viewport meta
- `viewport_content` - Viewport value
- `has_charset` - Charset declaration
- `charset` - Character encoding
- `html_lang` - HTML language
- `has_doctype` - DOCTYPE present
- `doctype` - DOCTYPE value
- `has_favicon` - Favicon
- `has_apple_touch_icon` - Apple icon
- `has_manifest` - Web manifest
- `has_theme_color` - Theme color
- `has_schema_markup` - Schema.org
- `schema_count` - Schema count
- `schema_types` - Schema types
- `microdata_items` - Microdata
- `rdfa_items` - RDFa items
- `total_css_files` - CSS files
- `total_js_files` - JS files
- `render_blocking_css` - Blocking CSS
- `render_blocking_js` - Blocking JS
- `async_js` - Async scripts
- `defer_js` - Deferred scripts
- `inline_css_count` - Inline CSS
- `inline_js_count` - Inline JS
- `has_gzip` - Gzip compression
- `has_cache_headers` - Caching
- `server` - Server header
- Security headers (8+ parameters)

### 📖 Content Analysis (35+ Parameters)
- `word_count` - Total words
- `sentence_count` - Sentences
- `paragraph_count` - Paragraphs
- `avg_sentence_length` - Sentence length
- `unique_words` - Unique word count
- `lexical_density` - Vocabulary richness
- `text_html_ratio` - Text percentage
- `flesch_reading_ease` - Readability score
- `flesch_kincaid_grade` - Grade level
- `top_keywords` - Keyword frequency
- `keyword_density` - Keyword percentage
- Content elements (lists, tables, quotes, etc.)
- Media elements (videos, iframes, etc.)

### And 50+ More Parameters...

## 📈 Category Scoring Weights

| Category | Weight |
|----------|--------|
| Technical SEO | 15% |
| Meta Tags | 12% |
| Content | 12% |
| Links | 10% |
| Images | 10% |
| Headings | 8% |
| Accessibility | 8% |
| Security | 7% |
| Open Graph | 5% |
| Twitter Cards | 4% |
| Mobile/UX | 4% |
| Performance | 3% |
| i18n | 1% |
| E-commerce | 1% |

## 🎨 Web Interface Features

- **Dark Mode UI** - Modern, professional design
- **Real-time Analysis** - Live progress updates
- **Categorized Results** - Organized by category tabs
- **Score Visualization** - Circular score display with grade
- **Issue Highlighting** - Color-coded by severity
- **Export Options** - JSON, Text, CSV downloads
- **Responsive Design** - Works on all devices

## 📊 Report Formats

### HTML Report
- Professional, printable design
- Interactive elements
- Full parameter breakdown
- Color-coded scores

### JSON Report
- Machine-readable
- All 200+ parameters
- Suitable for integration

### CSV Summary
- Spreadsheet-compatible
- Key metrics only
- Batch comparison

## 🔧 Configuration

### Target Keyword
Setting a target keyword enables additional checks:
- Keyword in title
- Keyword in meta description
- Keyword in H1
- Keyword in content
- Keyword density analysis

### Batch Processing
- Sequential or parallel processing
- Configurable worker threads
- Rate limiting built-in
- Aggregate reporting

## 🚀 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

### Heroku
```bash
heroku create your-seo-tool
git push heroku main
```

## 📝 License

MIT License - Free for personal and commercial use.

## 👨‍💻 Author

**Muntasir Islam**
- 🌐 [Portfolio](https://muntasir-islam.github.io)
- 💼 SEO Specialist & Web Strategist

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## ⭐ Star History

If you find this tool useful, please give it a star!

---

**Advanced SEO Audit Tool v2.0** - Comprehensive SEO analysis with 200+ parameters.
