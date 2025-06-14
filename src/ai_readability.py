"""
AI Readability Analysis: SEO Structure Metrics
"""
from typing import Dict, List
import re
import html5lib
from html5lib.html5parser import ParseError

class AIReadabilityAnalyzer:
    def __init__(self):
        self.title_ideal_min = 50
        self.title_ideal_max = 60
        self.meta_desc_max = 155
        self.content_word_min = 300
        self.semantic_tags = ["header", "nav", "main", "article", "section", "footer"]

    def analyze_seo_structure(self, seo_analysis: Dict) -> Dict:
        """
        Analyze SEO structure metrics for AI readability.
        Args:
            seo_analysis (dict): Output from SEOAnalyzer
        Returns:
            dict: Metrics, flags, and AI-focused explanations
        """
        meta = seo_analysis.get('meta_tags', {})
        content = seo_analysis.get('content_analysis', {})
        headings = content.get('heading_structure', {})
        
        # Title Tag Length
        title = meta.get('title', {}).get('content', '')
        title_len = len(title)
        title_flag = self.title_ideal_min <= title_len <= self.title_ideal_max
        title_explanation = (
            "Optimal: Title is concise and clear for AI/search display."
            if title_flag else
            f"{'Too short' if title_len < self.title_ideal_min else 'Too long'}: Title may not be optimal for AI/search context."
        )

        # Meta Description Length
        meta_desc = meta.get('meta_description', {}).get('content', '')
        meta_desc_len = len(meta_desc)
        meta_desc_flag = 0 < meta_desc_len <= self.meta_desc_max
        meta_desc_explanation = (
            "Optimal: Meta description is present and concise for AI/search snippets."
            if meta_desc_flag else
            ("Missing: No meta description for AI/search snippet." if meta_desc_len == 0 else "Too long: May be truncated in AI/search results.")
        )

        # H1 Tag Presence
        h1_count = headings.get('h1', 0)
        h1_flag = h1_count == 1
        h1_explanation = (
            "Optimal: Single H1 tag provides clear main topic for AI parsing."
            if h1_flag else
            ("Missing: No H1 tag for main topic." if h1_count == 0 else "Multiple H1 tags: Ambiguous main topic for AI.")
        )

        # Content Word Count
        main_content = content.get('main_content', '')
        word_count = len(main_content.split())
        content_flag = word_count >= self.content_word_min
        content_explanation = (
            "Optimal: Sufficient content for AI to understand and summarize."
            if content_flag else
            "Too little content: May be considered 'thin' by AI/search."
        )

        return {
            'title_tag_length': {
                'value': title_len,
                'optimal': title_flag,
                'explanation': title_explanation
            },
            'meta_description_length': {
                'value': meta_desc_len,
                'optimal': meta_desc_flag,
                'explanation': meta_desc_explanation
            },
            'h1_tag_presence': {
                'value': h1_count,
                'optimal': h1_flag,
                'explanation': h1_explanation
            },
            'content_word_count': {
                'value': word_count,
                'optimal': content_flag,
                'explanation': content_explanation
            }
        }

    def analyze_semantic_and_structure(self, html: str, seo_analysis: Dict) -> Dict:
        """
        Analyze semantic element usage, HTML validation errors, and heading hierarchy order.
        Args:
            html (str): Raw HTML content
            seo_analysis (dict): Output from SEOAnalyzer
        Returns:
            dict: Metrics, flags, and AI-focused explanations
        """
        # --- Semantic Element Usage ---
        semantic_counts = {tag: len(re.findall(f'<{tag}[^>]*>', html, re.IGNORECASE)) for tag in self.semantic_tags}
        total_semantic = sum(semantic_counts.values())
        total_div_sections = len(re.findall(r'<div[^>]*>', html, re.IGNORECASE))
        total_sections = total_semantic + total_div_sections
        semantic_ratio = total_semantic / total_sections if total_sections > 0 else 0
        semantic_flag = semantic_ratio >= 0.5  # Optimal if at least half are semantic
        semantic_explanation = (
            "Optimal: Semantic HTML5 elements are used for clear structure."
            if semantic_flag else
            "Suboptimal: Consider using more semantic HTML5 elements for better AI understanding."
        )

        # --- HTML Validation Errors ---
        parser = html5lib.HTMLParser(strict=True)
        errors: List[ParseError] = []
        try:
            parser.parse(html)
        except Exception as e:
            # html5lib raises ParseError for each error, but doesn't collect all by default
            # We'll use a regex fallback for common errors
            errors = re.findall(r'<[^>]+$', html, re.MULTILINE)  # Unclosed tags at EOF
        error_count = len(parser.errors) if hasattr(parser, 'errors') and parser.errors else len(errors)
        html_valid_flag = error_count == 0
        html_valid_explanation = (
            "Optimal: No HTML validation errors detected."
            if html_valid_flag else
            f"{error_count} HTML validation error(s) detected. This may confuse AI/bots."
        )

        # --- Heading Hierarchy Order ---
        headings = re.findall(r'<h([1-6])[^>]*>', html, re.IGNORECASE)
        heading_levels = [int(h) for h in headings]
        hierarchy_flag, hierarchy_explanation = self._check_heading_hierarchy(heading_levels)

        return {
            'semantic_element_usage': {
                'semantic_count': total_semantic,
                'total_sections': total_sections,
                'ratio': semantic_ratio,
                'optimal': semantic_flag,
                'explanation': semantic_explanation
            },
            'html_validation_errors': {
                'error_count': error_count,
                'optimal': html_valid_flag,
                'explanation': html_valid_explanation
            },
            'heading_hierarchy_order': {
                'levels': heading_levels,
                'optimal': hierarchy_flag,
                'explanation': hierarchy_explanation
            }
        }

    def _check_heading_hierarchy(self, levels: List[int]) -> (bool, str):
        """Check for logical heading order (no skips)."""
        if not levels:
            return False, "No headings found."
        prev = levels[0]
        for curr in levels[1:]:
            if curr > prev + 1:
                return False, f"Heading level skipped: h{prev} to h{curr}."
            prev = curr
        return True, "Optimal: Heading hierarchy is logical and accessible." 