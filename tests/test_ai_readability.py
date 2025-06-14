"""
Tests for AIReadabilityAnalyzer (SEO Structure Metrics)
"""
import pytest
from src.ai_readability import AIReadabilityAnalyzer
from unittest.mock import patch

@pytest.fixture
def analyzer():
    return AIReadabilityAnalyzer()

@pytest.fixture
def good_seo_analysis():
    return {
        'meta_tags': {
            'title': {'content': 'A Good Title for AI and Search', 'length': 29, 'found': True},
            'meta_description': {'content': 'A concise and relevant meta description for the page.', 'length': 53, 'found': True}
        },
        'content_analysis': {
            'main_content': ' '.join(['word'] * 350),
            'heading_structure': {'h1': 1}
        }
    }

@pytest.fixture
def bad_seo_analysis():
    return {
        'meta_tags': {
            'title': {'content': 'Short', 'length': 5, 'found': True},
            'meta_description': {'content': '', 'length': 0, 'found': False}
        },
        'content_analysis': {
            'main_content': 'Too short.',
            'heading_structure': {'h1': 0}
        }
    }

@pytest.fixture
def long_title_analysis():
    return {
        'meta_tags': {
            'title': {'content': 'T' * 80, 'length': 80, 'found': True},
            'meta_description': {'content': 'D' * 200, 'length': 200, 'found': True}
        },
        'content_analysis': {
            'main_content': ' '.join(['word'] * 400),
            'heading_structure': {'h1': 2}
        }
    }

def test_good_seo_structure(analyzer, good_seo_analysis):
    result = analyzer.analyze_seo_structure(good_seo_analysis)
    assert result['title_tag_length']['optimal'] is False  # 29 < 50
    assert result['meta_description_length']['optimal'] is True
    assert result['h1_tag_presence']['optimal'] is True
    assert result['content_word_count']['optimal'] is True
    assert 'Optimal' in result['meta_description_length']['explanation']
    assert 'Optimal' in result['h1_tag_presence']['explanation']
    assert 'Optimal' in result['content_word_count']['explanation']

def test_bad_seo_structure(analyzer, bad_seo_analysis):
    result = analyzer.analyze_seo_structure(bad_seo_analysis)
    assert result['title_tag_length']['optimal'] is False
    assert result['meta_description_length']['optimal'] is False
    assert result['h1_tag_presence']['optimal'] is False
    assert result['content_word_count']['optimal'] is False
    assert 'Too short' in result['title_tag_length']['explanation']
    assert 'Missing' in result['meta_description_length']['explanation']
    assert 'Missing' in result['h1_tag_presence']['explanation']
    assert 'Too little content' in result['content_word_count']['explanation']

def test_long_title_and_meta(analyzer, long_title_analysis):
    result = analyzer.analyze_seo_structure(long_title_analysis)
    assert result['title_tag_length']['optimal'] is False
    assert result['meta_description_length']['optimal'] is False
    assert result['h1_tag_presence']['optimal'] is False
    assert result['content_word_count']['optimal'] is True
    assert 'Too long' in result['title_tag_length']['explanation']
    assert 'Too long' in result['meta_description_length']['explanation']
    assert 'Multiple H1 tags' in result['h1_tag_presence']['explanation']
    assert 'Optimal' in result['content_word_count']['explanation']

def test_missing_fields(analyzer):
    # Should handle missing fields gracefully
    result = analyzer.analyze_seo_structure({})
    assert result['title_tag_length']['optimal'] is False
    assert result['meta_description_length']['optimal'] is False
    assert result['h1_tag_presence']['optimal'] is False
    assert result['content_word_count']['optimal'] is False

def html_sample(semantic=True, valid=True, heading_skip=False):
    # Compose HTML with options for semantic tags, validity, and heading order
    semantic_tags = "<header></header><nav></nav><main></main><article></article><section></section><footer></footer><aside></aside>" if semantic else ""
    divs = "<div></div>" * 6
    headings = "<h1>Title</h1><h2>Section</h2><h3>Subsection</h3>" if not heading_skip else "<h1>Title</h1><h3>Skipped</h3>"
    html = f"<html><body>{semantic_tags}{divs}{headings}</body></html>"
    if not valid:
        html = html.replace("</footer>", "")  # Remove closing tag to make invalid
    return html

def test_semantic_element_usage_optimal(analyzer):
    html = html_sample(semantic=True)
    result = analyzer.analyze_semantic_and_structure(html, {})
    assert result['semantic_element_usage']['optimal'] is True
    assert result['semantic_element_usage']['semantic_count'] > 0
    assert result['semantic_element_usage']['ratio'] >= 0.5
    assert 'Optimal' in result['semantic_element_usage']['explanation']

def test_semantic_element_usage_suboptimal(analyzer):
    html = html_sample(semantic=False)
    result = analyzer.analyze_semantic_and_structure(html, {})
    assert result['semantic_element_usage']['optimal'] is False
    assert result['semantic_element_usage']['semantic_count'] == 0
    assert 'Suboptimal' in result['semantic_element_usage']['explanation']

def test_html_validation_errors_none(analyzer):
    html = "<html><body><p>Valid HTML</p></body></html>"
    with patch('html5lib.HTMLParser') as mock_parser:
        mock_parser.return_value.parse.return_value = None
        mock_parser.return_value.errors = []
        result = analyzer.analyze_semantic_and_structure(html, {})
        assert result['html_validation_errors']['optimal'] is True
        assert result['html_validation_errors']['error_count'] == 0
        assert 'Optimal' in result['html_validation_errors']['explanation']

def test_html_validation_errors_present(analyzer):
    html = html_sample(valid=False)
    result = analyzer.analyze_semantic_and_structure(html, {})
    assert result['html_validation_errors']['optimal'] is False
    assert result['html_validation_errors']['error_count'] >= 1
    assert 'error' in result['html_validation_errors']['explanation']

def test_heading_hierarchy_optimal(analyzer):
    html = html_sample(heading_skip=False)
    result = analyzer.analyze_semantic_and_structure(html, {})
    assert result['heading_hierarchy_order']['optimal'] is True
    assert 'Optimal' in result['heading_hierarchy_order']['explanation']

def test_heading_hierarchy_skipped(analyzer):
    html = html_sample(heading_skip=True)
    result = analyzer.analyze_semantic_and_structure(html, {})
    assert result['heading_hierarchy_order']['optimal'] is False
    assert 'skipped' in result['heading_hierarchy_order']['explanation']

def test_heading_hierarchy_none(analyzer):
    html = "<html><body>No headings here</body></html>"
    result = analyzer.analyze_semantic_and_structure(html, {})
    assert result['heading_hierarchy_order']['optimal'] is False
    assert 'No headings' in result['heading_hierarchy_order']['explanation'] 