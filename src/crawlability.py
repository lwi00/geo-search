"""
Crawlability analysis module for GeoSearch.
"""
import re
import time
import requests
from typing import Dict, Optional, Tuple, List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class CrawlabilityAnalyzer:
    def __init__(self):
        self.ideal_text_ratio_range = (25, 70)  # percentage
        self.ideal_load_time = 2.0  # seconds
        
        # Define LLM bots and their user agents
        self.llm_bots = {
            'GPTBot': {
                'user_agent': 'GPTBot',
                'purpose': 'Crawls to improve OpenAI models (e.g., ChatGPT)',
                'company': 'OpenAI'
            },
            'ClaudeBot': {
                'user_agent': ['ClaudeBot', 'anthropic-ai'],
                'purpose': 'Crawls for Claude model training',
                'company': 'Anthropic'
            },
            'Google-Extended': {
                'user_agent': 'Google-Extended',
                'purpose': 'Controls use of content in Google\'s AI models (SGE, Gemini)',
                'company': 'Google'
            },
            'CCBot': {
                'user_agent': 'CCBot',
                'purpose': 'Feeds large public datasets (used by many LLMs)',
                'company': 'Common Crawl'
            },
            'PerplexityBot': {
                'user_agent': 'PerplexityBot',
                'purpose': 'Real-time AI search engine crawler',
                'company': 'Perplexity AI'
            },
            'Amazonbot': {
                'user_agent': 'Amazonbot',
                'purpose': 'May power Alexa and Amazon\'s AI training datasets',
                'company': 'Amazon'
            },
            'YouBot': {
                'user_agent': 'YouBot',
                'purpose': 'AI-powered search engine with LLM-like summaries',
                'company': 'You.com'
            },
            'Neevabot': {
                'user_agent': 'Neevabot',
                'purpose': 'Former AI search engine',
                'company': 'NeevaAI'
            },
            'MetaBot': {
                'user_agent': ['facebookexternalhit', 'MetaBot'],
                'purpose': 'Meta\'s AI and social graph crawling',
                'company': 'Meta'
            }
        }

    def analyze_crawlability(self, url: str, html_content: str) -> Dict:
        """
        Analyze crawlability metrics for a given URL and its HTML content.
        
        Args:
            url (str): The URL to analyze
            html_content (str): The HTML content of the page
            
        Returns:
            dict: Crawlability analysis results
        """
        # Get base URL for sitemap and robots.txt checking
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # Analyze indexability
        indexability = self._analyze_indexability(html_content)
        
        # Check sitemap inclusion
        sitemap_status = self._check_sitemap_inclusion(url, base_url)
        
        # Calculate text-to-HTML ratio
        text_ratio = self._calculate_text_ratio(html_content)
        
        # Measure page load time
        load_time = self._measure_load_time(url)
        
        # Analyze robots.txt for LLM bot directives
        llm_bot_analysis = self._analyze_llm_bot_directives(base_url)
        
        return {
            "indexability": indexability,
            "sitemap_status": sitemap_status,
            "text_ratio": text_ratio,
            "load_time": load_time,
            "llm_bot_analysis": llm_bot_analysis,
            "overall_score": self._compute_overall_score(
                indexability, sitemap_status, text_ratio, load_time, llm_bot_analysis
            )
        }

    def _analyze_indexability(self, html_content: str) -> Dict:
        """
        Analyze if the page is indexable by checking robots meta tags and headers.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check meta robots tag
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        noindex = False
        nofollow = False
        
        if robots_meta and robots_meta.get('content'):
            content = robots_meta['content'].lower()
            noindex = 'noindex' in content
            nofollow = 'nofollow' in content
        
        # Check X-Robots-Tag header (would need to be passed in from main)
        # For now, we'll assume it's not present
        
        return {
            "is_indexable": not noindex,
            "is_followable": not nofollow,
            "meta_robots_present": bool(robots_meta),
            "meta_robots_content": robots_meta.get('content') if robots_meta else None,
            "explanation": self._get_indexability_explanation(noindex, nofollow)
        }

    def _check_sitemap_inclusion(self, url: str, base_url: str) -> Dict:
        """
        Check if the URL is included in the sitemap.
        """
        sitemap_url = urljoin(base_url, '/sitemap.xml')
        
        try:
            response = requests.get(sitemap_url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                urls = soup.find_all('loc')
                url_in_sitemap = any(url in loc.text for loc in urls)
                
                return {
                    "sitemap_exists": True,
                    "url_in_sitemap": url_in_sitemap,
                    "sitemap_url": sitemap_url,
                    "explanation": self._get_sitemap_explanation(url_in_sitemap)
                }
        except requests.RequestException:
            pass
        
        return {
            "sitemap_exists": False,
            "url_in_sitemap": False,
            "sitemap_url": sitemap_url,
            "explanation": "No sitemap.xml found"
        }

    def _calculate_text_ratio(self, html_content: str) -> Dict:
        """
        Calculate the ratio of text content to HTML code.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get text content
        text_content = soup.get_text(separator=' ', strip=True)
        text_bytes = len(text_content.encode('utf-8'))
        
        # Get total HTML size
        html_bytes = len(html_content.encode('utf-8'))
        
        # Calculate ratio
        ratio = (text_bytes / html_bytes) * 100 if html_bytes > 0 else 0
        
        return {
            "ratio": ratio,
            "text_bytes": text_bytes,
            "html_bytes": html_bytes,
            "is_optimal": self.ideal_text_ratio_range[0] <= ratio <= self.ideal_text_ratio_range[1],
            "explanation": self._get_text_ratio_explanation(ratio)
        }

    def _measure_load_time(self, url: str) -> Dict:
        """
        Measure the page load time.
        """
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            load_time = time.time() - start_time
            
            return {
                "load_time": load_time,
                "is_optimal": load_time <= self.ideal_load_time,
                "status_code": response.status_code,
                "explanation": self._get_load_time_explanation(load_time)
            }
        except requests.RequestException as e:
            return {
                "load_time": None,
                "is_optimal": False,
                "error": str(e),
                "explanation": f"Failed to measure load time: {str(e)}"
            }

    def _analyze_llm_bot_directives(self, base_url: str) -> Dict:
        """
        Analyze robots.txt for LLM bot directives.
        
        Args:
            base_url (str): Base URL of the website
            
        Returns:
            dict: Analysis of LLM bot directives
        """
        robots_url = urljoin(base_url, '/robots.txt')
        bot_directives = {}
        robots_content = None
        
        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                robots_content = response.text
                
                # Analyze each LLM bot
                for bot_name, bot_info in self.llm_bots.items():
                    user_agents = bot_info['user_agent'] if isinstance(bot_info['user_agent'], list) else [bot_info['user_agent']]
                    bot_directives[bot_name] = self._analyze_bot_directive(robots_content, user_agents, bot_info)
                
                return {
                    "robots_txt_exists": True,
                    "robots_txt_url": robots_url,
                    "bot_directives": bot_directives,
                    "summary": self._generate_llm_bot_summary(bot_directives)
                }
        except requests.RequestException:
            pass
        
        return {
            "robots_txt_exists": False,
            "robots_txt_url": robots_url,
            "bot_directives": {},
            "summary": "No robots.txt found"
        }

    def _analyze_bot_directive(self, robots_content: str, user_agents: List[str], bot_info: Dict) -> Dict:
        """
        Analyze directives for a specific bot in robots.txt.
        
        Args:
            robots_content (str): Content of robots.txt
            user_agents (List[str]): List of user agents to check
            bot_info (Dict): Bot information dictionary
            
        Returns:
            dict: Analysis of bot directives
        """
        directives = {
            "allowed": True,
            "disallowed_paths": [],
            "crawl_delay": None,
            "user_agents_found": [],
            "directives_found": []
        }
        
        # Check each user agent
        for user_agent in user_agents:
            if user_agent.lower() in robots_content.lower():
                directives["user_agents_found"].append(user_agent)
                
                # Find the section for this user agent
                pattern = rf"(?i)User-agent:\s*{re.escape(user_agent)}.*?(?=User-agent:|$)"
                section = re.search(pattern, robots_content, re.DOTALL)
                
                if section:
                    section_text = section.group(0)
                    directives["directives_found"].append(section_text)
                    
                    # Check for Disallow directives
                    disallows = re.findall(r"Disallow:\s*(.*)", section_text)
                    if disallows:
                        directives["disallowed_paths"].extend(disallows)
                        directives["allowed"] = False
                    
                    # Check for Crawl-delay
                    crawl_delay = re.search(r"Crawl-delay:\s*(\d+)", section_text)
                    if crawl_delay:
                        directives["crawl_delay"] = int(crawl_delay.group(1))
        
        return {
            "bot_name": bot_info['user_agent'][0] if isinstance(bot_info['user_agent'], list) else bot_info['user_agent'],
            "company": bot_info['company'],
            "purpose": bot_info['purpose'],
            "is_allowed": directives["allowed"],
            "disallowed_paths": directives["disallowed_paths"],
            "crawl_delay": directives["crawl_delay"],
            "user_agents_found": directives["user_agents_found"],
            "explanation": self._generate_bot_explanation(directives, bot_info)
        }

    def _generate_bot_explanation(self, directives: Dict, bot_info: Dict) -> str:
        """Generate explanation for bot directives."""
        if not directives["user_agents_found"]:
            return f"No specific directives found for {bot_info['company']} bots"
        
        if not directives["allowed"]:
            paths = ", ".join(directives["disallowed_paths"])
            return f"{bot_info['company']} bots are blocked from: {paths}"
        
        if directives["crawl_delay"]:
            return f"{bot_info['company']} bots are allowed with {directives['crawl_delay']}s crawl delay"
        
        return f"{bot_info['company']} bots are allowed to crawl"

    def _generate_llm_bot_summary(self, bot_directives: Dict) -> str:
        """Generate summary of LLM bot directives."""
        allowed_bots = []
        blocked_bots = []
        
        for bot_name, directive in bot_directives.items():
            if directive["is_allowed"]:
                allowed_bots.append(directive["company"])
            else:
                blocked_bots.append(directive["company"])
        
        summary = []
        if allowed_bots:
            summary.append(f"Allowed: {', '.join(allowed_bots)}")
        if blocked_bots:
            summary.append(f"Blocked: {', '.join(blocked_bots)}")
        
        return " | ".join(summary) if summary else "No LLM bot directives found"

    def _compute_overall_score(self, indexability: Dict, sitemap_status: Dict, 
                             text_ratio: Dict, load_time: Dict, llm_bot_analysis: Dict) -> Dict:
        """
        Compute overall crawlability score.
        """
        # Weight factors for each metric
        weights = {
            "indexability": 0.3,
            "sitemap": 0.2,
            "text_ratio": 0.2,
            "load_time": 0.15,
            "llm_bot": 0.15
        }
        
        # Calculate individual scores
        indexability_score = 1.0 if indexability["is_indexable"] else 0.0
        sitemap_score = 1.0 if sitemap_status["url_in_sitemap"] else 0.5 if sitemap_status["sitemap_exists"] else 0.0
        text_ratio_score = 1.0 if text_ratio["is_optimal"] else 0.5
        load_time_score = 1.0 if load_time.get("is_optimal", False) else 0.0
        
        # Calculate LLM bot score
        llm_bot_score = 0.0
        if llm_bot_analysis["robots_txt_exists"]:
            allowed_bots = sum(1 for bot in llm_bot_analysis["bot_directives"].values() if bot["is_allowed"])
            total_bots = len(llm_bot_analysis["bot_directives"])
            llm_bot_score = allowed_bots / total_bots if total_bots > 0 else 0.5
        
        # Calculate weighted score
        overall_score = (
            indexability_score * weights["indexability"] +
            sitemap_score * weights["sitemap"] +
            text_ratio_score * weights["text_ratio"] +
            load_time_score * weights["load_time"] +
            llm_bot_score * weights["llm_bot"]
        )
        
        return {
            "score": overall_score,
            "components": {
                "indexability": indexability_score,
                "sitemap": sitemap_score,
                "text_ratio": text_ratio_score,
                "load_time": load_time_score,
                "llm_bot": llm_bot_score
            },
            "explanation": self._get_overall_score_explanation(overall_score)
        }

    def _get_indexability_explanation(self, noindex: bool, nofollow: bool) -> str:
        """Generate explanation for indexability status."""
        if noindex:
            return "Page is not indexable (noindex directive present)"
        if nofollow:
            return "Page is indexable but links are not followed (nofollow directive present)"
        return "Page is fully indexable and crawlable"

    def _get_sitemap_explanation(self, url_in_sitemap: bool) -> str:
        """Generate explanation for sitemap status."""
        if url_in_sitemap:
            return "URL is included in sitemap.xml"
        return "URL is not included in sitemap.xml"

    def _get_text_ratio_explanation(self, ratio: float) -> str:
        """Generate explanation for text-to-HTML ratio."""
        if ratio < self.ideal_text_ratio_range[0]:
            return f"Low text-to-HTML ratio ({ratio:.1f}%) - page may have too much code"
        if ratio > self.ideal_text_ratio_range[1]:
            return f"High text-to-HTML ratio ({ratio:.1f}%) - page may have too much text"
        return f"Optimal text-to-HTML ratio ({ratio:.1f}%)"

    def _get_load_time_explanation(self, load_time: float) -> str:
        """Generate explanation for page load time."""
        if load_time <= self.ideal_load_time:
            return f"Fast page load time ({load_time:.2f}s)"
        return f"Slow page load time ({load_time:.2f}s) - may affect crawlability"

    def _get_overall_score_explanation(self, score: float) -> str:
        """Generate explanation for overall crawlability score."""
        if score >= 0.8:
            return "Excellent crawlability"
        if score >= 0.6:
            return "Good crawlability"
        if score >= 0.4:
            return "Fair crawlability"
        return "Poor crawlability" 