"""
Tests for the web scraper module.
"""
import pytest
from src.scraper import WebScraper
from bs4 import BeautifulSoup

# Sample HTML content for testing
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
    <meta name="description" content="This is a test page description">
</head>
<body>
    <h1>Main Header</h1>
    <div class="content">
        <h2>Section 1</h2>
        <p>This is some test content.</p>
        <h2>Section 2</h2>
        <p>More test content here.</p>
    </div>
    <script>
        console.log("This should be removed");
    </script>
    <style>
        body { color: black; }
    </style>
</body>
</html>
"""

class TestWebScraper:
    @pytest.fixture
    def scraper(self):
        """Create a WebScraper instance for testing."""
        return WebScraper()

    @pytest.fixture
    def mock_response(self, mocker):
        """Create a mock response for requests."""
        mock = mocker.patch('requests.get')
        mock.return_value.text = SAMPLE_HTML
        mock.return_value.raise_for_status = lambda: None
        return mock

    def test_fetch_page_success(self, scraper, mock_response):
        """Test successful page fetch."""
        result = scraper.fetch_page("http://example.com")
        assert result == SAMPLE_HTML
        mock_response.assert_called_once_with("http://example.com", timeout=30)

    def test_fetch_page_failure(self, scraper, mocker):
        """Test failed page fetch."""
        mock = mocker.patch('requests.get', side_effect=Exception("Connection error"))
        result = scraper.fetch_page("http://example.com")
        assert result is None
        mock.assert_called_once_with("http://example.com", timeout=30)

    def test_get_title(self, scraper):
        """Test title extraction."""
        soup = BeautifulSoup(SAMPLE_HTML, 'html.parser')
        title = scraper._get_title(soup)
        assert title == "Test Page"

    def test_get_meta_description(self, scraper):
        """Test meta description extraction."""
        soup = BeautifulSoup(SAMPLE_HTML, 'html.parser')
        description = scraper._get_meta_description(soup)
        assert description == "This is a test page description"

    def test_get_headers(self, scraper):
        """Test headers extraction."""
        soup = BeautifulSoup(SAMPLE_HTML, 'html.parser')
        headers = scraper._get_headers(soup)
        assert headers == {
            'h1': ['Main Header'],
            'h2': ['Section 1', 'Section 2']
        }

    def test_get_main_content(self, scraper):
        """Test main content extraction."""
        soup = BeautifulSoup(SAMPLE_HTML, 'html.parser')
        content = scraper._get_main_content(soup)
        # Check that script and style contents are removed
        assert "console.log" not in content
        assert "color: black" not in content
        # Check that actual content is present
        assert "Main Header" in content
        assert "This is some test content" in content
        assert "More test content here" in content

    def test_extract_content_complete(self, scraper):
        """Test complete content extraction."""
        result = scraper.extract_content(SAMPLE_HTML)
        assert isinstance(result, dict)
        assert result['title'] == "Test Page"
        assert result['meta_description'] == "This is a test page description"
        assert isinstance(result['main_content'], str)
        assert isinstance(result['headers'], dict)
        assert len(result['headers']) == 2  # h1 and h2 present 