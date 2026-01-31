"""
Advanced SEO Audit Tool - 200+ Parameter Analysis
Author: Muntasir Islam
Description: Enterprise-grade SEO audit tool with comprehensive checks
Version: 2.0
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
import json
import re
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any, Tuple
import time
import hashlib
from collections import Counter
import math


@dataclass
class SEOAuditResult:
    """Comprehensive data class to store 200+ audit parameters"""
    url: str
    audit_date: str
    score: int
    grade: str
    
    # ===========================================
    # CATEGORY 1: META TAGS (20+ parameters)
    # ===========================================
    title: Optional[str] = None
    title_length: int = 0
    title_status: str = ""
    title_has_keyword: bool = False
    title_has_numbers: bool = False
    title_has_power_words: bool = False
    title_pixel_width: int = 0
    
    meta_description: Optional[str] = None
    meta_description_length: int = 0
    meta_description_status: str = ""
    meta_description_has_keyword: bool = False
    meta_description_has_cta: bool = False
    
    meta_keywords: Optional[str] = None
    meta_keywords_count: int = 0
    
    canonical_url: Optional[str] = None
    canonical_is_self: bool = False
    robots_meta: Optional[str] = None
    robots_index: bool = True
    robots_follow: bool = True
    
    meta_author: Optional[str] = None
    meta_publisher: Optional[str] = None
    meta_copyright: Optional[str] = None
    meta_language: Optional[str] = None
    meta_revisit: Optional[str] = None
    meta_rating: Optional[str] = None
    meta_referrer: Optional[str] = None
    
    # ===========================================
    # CATEGORY 2: OPEN GRAPH (15+ parameters)
    # ===========================================
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    og_image_width: Optional[str] = None
    og_image_height: Optional[str] = None
    og_url: Optional[str] = None
    og_type: Optional[str] = None
    og_site_name: Optional[str] = None
    og_locale: Optional[str] = None
    og_video: Optional[str] = None
    og_audio: Optional[str] = None
    og_complete: bool = False
    og_score: int = 0
    
    # ===========================================
    # CATEGORY 3: TWITTER CARDS (12+ parameters)
    # ===========================================
    twitter_card: Optional[str] = None
    twitter_title: Optional[str] = None
    twitter_description: Optional[str] = None
    twitter_image: Optional[str] = None
    twitter_site: Optional[str] = None
    twitter_creator: Optional[str] = None
    twitter_player: Optional[str] = None
    twitter_app_iphone: Optional[str] = None
    twitter_app_android: Optional[str] = None
    twitter_complete: bool = False
    twitter_score: int = 0
    
    # ===========================================
    # CATEGORY 4: HEADINGS (20+ parameters)
    # ===========================================
    h1_count: int = 0
    h1_tags: List[str] = field(default_factory=list)
    h1_length_avg: float = 0.0
    h1_has_keyword: bool = False
    
    h2_count: int = 0
    h2_tags: List[str] = field(default_factory=list)
    h3_count: int = 0
    h3_tags: List[str] = field(default_factory=list)
    h4_count: int = 0
    h5_count: int = 0
    h6_count: int = 0
    
    total_headings: int = 0
    heading_hierarchy_valid: bool = False
    heading_structure_status: str = ""
    heading_keyword_density: float = 0.0
    headings_to_content_ratio: float = 0.0
    empty_headings: int = 0
    duplicate_headings: int = 0
    long_headings: int = 0
    
    # ===========================================
    # CATEGORY 5: IMAGES (25+ parameters)
    # ===========================================
    total_images: int = 0
    images_without_alt: int = 0
    images_with_empty_alt: int = 0
    images_with_title: int = 0
    images_without_src: int = 0
    images_status: str = ""
    
    images_with_lazy_loading: int = 0
    images_with_srcset: int = 0
    images_with_sizes: int = 0
    images_webp: int = 0
    images_svg: int = 0
    images_png: int = 0
    images_jpg: int = 0
    images_gif: int = 0
    images_external: int = 0
    images_internal: int = 0
    
    images_too_large: int = 0
    images_with_descriptive_filename: int = 0
    images_decorative: int = 0
    figure_elements: int = 0
    images_in_picture: int = 0
    
    avg_alt_length: float = 0.0
    images_score: int = 0
    
    # ===========================================
    # CATEGORY 6: LINKS (30+ parameters)
    # ===========================================
    internal_links: int = 0
    external_links: int = 0
    total_links: int = 0
    unique_internal_links: int = 0
    unique_external_links: int = 0
    
    nofollow_links: int = 0
    dofollow_links: int = 0
    sponsored_links: int = 0
    ugc_links: int = 0
    
    links_with_title: int = 0
    links_without_title: int = 0
    links_with_target_blank: int = 0
    links_with_rel_noopener: int = 0
    links_without_noopener: int = 0
    
    anchor_text_distribution: Dict[str, int] = field(default_factory=dict)
    empty_anchor_links: int = 0
    image_links: int = 0
    text_links: int = 0
    
    javascript_links: int = 0
    hash_links: int = 0
    mailto_links: int = 0
    tel_links: int = 0
    
    broken_links: List[str] = field(default_factory=list)
    redirect_links: int = 0
    
    link_depth_distribution: Dict[int, int] = field(default_factory=dict)
    links_score: int = 0
    
    # ===========================================
    # CATEGORY 7: TECHNICAL SEO (40+ parameters)
    # ===========================================
    has_ssl: bool = False
    ssl_valid: bool = False
    ssl_issuer: Optional[str] = None
    ssl_expiry: Optional[str] = None
    
    has_viewport: bool = False
    viewport_content: Optional[str] = None
    viewport_initial_scale: bool = False
    viewport_user_scalable: bool = True
    
    has_charset: bool = False
    charset_value: Optional[str] = None
    has_doctype: bool = False
    doctype_value: Optional[str] = None
    html_lang: Optional[str] = None
    
    has_favicon: bool = False
    favicon_format: Optional[str] = None
    has_apple_touch_icon: bool = False
    has_manifest: bool = False
    manifest_url: Optional[str] = None
    
    has_schema_markup: bool = False
    schema_types: List[str] = field(default_factory=list)
    schema_count: int = 0
    microdata_items: int = 0
    rdfa_items: int = 0
    
    has_robots_txt: bool = False
    robots_txt_url: Optional[str] = None
    has_sitemap: bool = False
    sitemap_url: Optional[str] = None
    sitemap_in_robots: bool = False
    
    response_time: float = 0.0
    page_size_bytes: int = 0
    page_size_kb: float = 0.0
    html_size_bytes: int = 0
    
    total_css_files: int = 0
    total_js_files: int = 0
    inline_css_count: int = 0
    inline_js_count: int = 0
    inline_css_size: int = 0
    inline_js_size: int = 0
    
    render_blocking_css: int = 0
    render_blocking_js: int = 0
    async_js: int = 0
    defer_js: int = 0
    
    has_gzip: bool = False
    content_encoding: Optional[str] = None
    
    has_cache_headers: bool = False
    cache_control: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    
    http_status: int = 0
    content_type: Optional[str] = None
    server: Optional[str] = None
    x_powered_by: Optional[str] = None
    
    has_hsts: bool = False
    has_xss_protection: bool = False
    has_content_type_options: bool = False
    has_frame_options: bool = False
    has_csp: bool = False
    security_headers_score: int = 0
    
    # ===========================================
    # CATEGORY 8: CONTENT ANALYSIS (35+ parameters)
    # ===========================================
    word_count: int = 0
    character_count: int = 0
    sentence_count: int = 0
    paragraph_count: int = 0
    avg_sentence_length: float = 0.0
    avg_word_length: float = 0.0
    
    flesch_reading_ease: float = 0.0
    flesch_kincaid_grade: float = 0.0
    readability_status: str = ""
    
    text_html_ratio: float = 0.0
    unique_words: int = 0
    lexical_density: float = 0.0
    
    top_keywords: List[Tuple[str, int]] = field(default_factory=list)
    keyword_density: Dict[str, float] = field(default_factory=dict)
    stop_words_ratio: float = 0.0
    
    has_lists: bool = False
    ordered_lists: int = 0
    unordered_lists: int = 0
    list_items: int = 0
    
    has_tables: bool = False
    table_count: int = 0
    tables_with_headers: int = 0
    
    has_blockquotes: bool = False
    blockquote_count: int = 0
    
    has_code_blocks: bool = False
    code_block_count: int = 0
    
    bold_text_count: int = 0
    italic_text_count: int = 0
    underline_text_count: int = 0
    highlighted_text: int = 0
    
    video_count: int = 0
    audio_count: int = 0
    iframe_count: int = 0
    embed_count: int = 0
    object_count: int = 0
    
    content_score: int = 0
    
    # ===========================================
    # CATEGORY 9: MOBILE & UX (15+ parameters)
    # ===========================================
    is_mobile_friendly: bool = False
    has_amp_version: bool = False
    amp_url: Optional[str] = None
    
    touch_icons_count: int = 0
    has_theme_color: bool = False
    theme_color: Optional[str] = None
    
    has_mobile_app_links: bool = False
    ios_app_link: Optional[str] = None
    android_app_link: Optional[str] = None
    
    tap_targets_status: str = ""
    font_size_status: str = ""
    content_width_status: str = ""
    
    ux_score: int = 0
    
    # ===========================================
    # CATEGORY 10: INTERNATIONALIZATION (10+ parameters)
    # ===========================================
    has_hreflang: bool = False
    hreflang_tags: List[Dict[str, str]] = field(default_factory=list)
    hreflang_count: int = 0
    has_x_default: bool = False
    
    content_language: Optional[str] = None
    detected_language: Optional[str] = None
    
    has_direction_attr: bool = False
    text_direction: Optional[str] = None
    
    i18n_score: int = 0
    
    # ===========================================
    # CATEGORY 11: SOCIAL & SHARING (10+ parameters)
    # ===========================================
    social_links: Dict[str, str] = field(default_factory=dict)
    social_links_count: int = 0
    
    has_share_buttons: bool = False
    share_button_platforms: List[str] = field(default_factory=list)
    
    has_social_proof: bool = False
    has_testimonials: bool = False
    has_reviews_schema: bool = False
    
    social_score: int = 0
    
    # ===========================================
    # CATEGORY 12: E-COMMERCE SEO (15+ parameters)
    # ===========================================
    has_product_schema: bool = False
    product_name: Optional[str] = None
    product_price: Optional[str] = None
    product_currency: Optional[str] = None
    product_availability: Optional[str] = None
    product_rating: Optional[str] = None
    product_review_count: Optional[str] = None
    
    has_breadcrumbs: bool = False
    has_breadcrumb_schema: bool = False
    breadcrumb_levels: int = 0
    
    has_faq_schema: bool = False
    faq_questions_count: int = 0
    
    has_howto_schema: bool = False
    has_recipe_schema: bool = False
    has_event_schema: bool = False
    has_local_business_schema: bool = False
    
    ecommerce_score: int = 0
    
    # ===========================================
    # CATEGORY 13: ACCESSIBILITY (15+ parameters)
    # ===========================================
    has_skip_link: bool = False
    has_main_landmark: bool = False
    has_nav_landmark: bool = False
    has_footer_landmark: bool = False
    
    form_labels_count: int = 0
    form_inputs_count: int = 0
    forms_without_labels: int = 0
    
    aria_labels_count: int = 0
    aria_roles_count: int = 0
    tabindex_elements: int = 0
    
    color_contrast_issues: int = 0
    focus_visible_issues: int = 0
    
    accessibility_score: int = 0
    
    # ===========================================
    # CATEGORY 14: PERFORMANCE HINTS (10+ parameters)
    # ===========================================
    has_preload: bool = False
    preload_resources: List[str] = field(default_factory=list)
    has_prefetch: bool = False
    prefetch_resources: List[str] = field(default_factory=list)
    has_preconnect: bool = False
    preconnect_domains: List[str] = field(default_factory=list)
    has_dns_prefetch: bool = False
    
    critical_css_inlined: bool = False
    has_resource_hints: bool = False
    
    performance_hints_score: int = 0
    
    # ===========================================
    # CATEGORY 15: CRAWLING & INDEXING (25+ parameters)
    # ===========================================
    is_indexable: bool = True
    robots_txt_blocks_url: bool = False
    robots_txt_content: Optional[str] = None
    x_robots_tag: Optional[str] = None
    sitemap_in_robots_txt: bool = False
    sitemap_urls: List[str] = field(default_factory=list)
    is_in_sitemap: bool = False
    url_is_crawlable: bool = True
    has_redirect_chain: bool = False
    redirect_chain_length: int = 0
    final_url: Optional[str] = None
    has_5xx_error: bool = False
    url_structure_friendly: bool = True
    url_length: int = 0
    url_has_parameters: bool = False
    url_has_underscores: bool = False
    url_depth: int = 0
    blocks_css_in_robots: bool = False
    blocks_js_in_robots: bool = False
    blocks_images_in_robots: bool = False
    has_noindex_system_pages: bool = True
    crawl_budget_issues: List[str] = field(default_factory=list)
    html_validation_errors: int = 0
    html_validation_warnings: int = 0
    crawling_score: int = 0
    
    # ===========================================
    # CATEGORY 16: CONTENT QUALITY (30+ parameters)
    # ===========================================
    has_thin_content: bool = False
    content_is_unique: bool = True
    duplicate_content_urls: List[str] = field(default_factory=list)
    has_privacy_policy: bool = False
    has_contact_page: bool = False
    has_about_page: bool = False
    publication_date: Optional[str] = None
    modified_date: Optional[str] = None
    has_author_info: bool = False
    author_name: Optional[str] = None
    has_publisher_info: bool = False
    has_eeat_signals: bool = False
    content_in_iframes: bool = False
    has_intrusive_interstitials: bool = False
    has_heavy_above_fold_ads: bool = False
    ad_density_ratio: float = 0.0
    has_hidden_text: bool = False
    has_cloaking: bool = False
    has_doorway_pages: bool = False
    is_infinite_scroll_crawlable: bool = True
    lazy_content_discoverable: bool = True
    has_clear_cta: bool = False
    grammar_issues: int = 0
    spelling_issues: int = 0
    uses_semantic_html: bool = False
    content_freshness_score: int = 0
    evergreen_content_ratio: float = 0.0
    content_quality_score: int = 0
    
    # ===========================================
    # CATEGORY 17: KEYWORD ANALYSIS (20+ parameters)
    # ===========================================
    target_keyword: Optional[str] = None
    keyword_in_title: bool = False
    keyword_in_title_position: int = -1
    keyword_in_meta_desc: bool = False
    keyword_in_h1: bool = False
    keyword_in_h2: bool = False
    keyword_in_first_paragraph: bool = False
    keyword_in_body: bool = False
    keyword_count_in_body: int = 0
    keyword_density_percent: float = 0.0
    keyword_overuse: bool = False
    keyword_cannibalization_risk: bool = False
    related_keywords: List[str] = field(default_factory=list)
    lsi_keywords: List[str] = field(default_factory=list)
    keyword_prominence_score: float = 0.0
    branded_query_potential: bool = False
    keyword_analysis_score: int = 0
    
    # ===========================================
    # CATEGORY 18: BACKLINKS (15+ parameters) 
    # ===========================================
    backlink_profile_status: str = "Not analyzed"
    estimated_domain_authority: Optional[int] = None
    external_links_to_authority_sites: int = 0
    has_social_profiles: bool = False
    social_profile_links: Dict[str, str] = field(default_factory=dict)
    outbound_link_quality: str = "Unknown"
    internal_link_structure_score: int = 0
    orphan_page_risk: bool = False
    link_equity_distribution: str = "Unknown"
    backlinks_score: int = 0
    
    # ===========================================
    # CATEGORY 19: MOBILE ADVANCED (20+ parameters)
    # ===========================================
    mobile_page_weight_kb: float = 0.0
    mobile_page_heavy: bool = False
    has_responsive_images: bool = False
    images_properly_sized: bool = True
    image_compression_score: int = 0
    tap_targets_sized_correctly: bool = True
    tap_target_issues: int = 0
    font_sizes_readable: bool = True
    small_font_elements: int = 0
    content_width_fits_viewport: bool = True
    horizontal_scroll_issues: bool = False
    mobile_navigation_friendly: bool = True
    thumb_friendly_navigation: bool = True
    mobile_video_optimized: bool = True
    favicon_in_mobile_serps: bool = False
    mobile_desktop_parity: bool = True
    mobile_meta_parity: bool = True
    mobile_directives_parity: bool = True
    mobile_advanced_score: int = 0
    
    # ===========================================
    # CATEGORY 20: PAGE ELEMENTS ANALYSIS (15+ parameters)
    # ===========================================
    has_multiple_h1: bool = False
    title_matches_content: bool = True
    title_starts_with_keyword: bool = False
    meta_desc_is_unique: bool = True
    meta_desc_compelling: bool = False
    links_distinguishable: bool = True
    text_contrast_sufficient: bool = True
    primary_content_clear: bool = True
    supplementary_content_marked: bool = False
    page_elements_score: int = 0
    
    # ===========================================
    # ISSUES & RECOMMENDATIONS
    # ===========================================
    critical_issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    passed_checks: List[str] = field(default_factory=list)
    
    meta_score: int = 0
    heading_score: int = 0
    technical_score: int = 0
    meta_tags_score: int = 0
    headings_score: int = 0
    technical_seo_score: int = 0
    viewport_configured: bool = False
    has_referrer_policy: bool = False
    preload_count: int = 0
    preconnect_count: int = 0
    dns_prefetch_count: int = 0
    prefetch_count: int = 0
    tabindex_issues: int = 0
    og_locale_alternate: List[str] = field(default_factory=list)
    twitter_image_alt: Optional[str] = None
    charset: Optional[str] = None
    headings_with_keywords: int = 0
    longest_alt: int = 0
    links_new_window: int = 0
    
    total_checks: int = 300
    checks_passed: int = 0
    checks_failed: int = 0
    checks_warnings: int = 0


class AdvancedSEOAuditor:
    """Enterprise-grade SEO Audit class with 200+ parameters"""
    
    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
        'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will',
        'with', 'the', 'this', 'but', 'they', 'have', 'had', 'what', 'when', 'where',
        'who', 'which', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
        'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
        'so', 'than', 'too', 'very', 'can', 'just', 'should', 'now', 'i', 'you', 'we',
        'your', 'my', 'our', 'their', 'his', 'her', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'under', 'again', 'further',
        'then', 'once', 'here', 'there', 'any', 'if', 'or', 'because', 'until', 'while'
    }
    
    POWER_WORDS = {
        'ultimate', 'complete', 'essential', 'proven', 'powerful', 'amazing', 'best',
        'top', 'secret', 'exclusive', 'free', 'new', 'easy', 'simple', 'fast', 'quick',
        'instant', 'guaranteed', 'effective', 'professional', 'expert', 'advanced',
        'comprehensive', 'definitive', 'guide', 'tips', 'tricks', 'hacks', 'strategies'
    }
    
    SOCIAL_PATTERNS = {
        'facebook': r'facebook\.com|fb\.com',
        'twitter': r'twitter\.com|x\.com',
        'linkedin': r'linkedin\.com',
        'instagram': r'instagram\.com',
        'youtube': r'youtube\.com|youtu\.be',
        'pinterest': r'pinterest\.com',
        'tiktok': r'tiktok\.com',
        'github': r'github\.com',
        'reddit': r'reddit\.com'
    }
    
    def __init__(self, url: str, target_keyword: str = None):
        self.url = self._normalize_url(url)
        self.target_keyword = target_keyword.lower() if target_keyword else None
        self.soup = None
        self.response = None
        self.headers = {}
        self.issues = {"critical": [], "warnings": [], "recommendations": [], "passed": []}
        self.response_time = 0
        
    def _normalize_url(self, url: str) -> str:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def fetch_page(self) -> bool:
        request_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        try:
            print(f"  → Fetching URL: {self.url}")
            start_time = time.time()
            self.response = requests.get(self.url, headers=request_headers, timeout=30, allow_redirects=True)
            self.response_time = time.time() - start_time
            print(f"  → Status Code: {self.response.status_code}")
            print(f"  → Response Time: {self.response_time:.2f}s")
            print(f"  → Content Length: {len(self.response.text)} chars")
            self.response.raise_for_status()
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            self.headers = dict(self.response.headers)
            
            # Debug: verify soup was created and has content
            title = self.soup.find('title')
            print(f"  → Title found: {title.get_text()[:50] if title else 'None'}...")
            
            return True
        except requests.RequestException as e:
            print(f"  ✗ Error fetching {self.url}: {e}")
            return False
    
    def analyze_title(self) -> dict:
        title_tag = self.soup.find('title')
        title = title_tag.get_text().strip() if title_tag else None
        length = len(title) if title else 0
        pixel_width = int(length * 6.5) if title else 0
        
        has_keyword = False
        if title and self.target_keyword:
            has_keyword = self.target_keyword.lower() in title.lower()
        
        has_numbers = bool(re.search(r'\d', title)) if title else False
        
        has_power_words = False
        if title:
            title_words = set(title.lower().split())
            has_power_words = bool(title_words & self.POWER_WORDS)
        
        if not title:
            status = "❌ Missing"
            self.issues["critical"].append("Missing page title - Critical for SEO")
        elif length < 30:
            status = "⚠️ Too Short"
            self.issues["warnings"].append(f"Title too short ({length} chars). Aim for 50-60 characters.")
        elif length > 60:
            status = "⚠️ Too Long"
            self.issues["warnings"].append(f"Title too long ({length} chars). May be truncated in SERPs.")
        elif pixel_width > 600:
            status = "⚠️ Pixel Width"
            self.issues["warnings"].append(f"Title may be truncated (est. {pixel_width}px > 600px)")
        else:
            status = "✅ Good"
            self.issues["passed"].append("Title tag is well optimized")
        
        if title and not has_keyword and self.target_keyword:
            self.issues["recommendations"].append(f"Consider adding target keyword '{self.target_keyword}' to title")
        
        return {
            "title": title, "length": length, "status": status,
            "pixel_width": pixel_width, "has_keyword": has_keyword,
            "has_numbers": has_numbers, "has_power_words": has_power_words
        }
    
    def analyze_meta_description(self) -> dict:
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '').strip() if meta_desc else None
        length = len(description) if description else 0
        
        has_keyword = False
        if description and self.target_keyword:
            has_keyword = self.target_keyword.lower() in description.lower()
        
        cta_words = ['learn', 'discover', 'get', 'find', 'try', 'start', 'buy', 'shop', 'read', 'click', 'download']
        has_cta = any(word in description.lower() for word in cta_words) if description else False
        
        if not description:
            status = "❌ Missing"
            self.issues["critical"].append("Missing meta description - Affects click-through rates")
        elif length < 120:
            status = "⚠️ Too Short"
            self.issues["warnings"].append(f"Meta description too short ({length} chars). Aim for 150-160 characters.")
        elif length > 160:
            status = "⚠️ Too Long"
            self.issues["warnings"].append(f"Meta description too long ({length} chars). May be truncated.")
        else:
            status = "✅ Good"
            self.issues["passed"].append("Meta description is well optimized")
        
        if description and not has_cta:
            self.issues["recommendations"].append("Add a call-to-action to meta description")
        
        return {
            "description": description, "length": length, "status": status,
            "has_keyword": has_keyword, "has_cta": has_cta
        }
    
    def analyze_meta_tags(self) -> dict:
        result = {}
        
        meta_kw = self.soup.find('meta', attrs={'name': 'keywords'})
        keywords = meta_kw.get('content', '').strip() if meta_kw else None
        result['keywords'] = keywords
        result['keywords_count'] = len(keywords.split(',')) if keywords else 0
        
        canonical = self.soup.find('link', attrs={'rel': 'canonical'})
        canonical_url = canonical.get('href') if canonical else None
        result['canonical_url'] = canonical_url
        result['canonical_is_self'] = canonical_url == self.url if canonical_url else False
        
        if not canonical_url:
            self.issues["warnings"].append("Missing canonical URL - May cause duplicate content issues")
        else:
            self.issues["passed"].append("Canonical URL is set")
        
        robots = self.soup.find('meta', attrs={'name': 'robots'})
        robots_content = robots.get('content', '').lower() if robots else ''
        result['robots_meta'] = robots_content or None
        result['robots_index'] = 'noindex' not in robots_content
        result['robots_follow'] = 'nofollow' not in robots_content
        
        if not result['robots_index']:
            self.issues["critical"].append("Page is set to noindex - Will not appear in search results")
        
        for name in ['author', 'publisher', 'copyright', 'language', 'revisit-after', 'rating', 'referrer']:
            meta = self.soup.find('meta', attrs={'name': name})
            result[f'meta_{name.replace("-", "_")}'] = meta.get('content') if meta else None
        
        return result
    
    def analyze_open_graph(self) -> dict:
        og_tags = {}
        og_properties = [
            'og:title', 'og:description', 'og:image', 'og:image:width', 'og:image:height',
            'og:url', 'og:type', 'og:site_name', 'og:locale', 'og:video', 'og:audio'
        ]
        
        for prop in og_properties:
            meta = self.soup.find('meta', attrs={'property': prop})
            key = prop.replace('og:', '').replace(':', '_')
            og_tags[key] = meta.get('content') if meta else None
        
        required = ['title', 'description', 'image', 'url', 'type']
        present = sum(1 for r in required if og_tags.get(r))
        og_tags['complete'] = present == len(required)
        og_tags['score'] = int((present / len(required)) * 100)
        
        if og_tags['score'] < 60:
            self.issues["warnings"].append(f"Incomplete Open Graph tags ({og_tags['score']}% complete)")
        elif og_tags['score'] == 100:
            self.issues["passed"].append("Open Graph tags are complete")
        
        return og_tags
    
    def analyze_twitter_cards(self) -> dict:
        twitter_tags = {}
        twitter_properties = [
            'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image',
            'twitter:site', 'twitter:creator', 'twitter:player', 'twitter:app:id:iphone',
            'twitter:app:id:googleplay'
        ]
        
        for prop in twitter_properties:
            meta = self.soup.find('meta', attrs={'name': prop})
            key = prop.replace('twitter:', '').replace(':', '_')
            twitter_tags[key] = meta.get('content') if meta else None
        
        required = ['card', 'title', 'description', 'image']
        present = sum(1 for r in required if twitter_tags.get(r))
        twitter_tags['complete'] = present == len(required)
        twitter_tags['score'] = int((present / len(required)) * 100)
        
        if twitter_tags['score'] < 60:
            self.issues["recommendations"].append("Add Twitter Card tags for better social sharing")
        elif twitter_tags['score'] == 100:
            self.issues["passed"].append("Twitter Card tags are complete")
        
        return twitter_tags
    
    def analyze_headings(self) -> dict:
        headings = {}
        
        for level in range(1, 7):
            tag = f'h{level}'
            elements = self.soup.find_all(tag)
            headings[f'{tag}_count'] = len(elements)
            if level <= 3:
                headings[f'{tag}_tags'] = [h.get_text().strip()[:100] for h in elements]
        
        h1_tags = headings.get('h1_tags', [])
        h1_count = headings['h1_count']
        
        total_headings = sum(headings[f'h{i}_count'] for i in range(1, 7))
        headings['total_headings'] = total_headings
        
        if h1_tags:
            headings['h1_length_avg'] = sum(len(h) for h in h1_tags) / len(h1_tags)
        
        hierarchy_valid = True
        if headings['h1_count'] == 0:
            hierarchy_valid = False
        elif headings['h2_count'] == 0 and (headings['h3_count'] > 0 or headings['h4_count'] > 0):
            hierarchy_valid = False
        headings['hierarchy_valid'] = hierarchy_valid
        
        all_headings = []
        for level in range(1, 7):
            all_headings.extend(self.soup.find_all(f'h{level}'))
        
        empty = sum(1 for h in all_headings if not h.get_text().strip())
        headings['empty_headings'] = empty
        
        heading_texts = [h.get_text().strip().lower() for h in all_headings if h.get_text().strip()]
        duplicates = len(heading_texts) - len(set(heading_texts))
        headings['duplicate_headings'] = duplicates
        
        long_count = sum(1 for h in all_headings if len(h.get_text().strip()) > 70)
        headings['long_headings'] = long_count
        
        has_keyword = False
        if self.target_keyword and h1_tags:
            has_keyword = any(self.target_keyword.lower() in h.lower() for h in h1_tags)
        headings['h1_has_keyword'] = has_keyword
        
        if h1_count == 0:
            status = "❌ Missing H1"
            self.issues["critical"].append("Missing H1 tag - Critical for SEO")
        elif h1_count > 1:
            status = "⚠️ Multiple H1s"
            self.issues["warnings"].append(f"Multiple H1 tags ({h1_count}). Best practice: one H1 per page")
        elif not hierarchy_valid:
            status = "⚠️ Invalid Hierarchy"
            self.issues["warnings"].append("Heading hierarchy is not sequential")
        else:
            status = "✅ Good"
            self.issues["passed"].append("Heading structure is well organized")
        
        headings['status'] = status
        
        if empty > 0:
            self.issues["warnings"].append(f"{empty} empty heading(s) found")
        if duplicates > 0:
            self.issues["recommendations"].append(f"{duplicates} duplicate heading(s)")
        
        return headings
    
    def analyze_images(self) -> dict:
        images = self.soup.find_all('img')
        total = len(images)
        
        result = {
            'total': total,
            'without_alt': 0,
            'with_empty_alt': 0,
            'with_title': 0,
            'without_src': 0,
            'with_lazy_loading': 0,
            'with_srcset': 0,
            'with_sizes': 0,
            'webp': 0, 'svg': 0, 'png': 0, 'jpg': 0, 'gif': 0,
            'external': 0, 'internal': 0,
            'with_descriptive_filename': 0,
            'decorative': 0,
            'alt_lengths': []
        }
        
        parsed_url = urlparse(self.url)
        base_domain = parsed_url.netloc
        
        for img in images:
            src = img.get('src', '')
            alt = img.get('alt')
            
            if alt is None:
                result['without_alt'] += 1
            elif alt.strip() == '':
                result['with_empty_alt'] += 1
                result['decorative'] += 1
            else:
                result['alt_lengths'].append(len(alt))
            
            if img.get('title'):
                result['with_title'] += 1
            
            if not src:
                result['without_src'] += 1
            
            if img.get('loading') == 'lazy' or 'lazy' in str(img.get('class', [])):
                result['with_lazy_loading'] += 1
            
            if img.get('srcset'):
                result['with_srcset'] += 1
            if img.get('sizes'):
                result['with_sizes'] += 1
            
            src_lower = src.lower()
            if '.webp' in src_lower:
                result['webp'] += 1
            elif '.svg' in src_lower:
                result['svg'] += 1
            elif '.png' in src_lower:
                result['png'] += 1
            elif '.jpg' in src_lower or '.jpeg' in src_lower:
                result['jpg'] += 1
            elif '.gif' in src_lower:
                result['gif'] += 1
            
            if src.startswith('http'):
                img_domain = urlparse(src).netloc
                if img_domain == base_domain:
                    result['internal'] += 1
                else:
                    result['external'] += 1
            else:
                result['internal'] += 1
            
            if src:
                filename = src.split('/')[-1].split('?')[0].lower()
                generic_names = ['image', 'img', 'photo', 'pic', 'picture', 'untitled', 'dsc', 'screenshot']
                if not any(g in filename for g in generic_names) and len(filename) > 5:
                    result['with_descriptive_filename'] += 1
        
        result['figure_elements'] = len(self.soup.find_all('figure'))
        result['images_in_picture'] = len(self.soup.find_all('picture'))
        
        if result['alt_lengths']:
            result['avg_alt_length'] = sum(result['alt_lengths']) / len(result['alt_lengths'])
        else:
            result['avg_alt_length'] = 0
        
        score = 100
        if total > 0:
            missing_alt_ratio = result['without_alt'] / total
            if missing_alt_ratio > 0.5:
                score -= 30
            elif missing_alt_ratio > 0.2:
                score -= 15
            
            if result['with_lazy_loading'] == 0 and total > 3:
                score -= 10
            
            if result['webp'] == 0 and total > 0:
                score -= 5
        
        result['score'] = max(0, score)
        
        if total == 0:
            status = "ℹ️ No Images"
        elif result['without_alt'] == 0:
            status = "✅ All Have Alt"
            self.issues["passed"].append("All images have alt attributes")
        elif result['without_alt'] / total > 0.5:
            status = "❌ Many Missing Alt"
            self.issues["critical"].append(f"{result['without_alt']} of {total} images missing alt text")
        else:
            status = "⚠️ Some Missing Alt"
            self.issues["warnings"].append(f"{result['without_alt']} of {total} images missing alt text")
        
        result['status'] = status
        
        if total > 3 and result['with_lazy_loading'] == 0:
            self.issues["recommendations"].append("Implement lazy loading for images")
        
        if total > 0 and result['webp'] == 0:
            self.issues["recommendations"].append("Consider using WebP format for better compression")
        
        return result
    
    def analyze_links(self) -> dict:
        links = self.soup.find_all('a', href=True)
        parsed_url = urlparse(self.url)
        base_domain = parsed_url.netloc
        
        result = {
            'internal': 0, 'external': 0, 'total': len(links),
            'unique_internal': set(), 'unique_external': set(),
            'nofollow': 0, 'dofollow': 0, 'sponsored': 0, 'ugc': 0,
            'with_title': 0, 'without_title': 0,
            'with_target_blank': 0, 'with_rel_noopener': 0, 'without_noopener': 0,
            'empty_anchor': 0, 'image_links': 0, 'text_links': 0,
            'javascript': 0, 'hash': 0, 'mailto': 0, 'tel': 0,
            'anchor_texts': [],
            'broken': []
        }
        
        for link in links:
            href = link.get('href', '')
            rel = link.get('rel', [])
            if isinstance(rel, str):
                rel = rel.split()
            
            if href.startswith('javascript:'):
                result['javascript'] += 1
                continue
            elif href.startswith('#'):
                result['hash'] += 1
                continue
            elif href.startswith('mailto:'):
                result['mailto'] += 1
                continue
            elif href.startswith('tel:'):
                result['tel'] += 1
                continue
            
            full_url = urljoin(self.url, href)
            link_domain = urlparse(full_url).netloc
            
            if link_domain == base_domain or not link_domain:
                result['internal'] += 1
                result['unique_internal'].add(full_url)
            else:
                result['external'] += 1
                result['unique_external'].add(full_url)
            
            if 'nofollow' in rel:
                result['nofollow'] += 1
            else:
                result['dofollow'] += 1
            
            if 'sponsored' in rel:
                result['sponsored'] += 1
            if 'ugc' in rel:
                result['ugc'] += 1
            
            if link.get('title'):
                result['with_title'] += 1
            else:
                result['without_title'] += 1
            
            if link.get('target') == '_blank':
                result['with_target_blank'] += 1
                if 'noopener' in rel or 'noreferrer' in rel:
                    result['with_rel_noopener'] += 1
                else:
                    result['without_noopener'] += 1
            
            anchor_text = link.get_text().strip()
            if not anchor_text:
                result['empty_anchor'] += 1
            else:
                result['anchor_texts'].append(anchor_text.lower())
            
            if link.find('img'):
                result['image_links'] += 1
            else:
                result['text_links'] += 1
        
        result['unique_internal'] = len(result['unique_internal'])
        result['unique_external'] = len(result['unique_external'])
        
        anchor_counter = Counter(result['anchor_texts'])
        result['anchor_distribution'] = dict(anchor_counter.most_common(10))
        del result['anchor_texts']
        
        score = 100
        if result['internal'] < 3:
            score -= 15
        if result['without_noopener'] > 0:
            score -= 10
        if result['empty_anchor'] > result['total'] * 0.2:
            score -= 10
        
        result['score'] = max(0, score)
        
        if result['internal'] < 3:
            self.issues["recommendations"].append("Add more internal links to improve site navigation")
        else:
            self.issues["passed"].append(f"Good internal linking ({result['internal']} links)")
        
        if result['without_noopener'] > 0:
            self.issues["warnings"].append(f"{result['without_noopener']} external links with target='_blank' missing rel='noopener'")
        
        if result['empty_anchor'] > 0:
            self.issues["warnings"].append(f"{result['empty_anchor']} links with empty anchor text")
        
        return result
    
    def analyze_technical(self) -> dict:
        result = {}
        
        result['has_ssl'] = self.url.startswith('https://')
        if not result['has_ssl']:
            self.issues["critical"].append("Website not using HTTPS - Security and ranking issue")
        else:
            self.issues["passed"].append("Website uses HTTPS")
        
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        result['has_viewport'] = viewport is not None
        result['viewport_content'] = viewport.get('content') if viewport else None
        
        if viewport:
            content = result['viewport_content'] or ''
            result['viewport_initial_scale'] = 'initial-scale' in content
            result['viewport_user_scalable'] = 'user-scalable=no' not in content.lower()
            self.issues["passed"].append("Viewport meta tag is set")
        else:
            self.issues["critical"].append("Missing viewport meta tag - Mobile unfriendly")
        
        charset = self.soup.find('meta', attrs={'charset': True})
        charset_http = self.soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        result['has_charset'] = charset is not None or charset_http is not None
        result['charset_value'] = charset.get('charset') if charset else None
        
        if result['has_charset']:
            self.issues["passed"].append("Character encoding is defined")
        else:
            self.issues["warnings"].append("Missing charset declaration")
        
        result['has_doctype'] = '<!doctype' in str(self.soup)[:100].lower()
        
        html_tag = self.soup.find('html')
        result['html_lang'] = html_tag.get('lang') if html_tag else None
        if not result['html_lang']:
            self.issues["warnings"].append("Missing lang attribute on html tag")
        else:
            self.issues["passed"].append("HTML lang attribute is set")
        
        favicon = self.soup.find('link', attrs={'rel': lambda x: x and 'icon' in x.lower() if x else False})
        result['has_favicon'] = favicon is not None
        if favicon:
            href = favicon.get('href', '')
            result['favicon_format'] = href.split('.')[-1].split('?')[0] if '.' in href else None
            self.issues["passed"].append("Favicon is set")
        else:
            self.issues["warnings"].append("Missing favicon")
        
        apple_icon = self.soup.find('link', attrs={'rel': 'apple-touch-icon'})
        result['has_apple_touch_icon'] = apple_icon is not None
        
        manifest = self.soup.find('link', attrs={'rel': 'manifest'})
        result['has_manifest'] = manifest is not None
        result['manifest_url'] = manifest.get('href') if manifest else None
        
        schema_scripts = self.soup.find_all('script', attrs={'type': 'application/ld+json'})
        result['has_schema'] = len(schema_scripts) > 0
        result['schema_count'] = len(schema_scripts)
        result['schema_types'] = []
        
        for script in schema_scripts:
            try:
                if script.string:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        if '@type' in data:
                            result['schema_types'].append(data['@type'])
                        if '@graph' in data:
                            for item in data['@graph']:
                                if '@type' in item:
                                    result['schema_types'].append(item['@type'])
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and '@type' in item:
                                result['schema_types'].append(item['@type'])
            except:
                pass
        
        if result['has_schema']:
            self.issues["passed"].append(f"Schema markup found: {', '.join(result['schema_types'][:3])}")
        else:
            self.issues["recommendations"].append("Add Schema.org structured data markup")
        
        result['microdata_items'] = len(self.soup.find_all(attrs={'itemtype': True}))
        result['rdfa_items'] = len(self.soup.find_all(attrs={'typeof': True}))
        
        result['total_css_files'] = len(self.soup.find_all('link', attrs={'rel': 'stylesheet'}))
        result['total_js_files'] = len(self.soup.find_all('script', attrs={'src': True}))
        
        style_tags = self.soup.find_all('style')
        result['inline_css_count'] = len(style_tags)
        result['inline_css_size'] = sum(len(s.get_text()) for s in style_tags)
        
        script_tags = [s for s in self.soup.find_all('script') if not s.get('src')]
        result['inline_js_count'] = len(script_tags)
        result['inline_js_size'] = sum(len(s.get_text()) for s in script_tags)
        
        all_scripts = self.soup.find_all('script', attrs={'src': True})
        result['async_js'] = sum(1 for s in all_scripts if s.get('async'))
        result['defer_js'] = sum(1 for s in all_scripts if s.get('defer'))
        result['render_blocking_js'] = result['total_js_files'] - result['async_js'] - result['defer_js']
        
        css_links = self.soup.find_all('link', attrs={'rel': 'stylesheet'})
        result['render_blocking_css'] = sum(1 for c in css_links if not c.get('media') or c.get('media') == 'all')
        
        result['http_status'] = self.response.status_code
        result['content_type'] = self.headers.get('Content-Type')
        result['server'] = self.headers.get('Server')
        result['x_powered_by'] = self.headers.get('X-Powered-By')
        
        result['content_encoding'] = self.headers.get('Content-Encoding')
        result['has_gzip'] = 'gzip' in (result['content_encoding'] or '').lower()
        
        if result['has_gzip']:
            self.issues["passed"].append("Gzip compression enabled")
        else:
            self.issues["recommendations"].append("Enable Gzip compression for faster loading")
        
        result['cache_control'] = self.headers.get('Cache-Control')
        result['etag'] = self.headers.get('ETag')
        result['last_modified'] = self.headers.get('Last-Modified')
        result['has_cache_headers'] = bool(result['cache_control'] or result['etag'])
        
        result['has_hsts'] = 'Strict-Transport-Security' in self.headers
        result['has_xss_protection'] = 'X-XSS-Protection' in self.headers
        result['has_content_type_options'] = 'X-Content-Type-Options' in self.headers
        result['has_frame_options'] = 'X-Frame-Options' in self.headers
        result['has_csp'] = 'Content-Security-Policy' in self.headers
        
        security_checks = [result['has_hsts'], result['has_xss_protection'], 
                         result['has_content_type_options'], result['has_frame_options'], result['has_csp']]
        result['security_headers_score'] = int((sum(security_checks) / len(security_checks)) * 100)
        
        if result['security_headers_score'] < 40:
            self.issues["warnings"].append(f"Security headers incomplete ({result['security_headers_score']}%)")
        
        result['page_size_bytes'] = len(self.response.content)
        result['page_size_kb'] = round(result['page_size_bytes'] / 1024, 2)
        result['html_size_bytes'] = len(self.response.text.encode('utf-8'))
        
        if result['page_size_kb'] > 3000:
            self.issues["warnings"].append(f"Page size is large ({result['page_size_kb']}KB)")
        
        return result
    
    def analyze_content(self) -> dict:
        result = {}
        
        soup_copy = BeautifulSoup(str(self.soup), 'html.parser')
        for element in soup_copy(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        text = soup_copy.get_text(separator=' ')
        text = ' '.join(text.split())
        
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        result['word_count'] = len(words)
        result['character_count'] = len(text)
        
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        result['sentence_count'] = len(sentences)
        
        paragraphs = soup_copy.find_all('p')
        result['paragraph_count'] = len(paragraphs)
        
        if sentences:
            result['avg_sentence_length'] = round(len(words) / len(sentences), 1)
        else:
            result['avg_sentence_length'] = 0
        
        if words:
            result['avg_word_length'] = round(sum(len(w) for w in words) / len(words), 1)
        else:
            result['avg_word_length'] = 0
        
        syllables = sum(self._count_syllables(w) for w in words)
        if result['sentence_count'] > 0 and result['word_count'] > 0:
            asl = result['word_count'] / result['sentence_count']
            asw = syllables / result['word_count']
            result['flesch_reading_ease'] = round(206.835 - 1.015 * asl - 84.6 * asw, 1)
            result['flesch_kincaid_grade'] = round(0.39 * asl + 11.8 * asw - 15.59, 1)
        else:
            result['flesch_reading_ease'] = 0
            result['flesch_kincaid_grade'] = 0
        
        fre = result['flesch_reading_ease']
        if fre >= 60:
            result['readability_status'] = "✅ Easy to Read"
        elif fre >= 30:
            result['readability_status'] = "⚠️ Difficult"
        else:
            result['readability_status'] = "❌ Very Difficult"
        
        html_length = len(self.response.text)
        result['text_html_ratio'] = round((len(text) / html_length) * 100, 1) if html_length else 0
        
        if result['text_html_ratio'] < 10:
            self.issues["warnings"].append(f"Low text-to-HTML ratio ({result['text_html_ratio']}%)")
        
        unique_words = set(words)
        result['unique_words'] = len(unique_words)
        result['lexical_density'] = round((len(unique_words) / len(words)) * 100, 1) if words else 0
        
        content_words = [w for w in words if w not in self.STOP_WORDS and len(w) > 2]
        word_freq = Counter(content_words)
        result['top_keywords'] = word_freq.most_common(10)
        
        if content_words:
            result['keyword_density'] = {word: round((count / len(words)) * 100, 2) 
                                         for word, count in word_freq.most_common(5)}
        
        stop_count = sum(1 for w in words if w in self.STOP_WORDS)
        result['stop_words_ratio'] = round((stop_count / len(words)) * 100, 1) if words else 0
        
        result['has_lists'] = len(soup_copy.find_all(['ul', 'ol'])) > 0
        result['ordered_lists'] = len(soup_copy.find_all('ol'))
        result['unordered_lists'] = len(soup_copy.find_all('ul'))
        result['list_items'] = len(soup_copy.find_all('li'))
        
        result['has_tables'] = len(soup_copy.find_all('table')) > 0
        result['table_count'] = len(soup_copy.find_all('table'))
        result['tables_with_headers'] = len([t for t in soup_copy.find_all('table') if t.find('th')])
        
        result['has_blockquotes'] = len(soup_copy.find_all('blockquote')) > 0
        result['blockquote_count'] = len(soup_copy.find_all('blockquote'))
        
        result['has_code_blocks'] = len(soup_copy.find_all(['code', 'pre'])) > 0
        result['code_block_count'] = len(soup_copy.find_all('pre'))
        
        result['bold_text_count'] = len(soup_copy.find_all(['b', 'strong']))
        result['italic_text_count'] = len(soup_copy.find_all(['i', 'em']))
        result['underline_text_count'] = len(soup_copy.find_all('u'))
        result['highlighted_text'] = len(soup_copy.find_all('mark'))
        
        result['video_count'] = len(self.soup.find_all('video'))
        result['audio_count'] = len(self.soup.find_all('audio'))
        result['iframe_count'] = len(self.soup.find_all('iframe'))
        result['embed_count'] = len(self.soup.find_all('embed'))
        result['object_count'] = len(self.soup.find_all('object'))
        
        score = 100
        if result['word_count'] < 300:
            score -= 20
            self.issues["warnings"].append(f"Low word count ({result['word_count']}). Aim for 300+ words")
        elif result['word_count'] >= 1000:
            self.issues["passed"].append(f"Good content length ({result['word_count']} words)")
        
        if not result['has_lists']:
            score -= 5
        
        result['score'] = max(0, score)
        
        return result
    
    def _count_syllables(self, word: str) -> int:
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        prev_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count = 1
        return count
    
    def analyze_mobile_ux(self) -> dict:
        result = {}
        
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        result['is_mobile_friendly'] = viewport is not None
        
        amp_link = self.soup.find('link', attrs={'rel': 'amphtml'})
        result['has_amp_version'] = amp_link is not None
        result['amp_url'] = amp_link.get('href') if amp_link else None
        
        touch_icons = self.soup.find_all('link', attrs={'rel': lambda x: x and 'apple-touch-icon' in x if x else False})
        result['touch_icons_count'] = len(touch_icons)
        
        theme_color = self.soup.find('meta', attrs={'name': 'theme-color'})
        result['has_theme_color'] = theme_color is not None
        result['theme_color'] = theme_color.get('content') if theme_color else None
        
        ios_app = self.soup.find('meta', attrs={'name': 'apple-itunes-app'})
        android_app = self.soup.find('meta', attrs={'name': 'google-play-app'})
        result['has_mobile_app_links'] = ios_app is not None or android_app is not None
        result['ios_app_link'] = ios_app.get('content') if ios_app else None
        result['android_app_link'] = android_app.get('content') if android_app else None
        
        score = 100
        if not result['is_mobile_friendly']:
            score -= 30
        if not result['has_theme_color']:
            score -= 5
        
        result['score'] = max(0, score)
        
        return result
    
    def analyze_internationalization(self) -> dict:
        result = {}
        
        hreflang_links = self.soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
        result['has_hreflang'] = len(hreflang_links) > 0
        result['hreflang_count'] = len(hreflang_links)
        result['hreflang_tags'] = [
            {'lang': link.get('hreflang'), 'url': link.get('href')}
            for link in hreflang_links
        ]
        result['has_x_default'] = any(link.get('hreflang') == 'x-default' for link in hreflang_links)
        
        content_lang = self.soup.find('meta', attrs={'http-equiv': 'content-language'})
        result['content_language'] = content_lang.get('content') if content_lang else None
        
        html_tag = self.soup.find('html')
        result['detected_language'] = html_tag.get('lang') if html_tag else None
        
        result['has_direction_attr'] = html_tag.get('dir') is not None if html_tag else False
        result['text_direction'] = html_tag.get('dir') if html_tag else None
        
        score = 100
        if result['hreflang_count'] > 0 and not result['has_x_default']:
            score -= 10
            self.issues["recommendations"].append("Add x-default hreflang for international SEO")
        
        result['score'] = score
        
        return result
    
    def analyze_social(self) -> dict:
        result = {}
        
        links = self.soup.find_all('a', href=True)
        social_links = {}
        
        for link in links:
            href = link.get('href', '').lower()
            for platform, pattern in self.SOCIAL_PATTERNS.items():
                if re.search(pattern, href):
                    social_links[platform] = href
                    break
        
        result['social_links'] = social_links
        result['social_links_count'] = len(social_links)
        
        share_patterns = ['share', 'social-share', 'sharing', 'addthis', 'sharethis']
        share_elements = []
        for pattern in share_patterns:
            share_elements.extend(self.soup.find_all(class_=lambda x: x and pattern in x.lower() if x else False))
        result['has_share_buttons'] = len(share_elements) > 0
        
        review_patterns = ['review', 'testimonial', 'rating', 'stars']
        has_social_proof = False
        for pattern in review_patterns:
            if self.soup.find(class_=lambda x: x and pattern in x.lower() if x else False):
                has_social_proof = True
                break
        result['has_social_proof'] = has_social_proof
        
        score = 100
        if result['social_links_count'] == 0:
            score -= 20
        if not result['has_share_buttons']:
            score -= 10
        
        result['score'] = max(0, score)
        
        return result
    
    def analyze_ecommerce(self) -> dict:
        result = {}
        
        schema_scripts = self.soup.find_all('script', attrs={'type': 'application/ld+json'})
        all_schemas = []
        
        for script in schema_scripts:
            try:
                if script.string:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        all_schemas.append(data)
                        if '@graph' in data:
                            all_schemas.extend(data['@graph'])
                    elif isinstance(data, list):
                        all_schemas.extend(data)
            except:
                pass
        
        schema_types = [s.get('@type', '') for s in all_schemas if isinstance(s, dict)]
        
        result['has_product_schema'] = 'Product' in schema_types
        result['has_breadcrumb_schema'] = 'BreadcrumbList' in schema_types
        result['has_faq_schema'] = 'FAQPage' in schema_types
        result['has_howto_schema'] = 'HowTo' in schema_types
        result['has_recipe_schema'] = 'Recipe' in schema_types
        result['has_event_schema'] = 'Event' in schema_types
        result['has_local_business_schema'] = any('LocalBusiness' in t or 'Organization' in t for t in schema_types)
        result['has_reviews_schema'] = 'Review' in schema_types or 'AggregateRating' in schema_types
        
        for schema in all_schemas:
            if isinstance(schema, dict) and schema.get('@type') == 'Product':
                result['product_name'] = schema.get('name')
                offers = schema.get('offers', {})
                if isinstance(offers, dict):
                    result['product_price'] = offers.get('price')
                    result['product_currency'] = offers.get('priceCurrency')
                    result['product_availability'] = offers.get('availability')
                rating = schema.get('aggregateRating', {})
                if isinstance(rating, dict):
                    result['product_rating'] = rating.get('ratingValue')
                    result['product_review_count'] = rating.get('reviewCount')
                break
        
        breadcrumb_patterns = ['breadcrumb', 'bread-crumb', 'breadcrumbs']
        breadcrumb_el = None
        for pattern in breadcrumb_patterns:
            breadcrumb_el = self.soup.find(class_=lambda x: x and pattern in x.lower() if x else False)
            if breadcrumb_el:
                break
        
        result['has_breadcrumbs'] = breadcrumb_el is not None or result['has_breadcrumb_schema']
        if breadcrumb_el:
            result['breadcrumb_levels'] = len(breadcrumb_el.find_all('a'))
        
        if result['has_faq_schema']:
            for schema in all_schemas:
                if isinstance(schema, dict) and schema.get('@type') == 'FAQPage':
                    result['faq_questions_count'] = len(schema.get('mainEntity', []))
                    break
        
        score = 0
        if result['has_product_schema']:
            score += 20
        if result['has_breadcrumb_schema']:
            score += 15
        if result['has_faq_schema']:
            score += 15
        if result['has_local_business_schema']:
            score += 20
        if result['has_reviews_schema']:
            score += 15
        if result['has_breadcrumbs']:
            score += 15
            self.issues["passed"].append("Breadcrumb navigation present")
        
        result['score'] = min(100, score)
        
        return result
    
    def analyze_accessibility(self) -> dict:
        result = {}
        
        skip_link = self.soup.find('a', href='#main') or self.soup.find('a', href='#content')
        skip_link = skip_link or self.soup.find('a', class_=lambda x: x and 'skip' in x.lower() if x else False)
        result['has_skip_link'] = skip_link is not None
        
        result['has_main_landmark'] = self.soup.find('main') is not None or \
                                      self.soup.find(attrs={'role': 'main'}) is not None
        result['has_nav_landmark'] = self.soup.find('nav') is not None or \
                                     self.soup.find(attrs={'role': 'navigation'}) is not None
        result['has_footer_landmark'] = self.soup.find('footer') is not None or \
                                        self.soup.find(attrs={'role': 'contentinfo'}) is not None
        
        inputs = self.soup.find_all(['input', 'textarea', 'select'])
        labels = self.soup.find_all('label')
        
        result['form_inputs_count'] = len(inputs)
        result['form_labels_count'] = len(labels)
        
        labeled_inputs = set()
        for label in labels:
            for_attr = label.get('for')
            if for_attr:
                labeled_inputs.add(for_attr)
        
        unlabeled = 0
        for inp in inputs:
            inp_id = inp.get('id')
            inp_type = inp.get('type', '').lower()
            if inp_type not in ['hidden', 'submit', 'button', 'reset']:
                if not inp_id or inp_id not in labeled_inputs:
                    if not inp.get('aria-label') and not inp.get('aria-labelledby'):
                        unlabeled += 1
        
        result['forms_without_labels'] = unlabeled
        
        result['aria_labels_count'] = len(self.soup.find_all(attrs={'aria-label': True}))
        result['aria_roles_count'] = len(self.soup.find_all(attrs={'role': True}))
        result['tabindex_elements'] = len(self.soup.find_all(attrs={'tabindex': True}))
        
        score = 100
        if not result['has_main_landmark']:
            score -= 10
        if not result['has_nav_landmark']:
            score -= 5
        if result['forms_without_labels'] > 0:
            score -= 15
            self.issues["warnings"].append(f"{result['forms_without_labels']} form inputs without labels")
        
        result['score'] = max(0, score)
        
        if result['has_main_landmark']:
            self.issues["passed"].append("Main landmark is present")
        
        return result
    
    def analyze_performance_hints(self) -> dict:
        result = {}
        
        preload_links = self.soup.find_all('link', attrs={'rel': 'preload'})
        result['has_preload'] = len(preload_links) > 0
        result['preload_resources'] = [link.get('href') for link in preload_links]
        
        prefetch_links = self.soup.find_all('link', attrs={'rel': 'prefetch'})
        result['has_prefetch'] = len(prefetch_links) > 0
        result['prefetch_resources'] = [link.get('href') for link in prefetch_links]
        
        preconnect_links = self.soup.find_all('link', attrs={'rel': 'preconnect'})
        result['has_preconnect'] = len(preconnect_links) > 0
        result['preconnect_domains'] = [link.get('href') for link in preconnect_links]
        
        dns_prefetch = self.soup.find_all('link', attrs={'rel': 'dns-prefetch'})
        result['has_dns_prefetch'] = len(dns_prefetch) > 0
        
        result['has_resource_hints'] = any([
            result['has_preload'], result['has_prefetch'],
            result['has_preconnect'], result['has_dns_prefetch']
        ])
        
        score = 0
        if result['has_preload']:
            score += 25
        if result['has_preconnect']:
            score += 25
        if result['has_dns_prefetch']:
            score += 25
        if result['has_prefetch']:
            score += 25
        
        result['score'] = score
        
        if not result['has_resource_hints']:
            self.issues["recommendations"].append("Add resource hints (preconnect, preload) for faster loading")
        else:
            self.issues["passed"].append("Resource hints are configured")
        
        return result
    
    def analyze_crawling_indexing(self) -> dict:
        """Analyze crawling and indexing factors from Plerdy checklist"""
        result = {}
        
        # Check if URL is indexable
        robots_meta = self.soup.find('meta', attrs={'name': 'robots'})
        robots_content = robots_meta.get('content', '').lower() if robots_meta else ''
        
        # X-Robots-Tag header
        x_robots = self.headers.get('X-Robots-Tag', '')
        result['x_robots_tag'] = x_robots if x_robots else None
        
        result['is_indexable'] = 'noindex' not in robots_content and 'noindex' not in x_robots.lower()
        
        if not result['is_indexable']:
            self.issues["critical"].append("Page is set to NOINDEX - will not appear in search results")
        else:
            self.issues["passed"].append("Page is indexable")
        
        # URL structure analysis
        parsed = urlparse(self.url)
        result['url_length'] = len(self.url)
        result['url_has_parameters'] = bool(parsed.query)
        result['url_has_underscores'] = '_' in parsed.path
        result['url_depth'] = len([p for p in parsed.path.split('/') if p])
        
        # Check for friendly URL structure
        result['url_structure_friendly'] = (
            not result['url_has_parameters'] and
            not result['url_has_underscores'] and
            result['url_depth'] <= 4 and
            result['url_length'] <= 100
        )
        
        if result['url_length'] > 100:
            self.issues["warnings"].append(f"URL is too long ({result['url_length']} chars). Keep under 100 characters.")
        
        if result['url_has_underscores']:
            self.issues["recommendations"].append("Use hyphens instead of underscores in URLs")
        
        if result['url_depth'] > 4:
            self.issues["warnings"].append(f"URL depth is {result['url_depth']}. Consider flattening site structure.")
        
        # Check for redirect chain
        result['final_url'] = self.response.url
        result['has_redirect_chain'] = len(self.response.history) > 1
        result['redirect_chain_length'] = len(self.response.history)
        
        if result['has_redirect_chain']:
            self.issues["warnings"].append(f"Redirect chain detected ({result['redirect_chain_length']} redirects)")
        
        # 5xx error check
        result['has_5xx_error'] = 500 <= self.response.status_code < 600
        if result['has_5xx_error']:
            self.issues["critical"].append(f"Server error: {self.response.status_code}")
        
        # Check system pages that should be noindexed
        system_patterns = ['/search', '/cart', '/checkout', '/login', '/register', '/account', '/wishlist']
        current_path = parsed.path.lower()
        is_system_page = any(pattern in current_path for pattern in system_patterns)
        
        if is_system_page and result['is_indexable']:
            self.issues["warnings"].append("System page (search/cart/login) should have noindex directive")
            result['has_noindex_system_pages'] = False
        else:
            result['has_noindex_system_pages'] = True
        
        # Score calculation
        score = 100
        if not result['is_indexable']:
            score -= 50
        if result['has_redirect_chain']:
            score -= 15
        if not result['url_structure_friendly']:
            score -= 10
        if result['has_5xx_error']:
            score -= 40
        
        result['score'] = max(0, score)
        
        return result
    
    def analyze_content_quality(self) -> dict:
        """Analyze content quality factors from Plerdy checklist"""
        result = {}
        
        # Check for thin content
        text = self.soup.get_text(separator=' ')
        word_count = len(re.findall(r'\b[a-zA-Z]+\b', text))
        result['has_thin_content'] = word_count < 300
        
        if result['has_thin_content']:
            self.issues["warnings"].append(f"Thin content detected ({word_count} words). Aim for 300+ words for quality content.")
        
        # Check for privacy policy, contact, about pages (via links)
        all_links = self.soup.find_all('a', href=True)
        link_hrefs = [a.get('href', '').lower() for a in all_links]
        link_texts = [a.get_text().lower() for a in all_links]
        
        result['has_privacy_policy'] = any('privacy' in h or 'privacy' in t for h, t in zip(link_hrefs, link_texts))
        result['has_contact_page'] = any('contact' in h or 'contact' in t for h, t in zip(link_hrefs, link_texts))
        result['has_about_page'] = any('about' in h or 'about' in t for h, t in zip(link_hrefs, link_texts))
        
        if not result['has_privacy_policy']:
            self.issues["recommendations"].append("Add a Privacy Policy page and link to it")
        else:
            self.issues["passed"].append("Privacy Policy link found")
        
        if not result['has_contact_page']:
            self.issues["recommendations"].append("Add a Contact page and make it easy to find")
        else:
            self.issues["passed"].append("Contact page link found")
        
        # Check for publication/modified dates
        time_elements = self.soup.find_all(['time', 'meta'])
        for el in time_elements:
            if el.name == 'time':
                datetime_attr = el.get('datetime')
                if datetime_attr:
                    if not result.get('publication_date'):
                        result['publication_date'] = datetime_attr
            elif el.name == 'meta':
                if el.get('property') == 'article:published_time':
                    result['publication_date'] = el.get('content')
                elif el.get('property') == 'article:modified_time':
                    result['modified_date'] = el.get('content')
        
        # Check for author info
        author_meta = self.soup.find('meta', attrs={'name': 'author'})
        author_schema = None
        schema_scripts = self.soup.find_all('script', attrs={'type': 'application/ld+json'})
        for script in schema_scripts:
            try:
                if script.string:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        if data.get('@type') == 'Article' and 'author' in data:
                            author_schema = data['author']
                        elif '@graph' in data:
                            for item in data['@graph']:
                                if item.get('@type') == 'Article' and 'author' in item:
                                    author_schema = item['author']
            except:
                pass
        
        result['has_author_info'] = author_meta is not None or author_schema is not None
        if author_meta:
            result['author_name'] = author_meta.get('content')
        elif author_schema:
            if isinstance(author_schema, dict):
                result['author_name'] = author_schema.get('name')
            elif isinstance(author_schema, str):
                result['author_name'] = author_schema
        
        if result['has_author_info']:
            self.issues["passed"].append("Author information is present (E-E-A-T signal)")
        else:
            self.issues["recommendations"].append("Add author information for better E-E-A-T signals")
        
        # Check for content in iframes
        iframes = self.soup.find_all('iframe')
        main_content_iframes = [iframe for iframe in iframes if not iframe.get('src', '').startswith('https://www.youtube') 
                                and not iframe.get('src', '').startswith('https://www.google.com/maps')]
        result['content_in_iframes'] = len(main_content_iframes) > 0
        
        if result['content_in_iframes']:
            self.issues["warnings"].append("Important content may be inside iframes - not easily crawlable")
        
        # Check for intrusive interstitials
        popup_patterns = ['modal', 'popup', 'overlay', 'interstitial', 'lightbox']
        result['has_intrusive_interstitials'] = any(
            self.soup.find(class_=lambda x: x and pattern in x.lower() if x else False)
            for pattern in popup_patterns
        )
        
        # Check for heavy above-the-fold ads
        ad_patterns = ['advertisement', 'ad-slot', 'ad-container', 'adsense', 'ad-banner']
        ads_above_fold = sum(1 for pattern in ad_patterns if 
                           self.soup.find(class_=lambda x: x and pattern in x.lower() if x else False))
        result['has_heavy_above_fold_ads'] = ads_above_fold > 2
        result['ad_density_ratio'] = ads_above_fold / max(1, len(self.soup.find_all(['div', 'section']))) * 100
        
        if result['has_heavy_above_fold_ads']:
            self.issues["warnings"].append("Heavy ad density detected - may impact user experience and rankings")
        
        # Check for hidden text (common spam technique)
        hidden_patterns = ['display:none', 'visibility:hidden', 'font-size:0', 'color:white']
        potential_hidden = []
        for element in self.soup.find_all(style=True):
            style = element.get('style', '').lower().replace(' ', '')
            if any(pattern.replace(' ', '') in style for pattern in hidden_patterns):
                if element.get_text().strip():
                    potential_hidden.append(element.get_text()[:50])
        
        result['has_hidden_text'] = len(potential_hidden) > 0
        if result['has_hidden_text']:
            self.issues["critical"].append("Hidden text detected - this is against Google guidelines")
        
        # Check for clear CTAs
        cta_patterns = ['buy now', 'sign up', 'get started', 'learn more', 'contact us', 
                       'subscribe', 'download', 'shop now', 'order now', 'add to cart']
        all_text = text.lower()
        result['has_clear_cta'] = any(cta in all_text for cta in cta_patterns)
        
        if result['has_clear_cta']:
            self.issues["passed"].append("Clear call-to-action found")
        else:
            self.issues["recommendations"].append("Add clear calls-to-action to improve conversions")
        
        # Check for semantic HTML
        semantic_elements = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
        semantic_count = sum(len(self.soup.find_all(el)) for el in semantic_elements)
        result['uses_semantic_html'] = semantic_count >= 3
        
        if result['uses_semantic_html']:
            self.issues["passed"].append("Uses semantic HTML5 elements")
        else:
            self.issues["recommendations"].append("Use semantic HTML5 elements (header, nav, main, article, section, footer)")
        
        # E-E-A-T signals check
        eeat_signals = [
            result['has_author_info'],
            result.get('has_about_page', False),
            result.get('has_contact_page', False),
            bool(result.get('publication_date')),
            self.soup.find('meta', attrs={'name': 'author'}) is not None
        ]
        result['has_eeat_signals'] = sum(eeat_signals) >= 3
        
        # Score calculation
        score = 100
        if result['has_thin_content']:
            score -= 25
        if result['content_in_iframes']:
            score -= 15
        if result['has_hidden_text']:
            score -= 40
        if result['has_heavy_above_fold_ads']:
            score -= 15
        if not result['uses_semantic_html']:
            score -= 5
        if not result['has_eeat_signals']:
            score -= 10
        
        result['score'] = max(0, score)
        
        return result
    
    def analyze_keyword_optimization(self) -> dict:
        """Analyze keyword optimization from Plerdy checklist"""
        result = {
            'target_keyword': self.target_keyword,
            'keyword_in_title': False,
            'keyword_in_title_position': -1,
            'keyword_in_meta_desc': False,
            'keyword_in_h1': False,
            'keyword_in_h2': False,
            'keyword_in_first_paragraph': False,
            'keyword_in_body': False,
            'keyword_count_in_body': 0,
            'keyword_density_percent': 0.0,
            'keyword_overuse': False
        }
        
        if not self.target_keyword:
            result['score'] = 50  # Neutral score if no keyword set
            return result
        
        keyword = self.target_keyword.lower()
        
        # Title analysis
        title_tag = self.soup.find('title')
        if title_tag:
            title_text = title_tag.get_text().lower()
            result['keyword_in_title'] = keyword in title_text
            if result['keyword_in_title']:
                result['keyword_in_title_position'] = title_text.find(keyword)
                result['title_starts_with_keyword'] = title_text.strip().startswith(keyword)
                self.issues["passed"].append("Target keyword found in title")
                if result['keyword_in_title_position'] == 0 or result['keyword_in_title_position'] < 20:
                    self.issues["passed"].append("Keyword is placed early in title")
            else:
                self.issues["recommendations"].append(f"Add target keyword '{self.target_keyword}' to the title")
        
        # Meta description analysis
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            desc_text = meta_desc.get('content', '').lower()
            result['keyword_in_meta_desc'] = keyword in desc_text
            if result['keyword_in_meta_desc']:
                self.issues["passed"].append("Target keyword found in meta description")
            else:
                self.issues["recommendations"].append("Add target keyword to meta description for better CTR")
        
        # H1 analysis
        h1_tags = self.soup.find_all('h1')
        for h1 in h1_tags:
            if keyword in h1.get_text().lower():
                result['keyword_in_h1'] = True
                self.issues["passed"].append("Target keyword found in H1")
                break
        
        if not result['keyword_in_h1'] and h1_tags:
            self.issues["recommendations"].append("Include target keyword in the H1 heading")
        
        # H2 analysis
        h2_tags = self.soup.find_all('h2')
        for h2 in h2_tags:
            if keyword in h2.get_text().lower():
                result['keyword_in_h2'] = True
                self.issues["passed"].append("Target keyword found in H2 subheading")
                break
        
        if not result['keyword_in_h2'] and h2_tags:
            self.issues["recommendations"].append("Include target keyword (or close variant) in an H2 subheading")
        
        # Body content analysis
        body_text = self.soup.get_text().lower()
        words = re.findall(r'\b[a-zA-Z]+\b', body_text)
        total_words = len(words)
        
        # Count keyword occurrences
        keyword_pattern = re.escape(keyword)
        keyword_matches = re.findall(keyword_pattern, body_text)
        result['keyword_count_in_body'] = len(keyword_matches)
        result['keyword_in_body'] = result['keyword_count_in_body'] > 0
        
        if total_words > 0:
            result['keyword_density_percent'] = round((result['keyword_count_in_body'] / total_words) * 100, 2)
        
        # Check for keyword overuse (>3% is generally considered stuffing)
        result['keyword_overuse'] = result['keyword_density_percent'] > 3.0
        
        if result['keyword_overuse']:
            self.issues["warnings"].append(f"Keyword density too high ({result['keyword_density_percent']}%). Risk of keyword stuffing.")
        elif result['keyword_density_percent'] > 0 and result['keyword_density_percent'] < 0.5:
            self.issues["recommendations"].append("Keyword density is low. Consider using the keyword more naturally in content.")
        elif 0.5 <= result['keyword_density_percent'] <= 2.5:
            self.issues["passed"].append(f"Keyword density is optimal ({result['keyword_density_percent']}%)")
        
        # First paragraph check
        paragraphs = self.soup.find_all('p')
        if paragraphs:
            first_para = paragraphs[0].get_text().lower() if paragraphs else ''
            result['keyword_in_first_paragraph'] = keyword in first_para
            if result['keyword_in_first_paragraph']:
                self.issues["passed"].append("Target keyword found in opening paragraph")
            else:
                self.issues["recommendations"].append("Include target keyword in the opening paragraph")
        
        # Score calculation
        score = 0
        if result['keyword_in_title']:
            score += 20
        if result['keyword_in_title_position'] < 20:
            score += 10
        if result['keyword_in_meta_desc']:
            score += 15
        if result['keyword_in_h1']:
            score += 20
        if result['keyword_in_h2']:
            score += 10
        if result['keyword_in_first_paragraph']:
            score += 15
        if result['keyword_in_body'] and not result['keyword_overuse']:
            score += 10
        
        if result['keyword_overuse']:
            score -= 30
        
        result['score'] = max(0, min(100, score))
        
        return result
    
    def analyze_mobile_advanced(self) -> dict:
        """Analyze advanced mobile factors from Plerdy checklist"""
        result = {}
        
        # Page weight
        page_size_kb = len(self.response.content) / 1024
        result['mobile_page_weight_kb'] = round(page_size_kb, 2)
        result['mobile_page_heavy'] = page_size_kb > 1500  # 1.5MB threshold for mobile
        
        if result['mobile_page_heavy']:
            self.issues["warnings"].append(f"Page is heavy for mobile ({result['mobile_page_weight_kb']}KB). Aim for under 1.5MB.")
        
        # Responsive images check
        images = self.soup.find_all('img')
        images_with_srcset = sum(1 for img in images if img.get('srcset'))
        result['has_responsive_images'] = images_with_srcset > len(images) * 0.5 if images else True
        
        if not result['has_responsive_images'] and len(images) > 3:
            self.issues["recommendations"].append("Use responsive images with srcset attribute for mobile optimization")
        
        # Check for properly sized images (those with width/height attributes)
        images_with_dimensions = sum(1 for img in images if img.get('width') or img.get('height'))
        result['images_properly_sized'] = images_with_dimensions >= len(images) * 0.5 if images else True
        
        # Font size check (look for very small font sizes in styles)
        small_fonts = 0
        for element in self.soup.find_all(style=True):
            style = element.get('style', '')
            font_match = re.search(r'font-size:\s*(\d+)', style)
            if font_match and int(font_match.group(1)) < 12:
                small_fonts += 1
        
        result['font_sizes_readable'] = small_fonts == 0
        result['small_font_elements'] = small_fonts
        
        if not result['font_sizes_readable']:
            self.issues["warnings"].append(f"{small_fonts} elements with small font sizes detected. Ensure readability on mobile.")
        else:
            self.issues["passed"].append("Font sizes appear readable")
        
        # Tap target analysis (buttons, links should be adequately sized)
        links = self.soup.find_all('a')
        tap_issues = 0
        for link in links:
            # Check if link has very short text (potential tap target issue)
            text = link.get_text().strip()
            if text and len(text) < 3 and not link.find('img'):
                tap_issues += 1
        
        result['tap_targets_sized_correctly'] = tap_issues < 5
        result['tap_target_issues'] = tap_issues
        
        if tap_issues > 5:
            self.issues["warnings"].append(f"{tap_issues} potential tap target issues. Ensure clickable elements are adequately sized.")
        
        # Viewport meta check
        viewport = self.soup.find('meta', attrs={'name': 'viewport'})
        result['content_width_fits_viewport'] = viewport is not None
        
        # Mobile navigation check
        nav = self.soup.find('nav') or self.soup.find(class_=lambda x: x and 'nav' in x.lower() if x else False)
        hamburger_patterns = ['hamburger', 'mobile-menu', 'menu-toggle', 'nav-toggle']
        has_mobile_nav = any(self.soup.find(class_=lambda x: x and pattern in x.lower() if x else False) 
                           for pattern in hamburger_patterns)
        result['mobile_navigation_friendly'] = nav is not None
        result['thumb_friendly_navigation'] = has_mobile_nav or nav is not None
        
        # Favicon in mobile SERPs (check for proper favicon setup)
        favicon = self.soup.find('link', attrs={'rel': lambda x: x and 'icon' in x.lower() if x else False})
        result['favicon_in_mobile_serps'] = favicon is not None
        
        # Mobile-desktop parity checks
        result['mobile_desktop_parity'] = True  # Assume true unless specific issues detected
        result['mobile_meta_parity'] = True
        result['mobile_directives_parity'] = True
        
        # Score calculation
        score = 100
        if result['mobile_page_heavy']:
            score -= 20
        if not result['has_responsive_images']:
            score -= 10
        if not result['font_sizes_readable']:
            score -= 15
        if not result['tap_targets_sized_correctly']:
            score -= 15
        if not result['mobile_navigation_friendly']:
            score -= 10
        if not result['favicon_in_mobile_serps']:
            score -= 5
        
        result['score'] = max(0, score)
        
        return result
    
    def analyze_page_elements(self) -> dict:
        """Analyze page elements from Plerdy checklist"""
        result = {}
        
        # Multiple H1 check
        h1_tags = self.soup.find_all('h1')
        result['has_multiple_h1'] = len(h1_tags) > 1
        
        if result['has_multiple_h1']:
            self.issues["warnings"].append(f"Multiple H1 tags found ({len(h1_tags)}). Use only one H1 per page.")
        
        # Title matches content check
        title_tag = self.soup.find('title')
        h1_text = h1_tags[0].get_text().lower() if h1_tags else ''
        title_text = title_tag.get_text().lower() if title_tag else ''
        
        # Simple check: title and H1 should share some keywords
        title_words = set(re.findall(r'\b\w+\b', title_text))
        h1_words = set(re.findall(r'\b\w+\b', h1_text))
        common_words = title_words & h1_words - {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        result['title_matches_content'] = len(common_words) >= 2 if title_words and h1_words else True
        
        if not result['title_matches_content']:
            self.issues["recommendations"].append("Title and H1 should be related - ensure they describe the same topic")
        
        # Meta description uniqueness (basic check - just verify it's not a duplicate of title)
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        desc_text = meta_desc.get('content', '') if meta_desc else ''
        result['meta_desc_is_unique'] = desc_text.lower() != title_text and len(desc_text) > 0
        
        if not result['meta_desc_is_unique'] and desc_text:
            self.issues["warnings"].append("Meta description should be unique and not duplicate the title")
        
        # Check if meta description is compelling (has power words or CTA)
        compelling_words = ['discover', 'learn', 'get', 'find', 'best', 'top', 'ultimate', 'free', 'easy', 'proven', 'exclusive']
        result['meta_desc_compelling'] = any(word in desc_text.lower() for word in compelling_words)
        
        if not result['meta_desc_compelling'] and desc_text:
            self.issues["recommendations"].append("Make meta description more compelling with action words or unique value proposition")
        
        # Links distinguishable check
        links = self.soup.find_all('a')
        styled_links = sum(1 for link in links if link.get('style') or link.get('class'))
        result['links_distinguishable'] = True  # Assume true; proper check requires CSS parsing
        
        # Text contrast check (basic - look for potential issues)
        low_contrast_patterns = ['color:#fff', 'color:white', 'color:#ccc', 'color:#ddd']
        contrast_issues = 0
        for element in self.soup.find_all(style=True):
            style = element.get('style', '').lower().replace(' ', '')
            if any(pattern.replace(' ', '') in style for pattern in low_contrast_patterns):
                contrast_issues += 1
        result['text_contrast_sufficient'] = contrast_issues < 3
        
        if not result['text_contrast_sufficient']:
            self.issues["warnings"].append("Potential text contrast issues detected. Ensure sufficient contrast for readability.")
        
        # Primary content clear check
        main_element = self.soup.find('main') or self.soup.find('article')
        result['primary_content_clear'] = main_element is not None
        
        if result['primary_content_clear']:
            self.issues["passed"].append("Primary content is clearly marked with semantic HTML")
        else:
            self.issues["recommendations"].append("Use <main> or <article> tags to clearly mark primary content")
        
        # Supplementary content marked
        aside_elements = self.soup.find_all('aside')
        result['supplementary_content_marked'] = len(aside_elements) > 0
        
        # Score calculation
        score = 100
        if result['has_multiple_h1']:
            score -= 15
        if not result['title_matches_content']:
            score -= 10
        if not result['meta_desc_is_unique']:
            score -= 10
        if not result['text_contrast_sufficient']:
            score -= 10
        if not result['primary_content_clear']:
            score -= 10
        
        result['score'] = max(0, score)
        
        return result
    
    def calculate_score(self, category_scores: dict) -> Tuple[int, str]:
        weights = {
            'meta': 15,
            'headings': 10,
            'images': 10,
            'links': 10,
            'technical': 20,
            'content': 15,
            'mobile_ux': 10,
            'social': 5,
            'ecommerce': 5
        }
        
        total_score = 0
        total_weight = sum(weights.values())
        
        for category, weight in weights.items():
            score = category_scores.get(category, 50)
            total_score += (score * weight)
        
        final_score = int(total_score / total_weight)
        
        final_score -= len(self.issues["critical"]) * 5
        final_score -= len(self.issues["warnings"]) * 1
        
        final_score = max(0, min(100, final_score))
        
        if final_score >= 90:
            grade = "A+"
        elif final_score >= 80:
            grade = "A"
        elif final_score >= 70:
            grade = "B"
        elif final_score >= 60:
            grade = "C"
        elif final_score >= 50:
            grade = "D"
        else:
            grade = "F"
        
        return final_score, grade
    
    def run_audit(self) -> Optional[SEOAuditResult]:
        print(f"\n🔍 Starting Advanced SEO Audit for: {self.url}")
        print("=" * 60)
        print("Analyzing 200+ SEO parameters...")
        
        # Reset issues to ensure fresh state
        self.issues = {"critical": [], "warnings": [], "recommendations": [], "passed": []}
        
        if not self.fetch_page():
            return None
        
        print("  ✓ Analyzing meta tags...")
        title_data = self.analyze_title()
        meta_desc_data = self.analyze_meta_description()
        meta_data = self.analyze_meta_tags()
        
        print("  ✓ Analyzing Open Graph & Twitter Cards...")
        og_data = self.analyze_open_graph()
        twitter_data = self.analyze_twitter_cards()
        
        print("  ✓ Analyzing headings...")
        headings_data = self.analyze_headings()
        
        print("  ✓ Analyzing images...")
        images_data = self.analyze_images()
        
        print("  ✓ Analyzing links...")
        links_data = self.analyze_links()
        
        print("  ✓ Analyzing technical SEO...")
        technical_data = self.analyze_technical()
        
        print("  ✓ Analyzing content...")
        content_data = self.analyze_content()
        
        print("  ✓ Analyzing mobile & UX...")
        mobile_data = self.analyze_mobile_ux()
        
        print("  ✓ Analyzing internationalization...")
        i18n_data = self.analyze_internationalization()
        
        print("  ✓ Analyzing social integration...")
        social_data = self.analyze_social()
        
        print("  ✓ Analyzing e-commerce & rich snippets...")
        ecommerce_data = self.analyze_ecommerce()
        
        print("  ✓ Analyzing accessibility...")
        accessibility_data = self.analyze_accessibility()
        
        print("  ✓ Analyzing performance hints...")
        performance_data = self.analyze_performance_hints()
        
        print("  ✓ Analyzing crawling & indexing...")
        crawling_data = self.analyze_crawling_indexing()
        
        print("  ✓ Analyzing content quality...")
        content_quality_data = self.analyze_content_quality()
        
        print("  ✓ Analyzing keyword optimization...")
        keyword_data = self.analyze_keyword_optimization()
        
        print("  ✓ Analyzing mobile advanced features...")
        mobile_advanced_data = self.analyze_mobile_advanced()
        
        print("  ✓ Analyzing page elements...")
        page_elements_data = self.analyze_page_elements()
        
        category_scores = {
            'meta': 100 - (len([i for i in self.issues["critical"] if 'title' in i.lower() or 'meta' in i.lower()]) * 20),
            'headings': 100 if headings_data['h1_count'] == 1 else 60,
            'images': images_data.get('score', 50),
            'links': links_data.get('score', 50),
            'technical': technical_data.get('security_headers_score', 50),
            'content': content_data.get('score', 50),
            'mobile_ux': mobile_data.get('score', 50),
            'social': social_data.get('score', 50),
            'ecommerce': ecommerce_data.get('score', 50),
            'crawling': crawling_data.get('score', 50),
            'content_quality': content_quality_data.get('score', 50),
            'keyword': keyword_data.get('score', 50),
            'mobile_advanced': mobile_advanced_data.get('score', 50),
            'page_elements': page_elements_data.get('score', 50)
        }
        
        score, grade = self.calculate_score(category_scores)
        
        result = SEOAuditResult(
            url=self.url,
            audit_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            score=score,
            grade=grade,
            
            title=title_data["title"],
            title_length=title_data["length"],
            title_status=title_data["status"],
            title_has_keyword=title_data["has_keyword"],
            title_has_numbers=title_data["has_numbers"],
            title_has_power_words=title_data["has_power_words"],
            title_pixel_width=title_data["pixel_width"],
            
            meta_description=meta_desc_data["description"],
            meta_description_length=meta_desc_data["length"],
            meta_description_status=meta_desc_data["status"],
            meta_description_has_keyword=meta_desc_data["has_keyword"],
            meta_description_has_cta=meta_desc_data["has_cta"],
            
            meta_keywords=meta_data["keywords"],
            meta_keywords_count=meta_data["keywords_count"],
            canonical_url=meta_data["canonical_url"],
            canonical_is_self=meta_data["canonical_is_self"],
            robots_meta=meta_data["robots_meta"],
            robots_index=meta_data["robots_index"],
            robots_follow=meta_data["robots_follow"],
            meta_author=meta_data.get("meta_author"),
            meta_publisher=meta_data.get("meta_publisher"),
            meta_language=meta_data.get("meta_language"),
            meta_referrer=meta_data.get("meta_referrer"),
            
            og_title=og_data.get("title"),
            og_description=og_data.get("description"),
            og_image=og_data.get("image"),
            og_image_width=og_data.get("image_width"),
            og_image_height=og_data.get("image_height"),
            og_url=og_data.get("url"),
            og_type=og_data.get("type"),
            og_site_name=og_data.get("site_name"),
            og_locale=og_data.get("locale"),
            og_complete=og_data.get("complete", False),
            og_score=og_data.get("score", 0),
            
            twitter_card=twitter_data.get("card"),
            twitter_title=twitter_data.get("title"),
            twitter_description=twitter_data.get("description"),
            twitter_image=twitter_data.get("image"),
            twitter_site=twitter_data.get("site"),
            twitter_creator=twitter_data.get("creator"),
            twitter_complete=twitter_data.get("complete", False),
            twitter_score=twitter_data.get("score", 0),
            
            h1_count=headings_data["h1_count"],
            h1_tags=headings_data.get("h1_tags", []),
            h1_length_avg=headings_data.get("h1_length_avg", 0),
            h1_has_keyword=headings_data.get("h1_has_keyword", False),
            h2_count=headings_data["h2_count"],
            h2_tags=headings_data.get("h2_tags", []),
            h3_count=headings_data["h3_count"],
            h3_tags=headings_data.get("h3_tags", []),
            h4_count=headings_data.get("h4_count", 0),
            h5_count=headings_data.get("h5_count", 0),
            h6_count=headings_data.get("h6_count", 0),
            total_headings=headings_data.get("total_headings", 0),
            heading_hierarchy_valid=headings_data.get("hierarchy_valid", False),
            heading_structure_status=headings_data["status"],
            empty_headings=headings_data.get("empty_headings", 0),
            duplicate_headings=headings_data.get("duplicate_headings", 0),
            long_headings=headings_data.get("long_headings", 0),
            
            total_images=images_data["total"],
            images_without_alt=images_data["without_alt"],
            images_with_empty_alt=images_data.get("with_empty_alt", 0),
            images_with_title=images_data.get("with_title", 0),
            images_without_src=images_data.get("without_src", 0),
            images_status=images_data["status"],
            images_with_lazy_loading=images_data.get("with_lazy_loading", 0),
            images_with_srcset=images_data.get("with_srcset", 0),
            images_with_sizes=images_data.get("with_sizes", 0),
            images_webp=images_data.get("webp", 0),
            images_svg=images_data.get("svg", 0),
            images_png=images_data.get("png", 0),
            images_jpg=images_data.get("jpg", 0),
            images_gif=images_data.get("gif", 0),
            images_external=images_data.get("external", 0),
            images_internal=images_data.get("internal", 0),
            images_with_descriptive_filename=images_data.get("with_descriptive_filename", 0),
            images_decorative=images_data.get("decorative", 0),
            figure_elements=images_data.get("figure_elements", 0),
            images_in_picture=images_data.get("images_in_picture", 0),
            avg_alt_length=images_data.get("avg_alt_length", 0),
            images_score=images_data.get("score", 0),
            
            internal_links=links_data["internal"],
            external_links=links_data["external"],
            total_links=links_data["total"],
            unique_internal_links=links_data.get("unique_internal", 0),
            unique_external_links=links_data.get("unique_external", 0),
            nofollow_links=links_data.get("nofollow", 0),
            dofollow_links=links_data.get("dofollow", 0),
            sponsored_links=links_data.get("sponsored", 0),
            ugc_links=links_data.get("ugc", 0),
            links_with_title=links_data.get("with_title", 0),
            links_without_title=links_data.get("without_title", 0),
            links_with_target_blank=links_data.get("with_target_blank", 0),
            links_with_rel_noopener=links_data.get("with_rel_noopener", 0),
            links_without_noopener=links_data.get("without_noopener", 0),
            anchor_text_distribution=links_data.get("anchor_distribution", {}),
            empty_anchor_links=links_data.get("empty_anchor", 0),
            image_links=links_data.get("image_links", 0),
            text_links=links_data.get("text_links", 0),
            javascript_links=links_data.get("javascript", 0),
            hash_links=links_data.get("hash", 0),
            mailto_links=links_data.get("mailto", 0),
            tel_links=links_data.get("tel", 0),
            broken_links=links_data.get("broken", []),
            links_score=links_data.get("score", 0),
            
            has_ssl=technical_data["has_ssl"],
            has_viewport=technical_data["has_viewport"],
            viewport_content=technical_data.get("viewport_content"),
            viewport_initial_scale=technical_data.get("viewport_initial_scale", False),
            viewport_user_scalable=technical_data.get("viewport_user_scalable", True),
            has_charset=technical_data["has_charset"],
            charset_value=technical_data.get("charset_value"),
            has_doctype=technical_data.get("has_doctype", False),
            html_lang=technical_data.get("html_lang"),
            has_favicon=technical_data["has_favicon"],
            favicon_format=technical_data.get("favicon_format"),
            has_apple_touch_icon=technical_data.get("has_apple_touch_icon", False),
            has_manifest=technical_data.get("has_manifest", False),
            manifest_url=technical_data.get("manifest_url"),
            has_schema_markup=technical_data["has_schema"],
            schema_types=technical_data["schema_types"],
            schema_count=technical_data.get("schema_count", 0),
            microdata_items=technical_data.get("microdata_items", 0),
            rdfa_items=technical_data.get("rdfa_items", 0),
            
            response_time=self.response_time,
            page_size_bytes=technical_data.get("page_size_bytes", 0),
            page_size_kb=technical_data.get("page_size_kb", 0),
            html_size_bytes=technical_data.get("html_size_bytes", 0),
            
            total_css_files=technical_data.get("total_css_files", 0),
            total_js_files=technical_data.get("total_js_files", 0),
            inline_css_count=technical_data.get("inline_css_count", 0),
            inline_js_count=technical_data.get("inline_js_count", 0),
            inline_css_size=technical_data.get("inline_css_size", 0),
            inline_js_size=technical_data.get("inline_js_size", 0),
            
            render_blocking_css=technical_data.get("render_blocking_css", 0),
            render_blocking_js=technical_data.get("render_blocking_js", 0),
            async_js=technical_data.get("async_js", 0),
            defer_js=technical_data.get("defer_js", 0),
            
            has_gzip=technical_data.get("has_gzip", False),
            content_encoding=technical_data.get("content_encoding"),
            has_cache_headers=technical_data.get("has_cache_headers", False),
            cache_control=technical_data.get("cache_control"),
            etag=technical_data.get("etag"),
            last_modified=technical_data.get("last_modified"),
            
            http_status=technical_data.get("http_status", 0),
            content_type=technical_data.get("content_type"),
            server=technical_data.get("server"),
            x_powered_by=technical_data.get("x_powered_by"),
            
            has_hsts=technical_data.get("has_hsts", False),
            has_xss_protection=technical_data.get("has_xss_protection", False),
            has_content_type_options=technical_data.get("has_content_type_options", False),
            has_frame_options=technical_data.get("has_frame_options", False),
            has_csp=technical_data.get("has_csp", False),
            security_headers_score=technical_data.get("security_headers_score", 0),
            
            word_count=content_data["word_count"],
            character_count=content_data.get("character_count", 0),
            sentence_count=content_data.get("sentence_count", 0),
            paragraph_count=content_data.get("paragraph_count", 0),
            avg_sentence_length=content_data.get("avg_sentence_length", 0),
            avg_word_length=content_data.get("avg_word_length", 0),
            
            flesch_reading_ease=content_data.get("flesch_reading_ease", 0),
            flesch_kincaid_grade=content_data.get("flesch_kincaid_grade", 0),
            readability_status=content_data.get("readability_status", ""),
            
            text_html_ratio=content_data.get("text_html_ratio", 0),
            unique_words=content_data.get("unique_words", 0),
            lexical_density=content_data.get("lexical_density", 0),
            
            top_keywords=content_data.get("top_keywords", []),
            keyword_density=content_data.get("keyword_density", {}),
            stop_words_ratio=content_data.get("stop_words_ratio", 0),
            
            has_lists=content_data.get("has_lists", False),
            ordered_lists=content_data.get("ordered_lists", 0),
            unordered_lists=content_data.get("unordered_lists", 0),
            list_items=content_data.get("list_items", 0),
            has_tables=content_data.get("has_tables", False),
            table_count=content_data.get("table_count", 0),
            tables_with_headers=content_data.get("tables_with_headers", 0),
            has_blockquotes=content_data.get("has_blockquotes", False),
            blockquote_count=content_data.get("blockquote_count", 0),
            has_code_blocks=content_data.get("has_code_blocks", False),
            code_block_count=content_data.get("code_block_count", 0),
            
            bold_text_count=content_data.get("bold_text_count", 0),
            italic_text_count=content_data.get("italic_text_count", 0),
            underline_text_count=content_data.get("underline_text_count", 0),
            highlighted_text=content_data.get("highlighted_text", 0),
            
            video_count=content_data.get("video_count", 0),
            audio_count=content_data.get("audio_count", 0),
            iframe_count=content_data.get("iframe_count", 0),
            embed_count=content_data.get("embed_count", 0),
            object_count=content_data.get("object_count", 0),
            
            content_score=content_data.get("score", 0),
            
            is_mobile_friendly=mobile_data.get("is_mobile_friendly", False),
            has_amp_version=mobile_data.get("has_amp_version", False),
            amp_url=mobile_data.get("amp_url"),
            touch_icons_count=mobile_data.get("touch_icons_count", 0),
            has_theme_color=mobile_data.get("has_theme_color", False),
            theme_color=mobile_data.get("theme_color"),
            has_mobile_app_links=mobile_data.get("has_mobile_app_links", False),
            ios_app_link=mobile_data.get("ios_app_link"),
            android_app_link=mobile_data.get("android_app_link"),
            ux_score=mobile_data.get("score", 0),
            
            has_hreflang=i18n_data.get("has_hreflang", False),
            hreflang_tags=i18n_data.get("hreflang_tags", []),
            hreflang_count=i18n_data.get("hreflang_count", 0),
            has_x_default=i18n_data.get("has_x_default", False),
            content_language=i18n_data.get("content_language"),
            detected_language=i18n_data.get("detected_language"),
            has_direction_attr=i18n_data.get("has_direction_attr", False),
            text_direction=i18n_data.get("text_direction"),
            i18n_score=i18n_data.get("score", 0),
            
            social_links=social_data.get("social_links", {}),
            social_links_count=social_data.get("social_links_count", 0),
            has_share_buttons=social_data.get("has_share_buttons", False),
            has_social_proof=social_data.get("has_social_proof", False),
            social_score=social_data.get("score", 0),
            
            has_product_schema=ecommerce_data.get("has_product_schema", False),
            product_name=ecommerce_data.get("product_name"),
            product_price=ecommerce_data.get("product_price"),
            product_currency=ecommerce_data.get("product_currency"),
            product_availability=ecommerce_data.get("product_availability"),
            product_rating=ecommerce_data.get("product_rating"),
            product_review_count=ecommerce_data.get("product_review_count"),
            has_breadcrumbs=ecommerce_data.get("has_breadcrumbs", False),
            has_breadcrumb_schema=ecommerce_data.get("has_breadcrumb_schema", False),
            breadcrumb_levels=ecommerce_data.get("breadcrumb_levels", 0),
            has_faq_schema=ecommerce_data.get("has_faq_schema", False),
            faq_questions_count=ecommerce_data.get("faq_questions_count", 0),
            has_howto_schema=ecommerce_data.get("has_howto_schema", False),
            has_recipe_schema=ecommerce_data.get("has_recipe_schema", False),
            has_event_schema=ecommerce_data.get("has_event_schema", False),
            has_local_business_schema=ecommerce_data.get("has_local_business_schema", False),
            has_reviews_schema=ecommerce_data.get("has_reviews_schema", False),
            ecommerce_score=ecommerce_data.get("score", 0),
            
            has_skip_link=accessibility_data.get("has_skip_link", False),
            has_main_landmark=accessibility_data.get("has_main_landmark", False),
            has_nav_landmark=accessibility_data.get("has_nav_landmark", False),
            has_footer_landmark=accessibility_data.get("has_footer_landmark", False),
            form_labels_count=accessibility_data.get("form_labels_count", 0),
            form_inputs_count=accessibility_data.get("form_inputs_count", 0),
            forms_without_labels=accessibility_data.get("forms_without_labels", 0),
            aria_labels_count=accessibility_data.get("aria_labels_count", 0),
            aria_roles_count=accessibility_data.get("aria_roles_count", 0),
            tabindex_elements=accessibility_data.get("tabindex_elements", 0),
            accessibility_score=accessibility_data.get("score", 0),
            
            has_preload=performance_data.get("has_preload", False),
            preload_resources=performance_data.get("preload_resources", []),
            has_prefetch=performance_data.get("has_prefetch", False),
            prefetch_resources=performance_data.get("prefetch_resources", []),
            has_preconnect=performance_data.get("has_preconnect", False),
            preconnect_domains=performance_data.get("preconnect_domains", []),
            has_dns_prefetch=performance_data.get("has_dns_prefetch", False),
            has_resource_hints=performance_data.get("has_resource_hints", False),
            performance_hints_score=performance_data.get("score", 0),
            
            # Crawling & Indexing
            is_indexable=crawling_data.get("is_indexable", True),
            robots_txt_blocks_url=crawling_data.get("robots_txt_blocks_url", False),
            x_robots_tag=crawling_data.get("x_robots_tag"),
            url_structure_friendly=crawling_data.get("url_structure_friendly", True),
            url_length=crawling_data.get("url_length", 0),
            url_has_parameters=crawling_data.get("url_has_parameters", False),
            url_has_underscores=crawling_data.get("url_has_underscores", False),
            url_depth=crawling_data.get("url_depth", 0),
            has_redirect_chain=crawling_data.get("has_redirect_chain", False),
            redirect_chain_length=crawling_data.get("redirect_chain_length", 0),
            final_url=crawling_data.get("final_url"),
            has_5xx_error=crawling_data.get("has_5xx_error", False),
            has_noindex_system_pages=crawling_data.get("has_noindex_system_pages", True),
            crawling_score=crawling_data.get("score", 0),
            
            # Content Quality
            has_thin_content=content_quality_data.get("has_thin_content", False),
            content_is_unique=content_quality_data.get("content_is_unique", True),
            has_privacy_policy=content_quality_data.get("has_privacy_policy", False),
            has_contact_page=content_quality_data.get("has_contact_page", False),
            has_about_page=content_quality_data.get("has_about_page", False),
            publication_date=content_quality_data.get("publication_date"),
            modified_date=content_quality_data.get("modified_date"),
            has_author_info=content_quality_data.get("has_author_info", False),
            author_name=content_quality_data.get("author_name"),
            has_eeat_signals=content_quality_data.get("has_eeat_signals", False),
            content_in_iframes=content_quality_data.get("content_in_iframes", False),
            has_intrusive_interstitials=content_quality_data.get("has_intrusive_interstitials", False),
            has_heavy_above_fold_ads=content_quality_data.get("has_heavy_above_fold_ads", False),
            ad_density_ratio=content_quality_data.get("ad_density_ratio", 0.0),
            has_hidden_text=content_quality_data.get("has_hidden_text", False),
            has_clear_cta=content_quality_data.get("has_clear_cta", False),
            uses_semantic_html=content_quality_data.get("uses_semantic_html", False),
            content_quality_score=content_quality_data.get("score", 0),
            
            # Keyword Analysis
            target_keyword=keyword_data.get("target_keyword"),
            keyword_in_title=keyword_data.get("keyword_in_title", False),
            keyword_in_title_position=keyword_data.get("keyword_in_title_position", -1),
            keyword_in_meta_desc=keyword_data.get("keyword_in_meta_desc", False),
            keyword_in_h1=keyword_data.get("keyword_in_h1", False),
            keyword_in_h2=keyword_data.get("keyword_in_h2", False),
            keyword_in_first_paragraph=keyword_data.get("keyword_in_first_paragraph", False),
            keyword_in_body=keyword_data.get("keyword_in_body", False),
            keyword_count_in_body=keyword_data.get("keyword_count_in_body", 0),
            keyword_density_percent=keyword_data.get("keyword_density_percent", 0.0),
            keyword_overuse=keyword_data.get("keyword_overuse", False),
            keyword_analysis_score=keyword_data.get("score", 0),
            title_starts_with_keyword=keyword_data.get("title_starts_with_keyword", False),
            
            # Mobile Advanced
            mobile_page_weight_kb=mobile_advanced_data.get("mobile_page_weight_kb", 0.0),
            mobile_page_heavy=mobile_advanced_data.get("mobile_page_heavy", False),
            has_responsive_images=mobile_advanced_data.get("has_responsive_images", False),
            images_properly_sized=mobile_advanced_data.get("images_properly_sized", True),
            tap_targets_sized_correctly=mobile_advanced_data.get("tap_targets_sized_correctly", True),
            tap_target_issues=mobile_advanced_data.get("tap_target_issues", 0),
            font_sizes_readable=mobile_advanced_data.get("font_sizes_readable", True),
            small_font_elements=mobile_advanced_data.get("small_font_elements", 0),
            content_width_fits_viewport=mobile_advanced_data.get("content_width_fits_viewport", True),
            mobile_navigation_friendly=mobile_advanced_data.get("mobile_navigation_friendly", True),
            thumb_friendly_navigation=mobile_advanced_data.get("thumb_friendly_navigation", True),
            favicon_in_mobile_serps=mobile_advanced_data.get("favicon_in_mobile_serps", False),
            mobile_desktop_parity=mobile_advanced_data.get("mobile_desktop_parity", True),
            mobile_meta_parity=mobile_advanced_data.get("mobile_meta_parity", True),
            mobile_directives_parity=mobile_advanced_data.get("mobile_directives_parity", True),
            mobile_advanced_score=mobile_advanced_data.get("score", 0),
            
            # Page Elements
            has_multiple_h1=page_elements_data.get("has_multiple_h1", False),
            title_matches_content=page_elements_data.get("title_matches_content", True),
            meta_desc_is_unique=page_elements_data.get("meta_desc_is_unique", True),
            meta_desc_compelling=page_elements_data.get("meta_desc_compelling", False),
            links_distinguishable=page_elements_data.get("links_distinguishable", True),
            text_contrast_sufficient=page_elements_data.get("text_contrast_sufficient", True),
            primary_content_clear=page_elements_data.get("primary_content_clear", True),
            supplementary_content_marked=page_elements_data.get("supplementary_content_marked", False),
            page_elements_score=page_elements_data.get("score", 0),
            
            critical_issues=self.issues["critical"],
            warnings=self.issues["warnings"],
            recommendations=self.issues["recommendations"],
            passed_checks=self.issues["passed"],
            
            meta_score=category_scores.get('meta', 0),
            heading_score=category_scores.get('headings', 0),
            technical_score=category_scores.get('technical', 0),
            meta_tags_score=category_scores.get('meta', 0),
            headings_score=category_scores.get('headings', 0),
            technical_seo_score=category_scores.get('technical', 0),
            
            checks_passed=len(self.issues["passed"]),
            checks_failed=len(self.issues["critical"]),
            checks_warnings=len(self.issues["warnings"])
        )
        
        print(f"\n✅ Audit complete! Score: {score}/100 (Grade: {grade})")
        print(f"   Critical Issues: {len(self.issues['critical'])}")
        print(f"   Warnings: {len(self.issues['warnings'])}")
        print(f"   Passed Checks: {len(self.issues['passed'])}")
        
        return result


SEOAuditor = AdvancedSEOAuditor


def print_audit_report(result: SEOAuditResult):
    if result.score >= 80:
        score_indicator = "🟢"
    elif result.score >= 60:
        score_indicator = "🟡"
    else:
        score_indicator = "🔴"
    
    report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ADVANCED SEO AUDIT REPORT (200+ Parameters)               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  URL: {result.url[:65]:<65} ║
║  Date: {result.audit_date:<64} ║
║  Score: {score_indicator} {result.score}/100 (Grade: {result.grade}){' ' * 50} ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 SUMMARY: ✅ Passed: {result.checks_passed} | ⚠️ Warnings: {result.checks_warnings} | ❌ Critical: {result.checks_failed}
   Response: {result.response_time:.2f}s | Size: {result.page_size_kb}KB

📋 META: Title {result.title_status} ({result.title_length}ch) | Desc {result.meta_description_status} ({result.meta_description_length}ch)
🌐 SOCIAL: OG {result.og_score}% | Twitter {result.twitter_score}%
📝 HEADINGS: H1:{result.h1_count} H2:{result.h2_count} H3:{result.h3_count} | {result.heading_structure_status}
🖼️ IMAGES: {result.total_images} total | {result.images_without_alt} missing alt | Lazy:{result.images_with_lazy_loading}
🔗 LINKS: Internal:{result.internal_links} External:{result.external_links} | Score:{result.links_score}
⚙️ TECH: SSL:{'✅' if result.has_ssl else '❌'} Viewport:{'✅' if result.has_viewport else '❌'} Schema:{'✅' if result.has_schema_markup else '❌'}
📖 CONTENT: {result.word_count} words | Readability: {result.readability_status}
📱 MOBILE: {'✅' if result.is_mobile_friendly else '❌'} | AMP:{'✅' if result.has_amp_version else '❌'}
♿ A11Y: Score {result.accessibility_score}/100 | ⚡ PERF: Score {result.performance_hints_score}/100
"""
    
    if result.critical_issues:
        report += "\n🚨 CRITICAL ISSUES:\n"
        for issue in result.critical_issues[:10]:
            report += f"   ❌ {issue}\n"
    
    if result.warnings:
        report += "\n⚠️ WARNINGS:\n"
        for warning in result.warnings[:10]:
            report += f"   ⚠️ {warning}\n"
    
    if result.recommendations:
        report += "\n💡 RECOMMENDATIONS:\n"
        for rec in result.recommendations[:10]:
            report += f"   💡 {rec}\n"
    
    print(report)
    return report


def save_report_json(result: SEOAuditResult, filename: str = None):
    if filename is None:
        domain = urlparse(result.url).netloc.replace('.', '_')
        filename = f"audit_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(asdict(result), f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n📁 JSON Report saved to: {filename}")
    return filename


def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║          🔍 ADVANCED SEO AUDIT TOOL v2.0 - By Muntasir Islam              ║
    ║                    Enterprise-Grade 200+ Parameter Analysis               ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    url = input("Enter website URL to audit: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    keyword = input("Enter target keyword (optional, press Enter to skip): ").strip()
    
    auditor = AdvancedSEOAuditor(url, target_keyword=keyword if keyword else None)
    result = auditor.run_audit()
    
    if result:
        print_audit_report(result)
        
        save = input("\nSave report as JSON? (y/n): ").strip().lower()
        if save == 'y':
            save_report_json(result)
    else:
        print("❌ Failed to complete audit. Please check the URL and try again.")


if __name__ == "__main__":
    main()
