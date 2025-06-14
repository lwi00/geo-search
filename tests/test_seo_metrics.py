"""
Tests for the SEO metrics module.
"""
import pytest
from src.seo_metrics import SEOMetrics

@pytest.fixture
def seo_metrics():
    """Create a SEOMetrics instance for testing."""
    return SEOMetrics()

@pytest.fixture
def sample_analysis():
    """Create a sample SEO analysis for testing."""
    return {
        'content_analysis': {
            'content_length': 1500,
            'heading_structure': {
                'h1': 1,
                'h2': 3,
                'h3': 5
            },
            'paragraph_count': 10,
            'avg_paragraph_length': 150,
            'text_html_ratio': 25,
            'main_content': 'This is a sample text. It has multiple sentences. The text is used for testing readability scores.'
        },
        'meta_tags': {
            'title': {
                'content': 'Sample Title - Test Page',
                'length': 25,
                'found': True
            },
            'meta_description': {
                'content': 'This is a sample meta description for testing purposes.',
                'length': 55,
                'found': True
            }
        },
        'keyword_analysis': {
            'top_keywords': {
                'sample': {'density': 2.5},
                'test': {'density': 1.8},
                'content': {'density': 1.2}
            }
        },
        'link_analysis': {
            'internal_links': {
                'count': 5,
                'links': [
                    {'text': 'Home', 'url': '/home'},
                    {'text': 'About', 'url': '/about'}
                ]
            },
            'external_links': {
                'count': 3,
                'links': [
                    {'text': 'External Site', 'url': 'https://example.com'},
                    {'text': 'Another Site', 'url': 'https://another.com'}
                ]
            }
        },
        'image_analysis': {
            'total_images': 4,
            'images_with_alt': 3,
            'images_with_dimensions': 2
        },
        'technical_seo': {
            'has_viewport': True,
            'has_favicon': True,
            'has_structured_data': False,
            'has_analytics': True,
            'has_robots_txt': True
        }
    }

def test_compute_metrics(seo_metrics, sample_analysis):
    """Test the main compute_metrics method."""
    metrics = seo_metrics.compute_metrics(sample_analysis)
    
    assert 'content_quality' in metrics
    assert 'technical_score' in metrics
    assert 'readability' in metrics
    assert 'keyword_optimization' in metrics
    assert 'link_quality' in metrics
    assert 'image_optimization' in metrics
    assert 'overall_score' in metrics

def test_compute_metrics_empty_analysis(seo_metrics):
    """Test compute_metrics with empty analysis."""
    metrics = seo_metrics.compute_metrics({})
    
    assert metrics['content_quality']['overall_content_score'] == 0.0
    assert metrics['technical_score']['overall_technical_score'] == 0.0
    assert metrics['readability']['flesch_reading_ease'] == 0.0
    assert metrics['keyword_optimization']['keyword_optimization_score'] == 0.0
    assert metrics['link_quality']['overall_link_quality_score'] == 0.0
    assert metrics['image_optimization']['overall_image_score'] == 0.0
    assert metrics['overall_score']['overall_score'] == 0.0

def test_content_quality_metrics(seo_metrics, sample_analysis):
    """Test content quality metrics calculation."""
    metrics = seo_metrics._compute_content_quality(sample_analysis)
    
    assert 0 <= metrics['content_length_score'] <= 1
    assert 0 <= metrics['heading_structure_score'] <= 1
    assert 0 <= metrics['paragraph_structure_score'] <= 1
    assert 0 <= metrics['text_html_ratio_score'] <= 1
    assert 0 <= metrics['overall_content_score'] <= 1

def test_readability_metrics(seo_metrics, sample_analysis):
    """Test readability metrics calculation."""
    metrics = seo_metrics._compute_readability(sample_analysis)
    
    assert isinstance(metrics['flesch_reading_ease'], float)
    assert isinstance(metrics['avg_sentence_length'], float)
    assert isinstance(metrics['avg_word_length'], float)
    assert isinstance(metrics['readability_level'], str)
    assert metrics['readability_level'] in [
        'Very Easy', 'Easy', 'Fairly Easy', 'Standard',
        'Fairly Difficult', 'Difficult', 'Very Difficult', 'Unknown'
    ]

def test_keyword_optimization(seo_metrics, sample_analysis):
    """Test keyword optimization metrics calculation."""
    metrics = seo_metrics._compute_keyword_optimization(sample_analysis)
    
    assert isinstance(metrics['keyword_density_scores'], dict)
    assert isinstance(metrics['keywords_in_title'], list)
    assert isinstance(metrics['keywords_in_meta'], list)
    assert 0 <= metrics['keyword_optimization_score'] <= 1

def test_link_quality(seo_metrics, sample_analysis):
    """Test link quality metrics calculation."""
    metrics = seo_metrics._compute_link_quality(sample_analysis)
    
    assert 0 <= metrics['internal_external_ratio'] <= 1
    assert 0 <= metrics['internal_link_text_score'] <= 1
    assert 0 <= metrics['external_link_text_score'] <= 1
    assert 0 <= metrics['overall_link_quality_score'] <= 1

def test_image_optimization(seo_metrics, sample_analysis):
    """Test image optimization metrics calculation."""
    metrics = seo_metrics._compute_image_optimization(sample_analysis)
    
    assert 0 <= metrics['alt_text_score'] <= 1
    assert 0 <= metrics['dimensions_score'] <= 1
    assert 0 <= metrics['overall_image_score'] <= 1

def test_technical_score(seo_metrics, sample_analysis):
    """Test technical SEO score calculation."""
    metrics = seo_metrics._compute_technical_score(sample_analysis)
    
    assert 0 <= metrics['meta_tags_score'] <= 1
    assert 0 <= metrics['technical_elements_score'] <= 1
    assert 0 <= metrics['overall_technical_score'] <= 1

def test_overall_score(seo_metrics, sample_analysis):
    """Test overall score calculation."""
    metrics = seo_metrics._compute_overall_score(sample_analysis)
    
    assert 0 <= metrics['overall_score'] <= 1
    assert all(0 <= score <= 1 for score in metrics['score_breakdown'].values())

def test_normalize_score(seo_metrics):
    """Test score normalization."""
    # Test value within range
    assert seo_metrics._normalize_score(50, 30, 60) == 1.0
    
    # Test value below range
    assert 0 <= seo_metrics._normalize_score(20, 30, 60) < 1.0
    
    # Test value above range
    assert 0 <= seo_metrics._normalize_score(70, 30, 60) < 1.0
    
    # Test edge cases
    assert seo_metrics._normalize_score(0, 0, 0) == 0.0
    assert seo_metrics._normalize_score(0, 1, 1) == 0.0

def test_count_syllables(seo_metrics):
    """Test syllable counting."""
    assert seo_metrics._count_syllables('hello') > 0
    assert seo_metrics._count_syllables('') == 0
    assert seo_metrics._count_syllables('a') == 1
    assert seo_metrics._count_syllables('test') == 1

def test_get_readability_level(seo_metrics):
    """Test readability level determination."""
    assert seo_metrics._get_readability_level(95) == 'Very Easy'
    assert seo_metrics._get_readability_level(85) == 'Easy'
    assert seo_metrics._get_readability_level(75) == 'Fairly Easy'
    assert seo_metrics._get_readability_level(65) == 'Standard'
    assert seo_metrics._get_readability_level(55) == 'Fairly Difficult'
    assert seo_metrics._get_readability_level(25) == 'Difficult'
    assert seo_metrics._get_readability_level(15) == 'Very Difficult'
    assert seo_metrics._get_readability_level(-1) == 'Unknown'

def test_get_keywords_in_text(seo_metrics):
    """Test keyword extraction from text."""
    text = 'This is a sample text with some keywords'
    keywords = seo_metrics._get_keywords_in_text(text)
    
    assert isinstance(keywords, list)
    assert 'sample' in keywords
    assert 'keywords' in keywords
    assert 'this' not in keywords  # Should be filtered as stop word
    assert 'is' not in keywords    # Should be filtered as stop word

def test_calculate_link_text_score(seo_metrics):
    """Test link text quality scoring."""
    links = [
        {'text': 'Good Link Text'},
        {'text': 'Another Good Link'},
        {'text': 'a'}  # Too short
    ]
    
    score = seo_metrics._calculate_link_text_score(links)
    assert 0 <= score <= 1

def test_error_handling(seo_metrics):
    """Test error handling with invalid data."""
    # Test with None
    metrics = seo_metrics.compute_metrics(None)
    assert metrics['overall_score']['overall_score'] == 0.0
    
    # Test with empty dict
    metrics = seo_metrics.compute_metrics({})
    assert metrics['overall_score']['overall_score'] == 0.0
    
    # Test with missing keys
    metrics = seo_metrics.compute_metrics({'content_analysis': {}})
    assert metrics['overall_score']['overall_score'] == 0.0
    
    # Test with invalid values
    metrics = seo_metrics.compute_metrics({
        'content_analysis': {
            'content_length': 'invalid',
            'heading_structure': None
        }
    })
    assert metrics['overall_score']['overall_score'] == 0.0 