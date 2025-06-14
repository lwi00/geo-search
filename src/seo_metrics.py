"""
Advanced SEO metrics computation module.
"""
import re
from typing import Dict, List, Tuple
from collections import Counter
import math

class SEOMetrics:
    def __init__(self):
        """Initialize SEO metrics calculator."""
        # Common English stop words
        self.stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what'
        }
        
        # Ideal ranges for various metrics
        self.ideal_ranges = {
            'title_length': (30, 60),
            'meta_description_length': (120, 160),
            'content_length': (300, 2500),
            'keyword_density': (0.5, 3.0),
            'text_html_ratio': (15, 70),
            'heading_density': (0.1, 0.3),
            'link_density': (0.1, 0.3),
            'image_density': (0.1, 0.3)
        }

    def compute_metrics(self, seo_analysis: Dict) -> Dict:
        """
        Compute advanced SEO metrics from the analysis results.
        
        Args:
            seo_analysis (Dict): Results from SEOAnalyzer
            
        Returns:
            Dict: Advanced SEO metrics
        """
        try:
            return {
                'content_quality': self._compute_content_quality(seo_analysis),
                'technical_score': self._compute_technical_score(seo_analysis),
                'readability': self._compute_readability(seo_analysis),
                'keyword_optimization': self._compute_keyword_optimization(seo_analysis),
                'link_quality': self._compute_link_quality(seo_analysis),
                'image_optimization': self._compute_image_optimization(seo_analysis),
                'overall_score': self._compute_overall_score(seo_analysis)
            }
        except Exception as e:
            print(f"Warning: Error computing metrics: {str(e)}")
            return self._get_default_metrics()

    def _get_default_metrics(self) -> Dict:
        """Return default metrics when computation fails."""
        return {
            'content_quality': {
                'content_length_score': 0.0,
                'heading_structure_score': 0.0,
                'paragraph_structure_score': 0.0,
                'text_html_ratio_score': 0.0,
                'overall_content_score': 0.0
            },
            'technical_score': {
                'meta_tags_score': 0.0,
                'technical_elements_score': 0.0,
                'overall_technical_score': 0.0
            },
            'readability': {
                'flesch_reading_ease': 0.0,
                'avg_sentence_length': 0.0,
                'avg_word_length': 0.0,
                'readability_level': 'Unknown'
            },
            'keyword_optimization': {
                'keyword_density_scores': {},
                'keywords_in_title': [],
                'keywords_in_meta': [],
                'keyword_optimization_score': 0.0
            },
            'link_quality': {
                'internal_external_ratio': 0.0,
                'internal_link_text_score': 0.0,
                'external_link_text_score': 0.0,
                'overall_link_quality_score': 0.0
            },
            'image_optimization': {
                'alt_text_score': 0.0,
                'dimensions_score': 0.0,
                'overall_image_score': 0.0
            },
            'overall_score': {
                'overall_score': 0.0,
                'score_breakdown': {
                    'content_quality': 0.0,
                    'technical_score': 0.0,
                    'keyword_score': 0.0,
                    'link_score': 0.0,
                    'image_score': 0.0
                }
            }
        }

    def _compute_content_quality(self, analysis: Dict) -> Dict:
        """Compute content quality metrics."""
        try:
            content = analysis['content_analysis']
            meta = analysis['meta_tags']
            
            # Calculate content length score
            content_length = content.get('content_length', 0)
            content_length_score = self._normalize_score(
                content_length,
                self.ideal_ranges['content_length'][0],
                self.ideal_ranges['content_length'][1]
            )
            
            # Calculate heading structure score
            headings = content.get('heading_structure', {})
            heading_score = self._calculate_heading_score(headings)
            
            # Calculate paragraph structure score
            paragraph_score = self._calculate_paragraph_score(content)
            
            return {
                'content_length_score': content_length_score,
                'heading_structure_score': heading_score,
                'paragraph_structure_score': paragraph_score,
                'text_html_ratio_score': self._normalize_score(
                    content.get('text_html_ratio', 0),
                    self.ideal_ranges['text_html_ratio'][0],
                    self.ideal_ranges['text_html_ratio'][1]
                ),
                'overall_content_score': (content_length_score + heading_score + paragraph_score) / 3
            }
        except Exception as e:
            print(f"Warning: Error computing content quality: {str(e)}")
            return self._get_default_metrics()['content_quality']

    def _compute_technical_score(self, analysis: Dict) -> Dict:
        """Compute technical SEO score."""
        try:
            technical = analysis['technical_seo']
            meta = analysis['meta_tags']
            
            # Calculate meta tags score
            meta_score = self._calculate_meta_score(meta)
            
            # Calculate technical elements score
            technical_elements = {
                'viewport': technical['has_viewport'],
                'favicon': technical['has_favicon'],
                'structured_data': technical['has_structured_data'],
                'analytics': technical['has_analytics'],
                'robots_txt': technical['has_robots_txt']
            }
            
            technical_score = sum(technical_elements.values()) / len(technical_elements)
            
            return {
                'meta_tags_score': meta_score,
                'technical_elements_score': technical_score,
                'overall_technical_score': (meta_score + technical_score) / 2
            }
        except Exception as e:
            print(f"Warning: Error computing technical score: {str(e)}")
            return self._get_default_metrics()['technical_score']

    def _compute_readability(self, analysis: Dict) -> Dict:
        """Compute readability metrics."""
        try:
            content = analysis['content_analysis']
            text = content.get('main_content', '')
            
            # Calculate basic readability metrics
            sentences = len(re.split(r'[.!?]+', text))
            words = len(text.split())
            syllables = self._count_syllables(text)
            
            # Calculate Flesch Reading Ease score
            if sentences > 0 and words > 0:
                flesch_score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
            else:
                flesch_score = 0
            
            # Calculate average sentence length
            avg_sentence_length = words / sentences if sentences > 0 else 0
            
            return {
                'flesch_reading_ease': flesch_score,
                'avg_sentence_length': avg_sentence_length,
                'avg_word_length': sum(len(word) for word in text.split()) / words if words > 0 else 0,
                'readability_level': self._get_readability_level(flesch_score)
            }
        except Exception as e:
            print(f"Warning: Error computing readability: {str(e)}")
            return self._get_default_metrics()['readability']

    def _compute_keyword_optimization(self, analysis: Dict) -> Dict:
        """Compute keyword optimization metrics."""
        try:
            keywords = analysis['keyword_analysis']
            meta = analysis['meta_tags']
            
            # Calculate keyword density scores
            density_scores = {}
            for word, data in keywords.get('top_keywords', {}).items():
                density_scores[word] = self._normalize_score(
                    data['density'],
                    self.ideal_ranges['keyword_density'][0],
                    self.ideal_ranges['keyword_density'][1]
                )
            
            # Calculate keyword presence in title and meta description
            title_keywords = self._get_keywords_in_text(meta.get('title', {}).get('content', ''))
            meta_keywords = self._get_keywords_in_text(meta.get('meta_description', {}).get('content', ''))
            
            return {
                'keyword_density_scores': density_scores,
                'keywords_in_title': title_keywords,
                'keywords_in_meta': meta_keywords,
                'keyword_optimization_score': sum(density_scores.values()) / len(density_scores) if density_scores else 0
            }
        except Exception as e:
            print(f"Warning: Error computing keyword optimization: {str(e)}")
            return self._get_default_metrics()['keyword_optimization']

    def _compute_link_quality(self, analysis: Dict) -> Dict:
        """Compute link quality metrics."""
        try:
            links = analysis['link_analysis']
            
            # Calculate internal/external link ratio
            total_links = links['internal_links']['count'] + links['external_links']['count']
            internal_ratio = links['internal_links']['count'] / total_links if total_links > 0 else 0
            
            # Calculate link text quality
            internal_links = links['internal_links']['links']
            external_links = links['external_links']['links']
            
            internal_text_score = self._calculate_link_text_score(internal_links)
            external_text_score = self._calculate_link_text_score(external_links)
            
            return {
                'internal_external_ratio': internal_ratio,
                'internal_link_text_score': internal_text_score,
                'external_link_text_score': external_text_score,
                'overall_link_quality_score': (internal_text_score + external_text_score) / 2
            }
        except Exception as e:
            print(f"Warning: Error computing link quality: {str(e)}")
            return self._get_default_metrics()['link_quality']

    def _compute_image_optimization(self, analysis: Dict) -> Dict:
        """Compute image optimization metrics."""
        try:
            images = analysis['image_analysis']
            
            # Calculate image optimization scores
            total_images = images.get('total_images', 0)
            if total_images > 0:
                alt_text_score = images['images_with_alt'] / total_images
                dimensions_score = images['images_with_dimensions'] / total_images
            else:
                alt_text_score = 0
                dimensions_score = 0
            
            return {
                'alt_text_score': alt_text_score,
                'dimensions_score': dimensions_score,
                'overall_image_score': (alt_text_score + dimensions_score) / 2
            }
        except Exception as e:
            print(f"Warning: Error computing image optimization: {str(e)}")
            return self._get_default_metrics()['image_optimization']

    def _compute_overall_score(self, analysis: Dict) -> Dict:
        """Compute overall SEO score."""
        try:
            content_quality = self._compute_content_quality(analysis)['overall_content_score']
            technical_score = self._compute_technical_score(analysis)['overall_technical_score']
            keyword_score = self._compute_keyword_optimization(analysis)['keyword_optimization_score']
            link_score = self._compute_link_quality(analysis)['overall_link_quality_score']
            image_score = self._compute_image_optimization(analysis)['overall_image_score']
            
            # Weighted average of all scores
            weights = {
                'content': 0.3,
                'technical': 0.2,
                'keyword': 0.2,
                'link': 0.15,
                'image': 0.15
            }
            
            overall_score = (
                content_quality * weights['content'] +
                technical_score * weights['technical'] +
                keyword_score * weights['keyword'] +
                link_score * weights['link'] +
                image_score * weights['image']
            )
            
            return {
                'overall_score': overall_score,
                'score_breakdown': {
                    'content_quality': content_quality,
                    'technical_score': technical_score,
                    'keyword_score': keyword_score,
                    'link_score': link_score,
                    'image_score': image_score
                }
            }
        except Exception as e:
            print(f"Warning: Error computing overall score: {str(e)}")
            return self._get_default_metrics()['overall_score']

    def _normalize_score(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize a value to a 0-1 score based on ideal range."""
        try:
            # Handle edge cases
            if min_val == max_val:
                return 0.0 if value == 0 else 1.0
                
            if value < min_val:
                return value / min_val if min_val != 0 else 0.0
            elif value > max_val:
                return 1 - ((value - max_val) / max_val)
            return 1.0
        except Exception:
            return 0.0

    def _calculate_heading_score(self, headings: Dict) -> float:
        """Calculate heading structure score."""
        try:
            # Check for proper heading hierarchy
            has_h1 = headings.get('h1', 0) > 0
            has_h2 = headings.get('h2', 0) > 0
            
            # Calculate heading density
            total_headings = sum(headings.values())
            heading_density = total_headings / 100 if total_headings > 0 else 0
            
            # Score based on presence and hierarchy
            hierarchy_score = 1.0 if has_h1 and has_h2 else 0.5
            density_score = self._normalize_score(
                heading_density,
                self.ideal_ranges['heading_density'][0],
                self.ideal_ranges['heading_density'][1]
            )
            
            return (hierarchy_score + density_score) / 2
        except Exception:
            return 0.0

    def _calculate_paragraph_score(self, content: Dict) -> float:
        """Calculate paragraph structure score."""
        try:
            paragraph_count = content.get('paragraph_count', 0)
            avg_length = content.get('avg_paragraph_length', 0)
            
            # Score based on paragraph count and average length
            count_score = self._normalize_score(paragraph_count, 3, 10)
            length_score = self._normalize_score(avg_length, 50, 150)
            
            return (count_score + length_score) / 2
        except Exception:
            return 0.0

    def _calculate_meta_score(self, meta: Dict) -> float:
        """Calculate meta tags score."""
        try:
            title = meta.get('title', {})
            description = meta.get('meta_description', {})
            
            # Score title
            title_score = self._normalize_score(
                title.get('length', 0),
                self.ideal_ranges['title_length'][0],
                self.ideal_ranges['title_length'][1]
            ) if title.get('found', False) else 0
            
            # Score description
            desc_score = self._normalize_score(
                description.get('length', 0),
                self.ideal_ranges['meta_description_length'][0],
                self.ideal_ranges['meta_description_length'][1]
            ) if description.get('found', False) else 0
            
            return (title_score + desc_score) / 2
        except Exception:
            return 0.0

    def _count_syllables(self, text: str) -> int:
        """Count syllables in text."""
        try:
            count = 0
            vowels = 'aeiouy'
            text = text.lower()
            
            for word in text.split():
                if word[0] in vowels:
                    count += 1
                for i in range(1, len(word)):
                    if word[i] in vowels and word[i-1] not in vowels:
                        count += 1
                if word.endswith('e'):
                    count -= 1
                if count == 0:
                    count += 1
                    
            return count
        except Exception:
            return 0

    def _get_readability_level(self, flesch_score: float) -> str:
        """Get readability level based on Flesch score."""
        try:
            if flesch_score >= 90:
                return "Very Easy"
            elif flesch_score >= 80:
                return "Easy"
            elif flesch_score >= 70:
                return "Fairly Easy"
            elif flesch_score >= 60:
                return "Standard"
            elif flesch_score >= 50:
                return "Fairly Difficult"
            elif flesch_score >= 30:
                return "Difficult"
            elif flesch_score >= 0:
                return "Very Difficult"
            else:
                return "Unknown"
        except Exception:
            return "Unknown"

    def _get_keywords_in_text(self, text: str) -> List[str]:
        """Extract keywords from text."""
        try:
            words = re.findall(r'\w+', text.lower())
            return [word for word in words if word not in self.stop_words and len(word) > 2]
        except Exception:
            return []

    def _calculate_link_text_score(self, links: List[Dict]) -> float:
        """Calculate link text quality score."""
        try:
            if not links:
                return 0
                
            scores = []
            for link in links:
                text = link.get('text', '')
                # Score based on text length and presence of keywords
                length_score = self._normalize_score(len(text), 3, 10)
                keyword_score = 1.0 if any(word not in self.stop_words for word in text.split()) else 0.5
                scores.append((length_score + keyword_score) / 2)
                
            return sum(scores) / len(scores)
        except Exception:
            return 0.0 