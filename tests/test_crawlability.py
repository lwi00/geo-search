"""
Tests for the crawlability analyzer module.
"""
import pytest
from src.crawlability import CrawlabilityAnalyzer

@pytest.fixture
def analyzer():
    return CrawlabilityAnalyzer()

@pytest.fixture
def sample_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="robots" content="index,follow">
        <title>Test Page</title>
    </head>
    <body>
        <h1>Test Page</h1>
        <p>This is a test page with some content.</p>
    </body>
    </html>
    """

@pytest.fixture
def sample_robots_txt():
    return """
User-agent: GPTBot
Disallow: /private/
Crawl-delay: 10

User-agent: ClaudeBot
Allow: /
Crawl-delay: 5

User-agent: Google-Extended
Disallow: /api/
Disallow: /admin/

User-agent: *
Allow: /
    """

def test_analyze_indexability(analyzer, sample_html):
    """Test indexability analysis."""
    result = analyzer._analyze_indexability(sample_html)
    
    assert result["is_indexable"] is True
    assert result["is_followable"] is True
    assert result["meta_robots_present"] is True
    assert "index,follow" in result["meta_robots_content"].lower()

def test_analyze_indexability_noindex(analyzer):
    """Test indexability analysis with noindex directive."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="robots" content="noindex">
    </head>
    <body></body>
    </html>
    """
    result = analyzer._analyze_indexability(html)
    
    assert result["is_indexable"] is False
    assert result["is_followable"] is True
    assert "noindex" in result["meta_robots_content"].lower()

def test_calculate_text_ratio(analyzer, sample_html):
    """Test text-to-HTML ratio calculation."""
    result = analyzer._calculate_text_ratio(sample_html)
    
    assert "ratio" in result
    assert "text_bytes" in result
    assert "html_bytes" in result
    assert "is_optimal" in result
    assert "explanation" in result
    assert isinstance(result["ratio"], float)
    assert isinstance(result["text_bytes"], int)
    assert isinstance(result["html_bytes"], int)

def test_calculate_text_ratio_empty(analyzer):
    """Test text-to-HTML ratio calculation with empty content."""
    result = analyzer._calculate_text_ratio("")
    
    assert result["ratio"] == 0
    assert result["text_bytes"] == 0
    assert result["html_bytes"] == 0
    assert not result["is_optimal"]

def test_analyze_llm_bot_directives(analyzer, sample_robots_txt):
    """Test LLM bot directives analysis."""
    # Mock the robots.txt content
    class MockResponse:
        def __init__(self, content):
            self.content = content
            self.status_code = 200
            self.text = content

    # Test GPTBot directives
    gptbot_directive = analyzer._analyze_bot_directive(
        sample_robots_txt,
        ['GPTBot'],
        analyzer.llm_bots['GPTBot']
    )
    assert gptbot_directive["is_allowed"] is False
    assert "/private/" in gptbot_directive["disallowed_paths"]
    assert gptbot_directive["crawl_delay"] == 10
    assert "GPTBot" in gptbot_directive["user_agents_found"]

    # Test ClaudeBot directives
    claudebot_directive = analyzer._analyze_bot_directive(
        sample_robots_txt,
        ['ClaudeBot', 'anthropic-ai'],
        analyzer.llm_bots['ClaudeBot']
    )
    assert claudebot_directive["is_allowed"] is True
    assert claudebot_directive["crawl_delay"] == 5
    assert "ClaudeBot" in claudebot_directive["user_agents_found"]

    # Test Google-Extended directives
    google_directive = analyzer._analyze_bot_directive(
        sample_robots_txt,
        ['Google-Extended'],
        analyzer.llm_bots['Google-Extended']
    )
    assert google_directive["is_allowed"] is False
    assert "/api/" in google_directive["disallowed_paths"]
    assert "/admin/" in google_directive["disallowed_paths"]

def test_generate_bot_explanation(analyzer):
    """Test bot explanation generation."""
    # Test no directives found
    directives = {
        "allowed": True,
        "disallowed_paths": [],
        "crawl_delay": None,
        "user_agents_found": [],
        "directives_found": []
    }
    explanation = analyzer._generate_bot_explanation(directives, analyzer.llm_bots['GPTBot'])
    assert "No specific directives found" in explanation

    # Test blocked paths
    directives = {
        "allowed": False,
        "disallowed_paths": ["/private/", "/admin/"],
        "crawl_delay": None,
        "user_agents_found": ["GPTBot"],
        "directives_found": ["User-agent: GPTBot\nDisallow: /private/\nDisallow: /admin/"]
    }
    explanation = analyzer._generate_bot_explanation(directives, analyzer.llm_bots['GPTBot'])
    assert "blocked from" in explanation
    assert "/private/" in explanation
    assert "/admin/" in explanation

    # Test crawl delay
    directives = {
        "allowed": True,
        "disallowed_paths": [],
        "crawl_delay": 10,
        "user_agents_found": ["GPTBot"],
        "directives_found": ["User-agent: GPTBot\nCrawl-delay: 10"]
    }
    explanation = analyzer._generate_bot_explanation(directives, analyzer.llm_bots['GPTBot'])
    assert "allowed with 10s crawl delay" in explanation

def test_generate_llm_bot_summary(analyzer):
    """Test LLM bot summary generation."""
    bot_directives = {
        'GPTBot': {
            'company': 'OpenAI',
            'is_allowed': False
        },
        'ClaudeBot': {
            'company': 'Anthropic',
            'is_allowed': True
        },
        'Google-Extended': {
            'company': 'Google',
            'is_allowed': True
        }
    }
    
    summary = analyzer._generate_llm_bot_summary(bot_directives)
    assert "Allowed: Anthropic, Google" in summary
    assert "Blocked: OpenAI" in summary

def test_compute_overall_score(analyzer):
    """Test overall score computation."""
    indexability = {
        "is_indexable": True,
        "is_followable": True,
        "meta_robots_present": True,
        "meta_robots_content": "index,follow",
        "explanation": "Page is fully indexable and crawlable"
    }
    
    sitemap_status = {
        "sitemap_exists": True,
        "url_in_sitemap": True,
        "sitemap_url": "http://example.com/sitemap.xml",
        "explanation": "URL is included in sitemap.xml"
    }
    
    text_ratio = {
        "ratio": 50.0,
        "text_bytes": 1000,
        "html_bytes": 2000,
        "is_optimal": True,
        "explanation": "Optimal text-to-HTML ratio (50.0%)"
    }
    
    load_time = {
        "load_time": 1.5,
        "is_optimal": True,
        "status_code": 200,
        "explanation": "Fast page load time (1.50s)"
    }
    
    llm_bot_analysis = {
        "robots_txt_exists": True,
        "bot_directives": {
            'GPTBot': {'is_allowed': True},
            'ClaudeBot': {'is_allowed': True},
            'Google-Extended': {'is_allowed': True}
        }
    }
    
    result = analyzer._compute_overall_score(
        indexability, sitemap_status, text_ratio, load_time, llm_bot_analysis
    )
    
    assert "score" in result
    assert "components" in result
    assert "explanation" in result
    assert isinstance(result["score"], float)
    assert result["score"] > 0.8  # Should be excellent
    assert all(0 <= score <= 1 for score in result["components"].values())
    assert "llm_bot" in result["components"]

def test_get_explanations(analyzer):
    """Test explanation generation methods."""
    # Test indexability explanations
    assert "not indexable" in analyzer._get_indexability_explanation(True, False)
    assert "not followed" in analyzer._get_indexability_explanation(False, True)
    assert "fully indexable" in analyzer._get_indexability_explanation(False, False)
    
    # Test sitemap explanations
    assert "included" in analyzer._get_sitemap_explanation(True)
    assert "not included" in analyzer._get_sitemap_explanation(False)
    
    # Test text ratio explanations
    assert "Low" in analyzer._get_text_ratio_explanation(10.0)
    assert "High" in analyzer._get_text_ratio_explanation(80.0)
    assert "Optimal" in analyzer._get_text_ratio_explanation(50.0)
    
    # Test load time explanations
    assert "Fast" in analyzer._get_load_time_explanation(1.0)
    assert "Slow" in analyzer._get_load_time_explanation(3.0)
    
    # Test overall score explanations
    assert "Excellent" in analyzer._get_overall_score_explanation(0.9)
    assert "Good" in analyzer._get_overall_score_explanation(0.7)
    assert "Fair" in analyzer._get_overall_score_explanation(0.5)
    assert "Poor" in analyzer._get_overall_score_explanation(0.3) 