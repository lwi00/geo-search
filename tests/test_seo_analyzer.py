"""
Tests for the SEO analyzer module.
"""
import pytest
from src.seo_analyzer import SEOAnalyzer

# Sample HTML content for testing
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page Title</title>
    <meta charset="UTF-8">
    <meta name="description" content="This is a test page description">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://example.com/test">
    <meta property="og:title" content="OG Title">
    <meta property="og:description" content="OG Description">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Twitter Title">
    <link rel="icon" href="/favicon.ico">
</head>
<body>
    <h1>Main Header</h1>
    <div class="content">
        <h2>Section 1</h2>
        <p>This is some test content about SEO and optimization.</p>
        <h2>Section 2</h2>
        <p>More test content here about SEO analysis.</p>
        <img src="test.jpg" alt="Test Image" width="100" height="100">
        <img src="no-alt.jpg">
        <a href="/internal">Internal Link</a>
        <a href="https://external.com" rel="nofollow">External Link</a>
    </div>
    <script type="application/ld+json">
        {"@type": "WebPage"}
    </script>
    <script>
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r})(window,document);
    </script>
</body>
</html>
"""

class TestSEOAnalyzer:
    @pytest.fixture
    def analyzer(self):
        """Create an SEOAnalyzer instance for testing."""
        return SEOAnalyzer()

    @pytest.fixture
    def base_url(self):
        """Provide base URL for testing."""
        return "https://example.com"

    def test_meta_tags_analysis(self, analyzer):
        """Test meta tags analysis."""
        result = analyzer.analyze(SAMPLE_HTML, "https://example.com")['meta_tags']
        
        assert result['title']['content'] == "Test Page Title"
        assert result['meta_description']['content'] == "This is a test page description"
        assert "index, follow" in result['robots']
        assert result['charset'] == "UTF-8"
        assert result['canonical'] == "https://example.com/test"
        
        # Test OpenGraph tags
        assert result['og_tags']['og:title'] == "OG Title"
        assert result['og_tags']['og:description'] == "OG Description"
        
        # Test Twitter cards
        assert result['twitter_cards']['twitter:card'] == "summary"
        assert result['twitter_cards']['twitter:title'] == "Twitter Title"

    def test_keyword_analysis(self, analyzer):
        """Test keyword analysis."""
        result = analyzer.analyze(SAMPLE_HTML, "https://example.com")['keyword_analysis']
        
        assert result['total_words'] > 0
        assert result['unique_words'] > 0
        assert 'top_keywords' in result
        assert isinstance(result['top_keywords'], dict)
        
        # Check if 'seo' is in top keywords (appears twice in sample)
        seo_keyword = next((k for k in result['top_keywords'].keys() if k.lower() == 'seo'), None)
        assert seo_keyword is not None
        assert result['top_keywords'][seo_keyword]['count'] == 2

    def test_content_analysis(self, analyzer):
        """Test content structure analysis."""
        result = analyzer.analyze(SAMPLE_HTML, "https://example.com")['content_analysis']
        
        assert result['paragraph_count'] == 2
        assert result['heading_structure']['h1'] == 1
        assert result['heading_structure']['h2'] == 2
        assert result['content_length'] > 0
        assert 0 <= result['text_html_ratio'] <= 100

    def test_link_analysis(self, analyzer, base_url):
        """Test link analysis."""
        result = analyzer.analyze(SAMPLE_HTML, base_url)['link_analysis']
        
        assert result['internal_links']['count'] == 1
        assert result['external_links']['count'] == 1
        
        # Check internal link
        internal = result['internal_links']['links'][0]
        assert internal['text'] == "Internal Link"
        assert internal['url'] == "https://example.com/internal"
        
        # Check external link
        external = result['external_links']['links'][0]
        assert external['text'] == "External Link"
        assert external['url'] == "https://external.com"
        assert external['nofollow'] is True

    def test_image_analysis(self, analyzer):
        """Test image analysis."""
        result = analyzer.analyze(SAMPLE_HTML, "https://example.com")['image_analysis']
        
        assert result['total_images'] == 2
        assert result['images_with_alt'] == 1
        assert result['images_with_dimensions'] == 1
        
        # Check specific image details
        images = result['image_details']
        assert any(img['alt'] == "Test Image" for img in images)
        assert any(img['has_dimensions'] for img in images)

    def test_technical_seo(self, analyzer):
        """Test technical SEO analysis."""
        result = analyzer.analyze(SAMPLE_HTML, "https://example.com")['technical_seo']
        
        assert result['has_viewport'] is True
        assert result['has_favicon'] is True
        assert result['has_structured_data'] is True
        assert result['has_analytics'] is True
        assert result['has_robots_txt'] is True

    def test_url_structure(self, analyzer):
        """Test URL structure analysis."""
        test_url = "https://example.com/blog/post?id=1#section"
        result = analyzer.analyze(SAMPLE_HTML, test_url)['url_structure']
        
        assert result['protocol'] == "https"
        assert result['domain'] == "example.com"
        assert result['path_depth'] == 2
        assert result['path_segments'] == ['blog', 'post']
        assert result['has_query_params'] is True
        assert result['has_fragment'] is True
        assert result['is_clean_url'] is False 