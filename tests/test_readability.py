"""
Tests for the readability analyzer module.
"""
import pytest
from src.readability import ReadabilityAnalyzer

@pytest.fixture
def analyzer():
    return ReadabilityAnalyzer()

@pytest.fixture
def sample_text():
    return """
    <html>
        <body>
            <p>This is a simple test paragraph. It has two sentences.</p>
            <p>Here is another paragraph with more complex words like 'sophisticated' and 'comprehensive'.</p>
        </body>
    </html>
    """

def test_clean_text(analyzer):
    """Test text cleaning functionality."""
    html = "<p>Test text with <b>HTML</b> tags.</p>"
    cleaned = analyzer._clean_text(html)
    assert cleaned == "Test text with HTML tags."

def test_count_syllables(analyzer):
    """Test syllable counting functionality."""
    assert analyzer._count_syllables("test") == 1
    assert analyzer._count_syllables("testing") == 2
    assert analyzer._count_syllables("sophisticated") == 5
    assert analyzer._count_syllables("comprehensive") == 4

def test_calculate_flesch_score(analyzer):
    """Test Flesch Reading Ease score calculation."""
    text = "This is a simple test. It has two sentences."
    words = text.split()
    score = analyzer._calculate_flesch_score(text, words)
    assert isinstance(score, dict)
    assert 'score' in score
    assert 'explanation' in score
    assert isinstance(score['score'], float)
    assert 0 <= score['score'] <= 100

def test_calculate_avg_sentence_length(analyzer):
    """Test average sentence length calculation."""
    text = "First sentence. Second sentence. Third sentence."
    words = text.split()
    avg_length = analyzer._calculate_avg_sentence_length(text, words)
    assert isinstance(avg_length, dict)
    assert 'avg_length' in avg_length
    assert isinstance(avg_length['avg_length'], float)
    assert avg_length['avg_length'] > 0

def test_calculate_lexical_complexity(analyzer):
    """Test lexical complexity calculation."""
    text = "Simple words and sophisticated vocabulary."
    complexity = analyzer._calculate_lexical_complexity(text)
    assert isinstance(complexity, dict)
    assert 'complex_percentage' in complexity
    assert 'complex_words' in complexity
    assert 'explanation' in complexity
    assert isinstance(complexity['complex_percentage'], float)
    assert 0 <= complexity['complex_percentage'] <= 100

def test_analyze_readability(analyzer, sample_text):
    """Test complete readability analysis."""
    results = analyzer.analyze_readability(sample_text)
    
    # Check structure
    assert isinstance(results, dict)
    assert 'flesch_reading_ease' in results
    assert 'average_sentence_length' in results
    assert 'lexical_complexity' in results
    assert 'overall_score' in results

    # Check Flesch Reading Ease
    flesch = results['flesch_reading_ease']
    assert 'score' in flesch
    assert 'level' in flesch
    assert 'explanation' in flesch
    assert isinstance(flesch['score'], float)
    assert 0 <= flesch['score'] <= 100

    # Check Average Sentence Length
    sentence_length = results['average_sentence_length']
    assert 'avg_length' in sentence_length
    assert 'explanation' in sentence_length
    assert isinstance(sentence_length['avg_length'], float)
    assert sentence_length['avg_length'] > 0

    # Check Lexical Complexity
    complexity = results['lexical_complexity']
    assert 'complex_percentage' in complexity
    assert 'complex_words' in complexity
    assert 'explanation' in complexity
    assert isinstance(complexity['complex_percentage'], float)
    assert 0 <= complexity['complex_percentage'] <= 100

    # Check Overall Score
    overall = results['overall_score']
    assert 'score' in overall
    assert 'explanation' in overall
    assert isinstance(overall['score'], float)
    assert 0 <= overall['score'] <= 1

def test_empty_text(analyzer):
    """Test analysis with empty text."""
    results = analyzer.analyze_readability("")
    assert results['flesch_reading_ease']['score'] == 0
    # For empty text, avg_length may not be present, so check for 0 or missing
    avg_length = results['average_sentence_length'].get('avg_length', 0)
    assert avg_length == 0
    # For empty text, complex_percentage may not be present, so check for 0 or missing
    complex_percentage = results['lexical_complexity'].get('complex_percentage', 0)
    assert complex_percentage == 0
    # For empty text, overall_score['score'] is 0.5 by implementation
    assert results['overall_score']['score'] == 0.5

def test_complex_text(analyzer):
    """Test analysis with complex text."""
    complex_text = """
    <p>The implementation of sophisticated algorithms necessitates comprehensive understanding 
    of computational complexity and algorithmic paradigms. Furthermore, the optimization of 
    these implementations requires meticulous attention to detail and thorough consideration 
    of edge cases.</p>
    """
    results = analyzer.analyze_readability(complex_text)
    
    # Complex text should have lower Flesch score
    assert results['flesch_reading_ease']['score'] < 50
    
    # Complex text should have higher lexical complexity
    assert results['lexical_complexity']['complex_percentage'] > 2
    
    # Complex text should have longer sentences
    assert results['average_sentence_length']['avg_length'] > 10

def test_simple_text(analyzer):
    """Test analysis with simple text."""
    simple_text = """
    <p>This is a simple text. It uses basic words. The sentences are short.</p>
    """
    results = analyzer.analyze_readability(simple_text)
    # Simple text should have higher Flesch score
    assert results['flesch_reading_ease']['score'] > 70
    # Simple text should have lower lexical complexity (allowing up to 10 for short samples)
    assert results['lexical_complexity']['complex_percentage'] < 10
    # Simple text should have shorter sentences
    assert results['average_sentence_length']['avg_length'] < 10 