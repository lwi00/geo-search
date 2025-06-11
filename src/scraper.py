"""
Web scraping module for extracting website content.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional

class WebScraper:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch webpage content from given URL.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            Optional[str]: HTML content if successful, None otherwise
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
            
    def extract_content(self, html: str) -> Dict:
        """
        Extract relevant content from HTML.
        
        Args:
            html (str): Raw HTML content
            
        Returns:
            Dict: Extracted content including title, meta description, and main text
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        return {
            'title': self._get_title(soup),
            'meta_description': self._get_meta_description(soup),
            'main_content': self._get_main_content(soup),
            'headers': self._get_headers(soup)
        }
        
    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title_tag = soup.find('title')
        return title_tag.text.strip() if title_tag else ''
        
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '').strip() if meta else ''
        
    def _get_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content text."""
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
            
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    def _get_headers(self, soup: BeautifulSoup) -> Dict[str, list]:
        """Extract all headers (h1-h6) from the page."""
        headers = {}
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            if h_tags:
                headers[f'h{i}'] = [tag.text.strip() for tag in h_tags]
        return headers 