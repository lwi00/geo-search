"""
Text readability analysis module for GeoSearch.
"""
import re
from typing import Dict, List, Tuple
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict

class ReadabilityAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/cmudict')
        except LookupError:
            nltk.download('punkt')
            nltk.download('cmudict')
        
        self.cmudict = cmudict.dict()
        self.ideal_sentence_length = 14  # words
        self.max_sentence_length = 20    # words
        self.complex_word_threshold = 3  # syllables
        self.complex_word_percentage_threshold = 15  # percentage

    def analyze_readability(self, text: str) -> Dict:
        """
        Analyze text readability metrics.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Readability analysis results
        """
        # Clean and prepare text
        cleaned_text = self._clean_text(text)
        
        # Get basic text statistics
        sentences = sent_tokenize(cleaned_text)
        words = word_tokenize(cleaned_text)
        
        # Calculate metrics
        flesch_score = self._calculate_flesch_score(sentences, words)
        avg_sentence_length = self._calculate_avg_sentence_length(sentences, words)
        lexical_complexity = self._calculate_lexical_complexity(words)
        
        return {
            "flesch_reading_ease": flesch_score,
            "average_sentence_length": avg_sentence_length,
            "lexical_complexity": lexical_complexity,
            "overall_score": self._compute_overall_score(flesch_score, avg_sentence_length, lexical_complexity)
        }

    def _clean_text(self, text: str) -> str:
        """Clean text for analysis."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep sentence endings
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        return text.strip()

    def _calculate_flesch_score(self, sentences: List[str], words: List[str]) -> Dict:
        """
        Calculate Flesch Reading Ease score.
        Formula: RE = 206.835 - 1.015*(words/sentence) - 84.6*(syllables/word)
        """
        if not sentences or not words:
            return {
                "score": 0,
                "explanation": "No text content to analyze",
                "is_optimal": False
            }
        
        # Calculate average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Calculate average syllables per word
        total_syllables = sum(self._count_syllables(word) for word in words)
        avg_syllables = total_syllables / len(words)
        
        # Calculate Flesch score
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
        
        # Determine readability level
        if score >= 90:
            level = "Very Easy"
        elif score >= 80:
            level = "Easy"
        elif score >= 70:
            level = "Fairly Easy"
        elif score >= 60:
            level = "Standard"
        elif score >= 50:
            level = "Fairly Difficult"
        elif score >= 30:
            level = "Difficult"
        else:
            level = "Very Difficult"
        
        return {
            "score": score,
            "level": level,
            "avg_sentence_length": avg_sentence_length,
            "avg_syllables_per_word": avg_syllables,
            "is_optimal": 60 <= score <= 80,  # Optimal range for general audience
            "explanation": f"Flesch Reading Ease: {score:.1f} ({level})"
        }

    def _calculate_avg_sentence_length(self, sentences: List[str], words: List[str]) -> Dict:
        """Calculate average sentence length."""
        if not sentences:
            return {
                "score": 0,
                "explanation": "No sentences found",
                "is_optimal": False
            }
        
        avg_length = len(words) / len(sentences)
        
        # Calculate percentage of sentences within optimal range
        optimal_sentences = sum(1 for s in sentences if len(word_tokenize(s)) <= self.ideal_sentence_length)
        optimal_percentage = (optimal_sentences / len(sentences)) * 100
        
        return {
            "avg_length": avg_length,
            "optimal_percentage": optimal_percentage,
            "is_optimal": avg_length <= self.ideal_sentence_length,
            "explanation": self._get_sentence_length_explanation(avg_length, optimal_percentage)
        }

    def _calculate_lexical_complexity(self, words: List[str]) -> Dict:
        """Calculate lexical complexity based on complex word percentage."""
        if not words:
            return {
                "score": 0,
                "explanation": "No words found",
                "is_optimal": False
            }
        
        # Count complex words (3+ syllables)
        complex_words = sum(1 for word in words if self._count_syllables(word) >= self.complex_word_threshold)
        complex_percentage = (complex_words / len(words)) * 100
        
        return {
            "complex_words": complex_words,
            "complex_percentage": complex_percentage,
            "is_optimal": complex_percentage <= self.complex_word_percentage_threshold,
            "explanation": self._get_lexical_complexity_explanation(complex_percentage)
        }

    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word using CMU dictionary."""
        word = word.lower()
        try:
            return len([x for x in self.cmudict[word][0] if x[-1].isdigit()])
        except KeyError:
            # Fallback to simple syllable counting
            count = 0
            vowels = 'aeiouy'
            word = word.lower()
            if word[0] in vowels:
                count += 1
            for index in range(1, len(word)):
                if word[index] in vowels and word[index - 1] not in vowels:
                    count += 1
            if word.endswith('e'):
                count -= 1
            if count == 0:
                count += 1
            return count

    def _compute_overall_score(self, flesch: Dict, sentence_length: Dict, lexical: Dict) -> Dict:
        """Compute overall readability score."""
        # Weight factors for each metric
        weights = {
            "flesch": 0.4,
            "sentence_length": 0.3,
            "lexical": 0.3
        }
        
        # Calculate individual scores
        flesch_score = 1.0 if flesch["is_optimal"] else 0.5
        sentence_score = 1.0 if sentence_length["is_optimal"] else 0.5
        lexical_score = 1.0 if lexical["is_optimal"] else 0.5
        
        # Calculate weighted score
        overall_score = (
            flesch_score * weights["flesch"] +
            sentence_score * weights["sentence_length"] +
            lexical_score * weights["lexical"]
        )
        
        return {
            "score": overall_score,
            "components": {
                "flesch": flesch_score,
                "sentence_length": sentence_score,
                "lexical": lexical_score
            },
            "explanation": self._get_overall_score_explanation(overall_score)
        }

    def _get_sentence_length_explanation(self, avg_length: float, optimal_percentage: float) -> str:
        """Generate explanation for sentence length analysis."""
        if avg_length <= self.ideal_sentence_length:
            return f"Optimal average sentence length ({avg_length:.1f} words)"
        elif avg_length <= self.max_sentence_length:
            return f"Acceptable average sentence length ({avg_length:.1f} words)"
        else:
            return f"Long average sentence length ({avg_length:.1f} words) - may affect readability"

    def _get_lexical_complexity_explanation(self, complex_percentage: float) -> str:
        """Generate explanation for lexical complexity analysis."""
        if complex_percentage <= self.complex_word_percentage_threshold:
            return f"Good lexical complexity ({complex_percentage:.1f}% complex words)"
        else:
            return f"High lexical complexity ({complex_percentage:.1f}% complex words) - may affect readability"

    def _get_overall_score_explanation(self, score: float) -> str:
        """Generate explanation for overall readability score."""
        if score >= 0.8:
            return "Excellent readability"
        if score >= 0.6:
            return "Good readability"
        if score >= 0.4:
            return "Fair readability"
        return "Poor readability" 