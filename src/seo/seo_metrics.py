"""
Advanced SEO metrics computation and scoring module.
"""
from typing import Dict, List, Tuple
import re
from collections import Counter

class SEOMetrics:
    def __init__(self):
        # Optimal ranges for various metrics
        self.optimal_ranges = {
            'title_length': (50, 60),
            'meta_description_length': (120, 160),
            'content_length': (300, 2500),
            'text_html_ratio': (20, 70),
            'keyword_density': (1, 3),
            'heading_count': {
                'h1': (1, 1),
                'h2': (2, 5),
                'h3': (3, 8)
            },
            'internal_links': (5, 20),
            'external_links': (2, 10),
            'images_with_alt': (80, 100),  # percentage
            'paragraph_length': (50, 150)
        }

    def compute_metrics(self, seo_analysis: Dict) -> Dict:
        """
        Compute advanced SEO metrics from the analysis results.
        
        Args:
            seo_analysis (Dict): Results from SEOAnalyzer
            
        Returns:
            Dict: Advanced metrics and scores
        """
        return {
            'content_quality': self._analyze_content_quality(seo_analysis),
            'technical_score': self._compute_technical_score(seo_analysis),
            'keyword_optimization': self._analyze_keyword_optimization(seo_analysis),
            'link_quality': self._analyze_link_quality(seo_analysis),
            'image_optimization': self._analyze_image_optimization(seo_analysis),
            'readability': self._analyze_readability(seo_analysis),
            'recommendations': self._generate_recommendations(seo_analysis),
            'overall_score': self._compute_overall_score(seo_analysis)
        }

    def _analyze_content_quality(self, seo_analysis: Dict) -> Dict:
        """Analyze content quality metrics."""
        content = seo_analysis['content_analysis']
        meta = seo_analysis['meta_tags']
        
        # Calculate content length score
        content_length = content['content_length']
        content_length_score = self._calculate_range_score(
            content_length,
            self.optimal_ranges['content_length']
        )
        
        # Calculate text/HTML ratio score
        text_ratio = content['text_html_ratio']
        text_ratio_score = self._calculate_range_score(
            text_ratio,
            self.optimal_ranges['text_html_ratio']
        )
        
        # Analyze heading structure
        heading_scores = {}
        for h_level, count in content['heading_structure'].items():
            if h_level in self.optimal_ranges['heading_count']:
                heading_scores[h_level] = self._calculate_range_score(
                    count,
                    self.optimal_ranges['heading_count'][h_level]
                )
        
        return {
            'content_length': {
                'value': content_length,
                'score': content_length_score,
                'optimal_range': self.optimal_ranges['content_length']
            },
            'text_html_ratio': {
                'value': text_ratio,
                'score': text_ratio_score,
                'optimal_range': self.optimal_ranges['text_html_ratio']
            },
            'heading_structure': heading_scores,
            'paragraph_count': content['paragraph_count'],
            'avg_paragraph_length': content['avg_paragraph_length']
        }

    def _compute_technical_score(self, seo_analysis: Dict) -> Dict:
        """Compute technical SEO score."""
        technical = seo_analysis['technical_seo']
        meta = seo_analysis['meta_tags']
        
        # Calculate title score
        title_length = meta['title']['length']
        title_score = self._calculate_range_score(
            title_length,
            self.optimal_ranges['title_length']
        )
        
        # Calculate meta description score
        meta_desc_length = meta['meta_description']['length']
        meta_desc_score = self._calculate_range_score(
            meta_desc_length,
            self.optimal_ranges['meta_description_length']
        )
        
        # Technical elements score
        technical_elements = {
            'viewport': technical['has_viewport'],
            'favicon': technical['has_favicon'],
            'structured_data': technical['has_structured_data'],
            'analytics': technical['has_analytics'],
            'robots_txt': technical['has_robots_txt']
        }
        
        return {
            'title': {
                'length': title_length,
                'score': title_score,
                'optimal_range': self.optimal_ranges['title_length']
            },
            'meta_description': {
                'length': meta_desc_length,
                'score': meta_desc_score,
                'optimal_range': self.optimal_ranges['meta_description_length']
            },
            'technical_elements': technical_elements,
            'technical_score': sum(technical_elements.values()) / len(technical_elements) * 100
        }

    def _analyze_keyword_optimization(self, seo_analysis: Dict) -> Dict:
        """Analyze keyword optimization metrics."""
        keywords = seo_analysis['keyword_analysis']
        meta = seo_analysis['meta_tags']
        
        # Extract keywords from title and meta description
        title_words = set(re.findall(r'\w+', meta['title']['content'].lower()))
        meta_desc_words = set(re.findall(r'\w+', meta['meta_description']['content'].lower()))
        
        # Find keywords in title and meta description
        keyword_usage = {}
        for keyword, data in keywords['top_keywords'].items():
            keyword_usage[keyword] = {
                'density': data['density'],
                'in_title': keyword in title_words,
                'in_meta_description': keyword in meta_desc_words,
                'score': self._calculate_range_score(
                    data['density'],
                    self.optimal_ranges['keyword_density']
                )
            }
        
        return {
            'keyword_usage': keyword_usage,
            'total_keywords': len(keywords['top_keywords']),
            'keywords_in_title': len(title_words),
            'keywords_in_meta': len(meta_desc_words)
        }

    def _analyze_link_quality(self, seo_analysis: Dict) -> Dict:
        """Analyze link quality metrics."""
        links = seo_analysis['link_analysis']
        
        # Calculate internal links score
        internal_count = links['internal_links']['count']
        internal_score = self._calculate_range_score(
            internal_count,
            self.optimal_ranges['internal_links']
        )
        
        # Calculate external links score
        external_count = links['external_links']['count']
        external_score = self._calculate_range_score(
            external_count,
            self.optimal_ranges['external_links']
        )
        
        # Analyze link text
        internal_texts = [link['text'] for link in links['internal_links']['links']]
        external_texts = [link['text'] for link in links['external_links']['links']]
        
        return {
            'internal_links': {
                'count': internal_count,
                'score': internal_score,
                'optimal_range': self.optimal_ranges['internal_links']
            },
            'external_links': {
                'count': external_count,
                'score': external_score,
                'optimal_range': self.optimal_ranges['external_links']
            },
            'link_text_analysis': {
                'internal_texts': internal_texts,
                'external_texts': external_texts
            }
        }

    def _analyze_image_optimization(self, seo_analysis: Dict) -> Dict:
        """Analyze image optimization metrics."""
        images = seo_analysis['image_analysis']
        
        # Calculate alt text score
        alt_text_percentage = (images['images_with_alt'] / images['total_images'] * 100) if images['total_images'] > 0 else 0
        alt_text_score = self._calculate_range_score(
            alt_text_percentage,
            self.optimal_ranges['images_with_alt']
        )
        
        return {
            'alt_text': {
                'percentage': alt_text_percentage,
                'score': alt_text_score,
                'optimal_range': self.optimal_ranges['images_with_alt']
            },
            'dimensions': {
                'with_dimensions': images['images_with_dimensions'],
                'total': images['total_images']
            }
        }

    def _analyze_readability(self, seo_analysis: Dict) -> Dict:
        """Analyze content readability metrics."""
        content = seo_analysis['content_analysis']
        
        # Calculate paragraph length score
        avg_paragraph_length = content['avg_paragraph_length']
        paragraph_score = self._calculate_range_score(
            avg_paragraph_length,
            self.optimal_ranges['paragraph_length']
        )
        
        return {
            'paragraph_length': {
                'average': avg_paragraph_length,
                'score': paragraph_score,
                'optimal_range': self.optimal_ranges['paragraph_length']
            }
        }

    def _generate_recommendations(self, seo_analysis: Dict) -> List[Dict]:
        """Generate SEO recommendations based on analysis."""
        recommendations = []
        
        # Check title
        title_length = seo_analysis['meta_tags']['title']['length']
        if not self.optimal_ranges['title_length'][0] <= title_length <= self.optimal_ranges['title_length'][1]:
            recommendations.append({
                'type': 'title',
                'priority': 'high',
                'message': f"Title length ({title_length} chars) should be between {self.optimal_ranges['title_length'][0]} and {self.optimal_ranges['title_length'][1]} characters"
            })
        
        # Check meta description
        meta_desc_length = seo_analysis['meta_tags']['meta_description']['length']
        if not self.optimal_ranges['meta_description_length'][0] <= meta_desc_length <= self.optimal_ranges['meta_description_length'][1]:
            recommendations.append({
                'type': 'meta_description',
                'priority': 'high',
                'message': f"Meta description length ({meta_desc_length} chars) should be between {self.optimal_ranges['meta_description_length'][0]} and {self.optimal_ranges['meta_description_length'][1]} characters"
            })
        
        # Check images
        images = seo_analysis['image_analysis']
        if images['total_images'] > 0:
            alt_text_percentage = (images['images_with_alt'] / images['total_images'] * 100)
            if alt_text_percentage < self.optimal_ranges['images_with_alt'][0]:
                recommendations.append({
                    'type': 'images',
                    'priority': 'medium',
                    'message': f"Only {alt_text_percentage:.1f}% of images have alt text. Aim for at least {self.optimal_ranges['images_with_alt'][0]}%"
                })
        
        # Check technical elements
        technical = seo_analysis['technical_seo']
        if not technical['has_viewport']:
            recommendations.append({
                'type': 'technical',
                'priority': 'high',
                'message': "Add viewport meta tag for mobile optimization"
            })
        if not technical['has_structured_data']:
            recommendations.append({
                'type': 'technical',
                'priority': 'medium',
                'message': "Consider adding structured data for better search results"
            })
        
        return recommendations

    def _compute_overall_score(self, seo_analysis: Dict) -> float:
        """Compute overall SEO score."""
        metrics = self.compute_metrics(seo_analysis)
        
        # Weight different components
        weights = {
            'content_quality': 0.3,
            'technical_score': 0.25,
            'keyword_optimization': 0.2,
            'link_quality': 0.15,
            'image_optimization': 0.1
        }
        
        # Calculate weighted average
        score = (
            metrics['content_quality']['text_html_ratio']['score'] * weights['content_quality'] +
            metrics['technical_score']['technical_score'] * weights['technical_score'] +
            sum(k['score'] for k in metrics['keyword_optimization']['keyword_usage'].values()) / len(metrics['keyword_optimization']['keyword_usage']) * weights['keyword_optimization'] +
            (metrics['link_quality']['internal_links']['score'] + metrics['link_quality']['external_links']['score']) / 2 * weights['link_quality'] +
            metrics['image_optimization']['alt_text']['score'] * weights['image_optimization']
        )
        
        return round(score, 2)

    def _calculate_range_score(self, value: float, optimal_range: Tuple[float, float]) -> float:
        """Calculate score based on optimal range."""
        min_val, max_val = optimal_range
        if min_val <= value <= max_val:
            return 100
        elif value < min_val:
            return (value / min_val) * 100
        else:
            return max(0, 100 - ((value - max_val) / max_val) * 100) 