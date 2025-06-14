"""
SEO Analysis module for extracting and analyzing SEO-related metrics from websites.
"""
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from collections import Counter
import re
from urllib.parse import urljoin, urlparse

class SEOAnalyzer:
    def __init__(self):
        self.important_tags = ['title', 'meta', 'h1', 'h2', 'h3', 'img', 'a']
        self.stop_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 
                          'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at'}

    def analyze(self, html: str, base_url: str) -> Dict:
        """
        Perform comprehensive SEO analysis on the HTML content.
        
        Args:
            html (str): Raw HTML content
            base_url (str): Base URL of the page for resolving relative links
            
        Returns:
            Dict: Complete SEO analysis results
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        return {
            'meta_tags': self._analyze_meta_tags(soup),
            'keyword_analysis': self._analyze_keywords(soup),
            'content_analysis': self._analyze_content(soup),
            'link_analysis': self._analyze_links(soup, base_url),
            'image_analysis': self._analyze_images(soup),
            'technical_seo': self._analyze_technical_seo(soup),
            'url_structure': self._analyze_url_structure(base_url)
        }

    def _analyze_meta_tags(self, soup: BeautifulSoup) -> Dict:
        """Analyze meta tags including OpenGraph and Twitter cards."""
        meta_tags = {
            'title': self._get_title_info(soup),
            'meta_description': self._get_meta_description(soup),
            'robots': self._get_meta_content(soup, 'robots'),
            'viewport': self._get_meta_content(soup, 'viewport'),
            'charset': self._get_charset(soup),
            'canonical': self._get_canonical_url(soup),
            'og_tags': self._get_opengraph_tags(soup),
            'twitter_cards': self._get_twitter_cards(soup)
        }
        return meta_tags

    def _analyze_keywords(self, soup: BeautifulSoup) -> Dict:
        """Analyze keyword usage and density."""
        text = soup.get_text()
        words = re.findall(r'\w+', text.lower())
        words = [w for w in words if w not in self.stop_words and len(w) > 2]
        
        # Calculate keyword frequency
        word_freq = Counter(words)
        total_words = len(words)
        
        # Get top keywords with density
        top_keywords = {
            word: {
                'count': count,
                'density': (count / total_words) * 100 if total_words > 0 else 0
            }
            for word, count in word_freq.most_common(10)
        }
        
        return {
            'top_keywords': top_keywords,
            'total_words': total_words,
            'unique_words': len(word_freq)
        }

    def _analyze_content(self, soup: BeautifulSoup) -> Dict:
        """Analyze content structure and readability."""
        paragraphs = soup.find_all('p')
        headings = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
        
        return {
            'paragraph_count': len(paragraphs),
            'heading_structure': headings,
            'avg_paragraph_length': self._calculate_avg_length(paragraphs),
            'content_length': len(soup.get_text()),
            'text_html_ratio': self._calculate_text_html_ratio(soup)
        }

    def _analyze_links(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """Analyze internal and external links."""
        links = soup.find_all('a', href=True)
        internal_links = []
        external_links = []
        
        base_domain = urlparse(base_url).netloc
        
        for link in links:
            href = link.get('href')
            absolute_url = urljoin(base_url, href)
            parsed_url = urlparse(absolute_url)
            
            link_info = {
                'url': absolute_url,
                'text': link.get_text().strip(),
                'title': link.get('title', ''),
                'nofollow': 'nofollow' in link.get('rel', [])
            }
            
            if parsed_url.netloc == base_domain:
                internal_links.append(link_info)
            else:
                external_links.append(link_info)
        
        return {
            'internal_links': {
                'count': len(internal_links),
                'links': internal_links
            },
            'external_links': {
                'count': len(external_links),
                'links': external_links
            }
        }

    def _analyze_images(self, soup: BeautifulSoup) -> Dict:
        """Analyze image optimization."""
        images = soup.find_all('img')
        image_analysis = []
        
        for img in images:
            image_analysis.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', ''),
                'has_alt': bool(img.get('alt')),
                'has_dimensions': bool(img.get('width')) and bool(img.get('height'))
            })
        
        return {
            'total_images': len(images),
            'images_with_alt': sum(1 for img in image_analysis if img['has_alt']),
            'images_with_dimensions': sum(1 for img in image_analysis if img['has_dimensions']),
            'image_details': image_analysis
        }

    def _analyze_technical_seo(self, soup: BeautifulSoup) -> Dict:
        """Analyze technical SEO elements."""
        return {
            'has_viewport': bool(soup.find('meta', attrs={'name': 'viewport'})),
            'has_favicon': bool(soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')),
            'has_structured_data': bool(soup.find('script', type='application/ld+json')),
            'has_xml_sitemap': bool(soup.find('link', rel='sitemap')),
            'has_robots_txt': bool(soup.find('meta', attrs={'name': 'robots'})),
            'has_analytics': bool(soup.find('script', string=re.compile(r'gtag|ga|analytics')))
        }

    def _analyze_url_structure(self, url: str) -> Dict:
        """Analyze URL structure and components."""
        parsed = urlparse(url)
        path_segments = [seg for seg in parsed.path.split('/') if seg]
        
        return {
            'protocol': parsed.scheme,
            'domain': parsed.netloc,
            'path_depth': len(path_segments),
            'path_segments': path_segments,
            'has_query_params': bool(parsed.query),
            'has_fragment': bool(parsed.fragment),
            'is_clean_url': not bool(parsed.query) and not bool(parsed.fragment)
        }

    def _get_title_info(self, soup: BeautifulSoup) -> Dict:
        """Get detailed title tag information."""
        title_tag = soup.find('title')
        if not title_tag:
            return {'found': False, 'content': '', 'length': 0}
        
        content = title_tag.string or ''
        return {
            'found': True,
            'content': content.strip(),
            'length': len(content.strip())
        }

    def _get_meta_description(self, soup: BeautifulSoup) -> Dict:
        """Get meta description information."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            return {'found': False, 'content': '', 'length': 0}
        
        content = meta_desc.get('content', '')
        return {
            'found': True,
            'content': content,
            'length': len(content)
        }

    def _get_meta_content(self, soup: BeautifulSoup, name: str) -> str:
        """Get content of a specific meta tag."""
        meta_tag = soup.find('meta', attrs={'name': name})
        return meta_tag.get('content', '') if meta_tag else ''

    def _get_charset(self, soup: BeautifulSoup) -> str:
        """Get document charset."""
        # Check meta charset
        meta_charset = soup.find('meta', charset=True)
        if meta_charset:
            return meta_charset.get('charset', '')
        
        # Check content-type meta
        meta_content_type = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        if meta_content_type:
            content = meta_content_type.get('content', '')
            match = re.search(r'charset=([^\s]*)', content)
            if match:
                return match.group(1)
        
        return ''

    def _get_canonical_url(self, soup: BeautifulSoup) -> str:
        """Get canonical URL."""
        canonical = soup.find('link', rel='canonical')
        return canonical.get('href', '') if canonical else ''

    def _get_opengraph_tags(self, soup: BeautifulSoup) -> Dict:
        """Get OpenGraph meta tags."""
        og_tags = {}
        for tag in soup.find_all('meta', property=re.compile(r'^og:')):
            og_tags[tag.get('property')] = tag.get('content', '')
        return og_tags

    def _get_twitter_cards(self, soup: BeautifulSoup) -> Dict:
        """Get Twitter Card meta tags."""
        twitter_tags = {}
        for tag in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')}):
            twitter_tags[tag.get('name')] = tag.get('content', '')
        return twitter_tags

    def _calculate_avg_length(self, elements) -> float:
        """Calculate average length of text in elements."""
        if not elements:
            return 0
        total_length = sum(len(elem.get_text().strip()) for elem in elements)
        return total_length / len(elements)

    def _calculate_text_html_ratio(self, soup: BeautifulSoup) -> float:
        """Calculate text to HTML ratio."""
        text_length = len(soup.get_text())
        html_length = len(str(soup))
        return (text_length / html_length) * 100 if html_length > 0 else 0 