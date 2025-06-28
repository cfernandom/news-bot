"""
Unit tests for sentiment analysis functionality
Tests SentimentAnalyzer class in isolation with mocked dependencies
"""

import pytest
from unittest.mock import Mock, patch
from services.nlp.src.sentiment import SentimentAnalyzer, get_sentiment_analyzer

class TestSentimentAnalyzer:
    """Test SentimentAnalyzer class functionality"""
    
    def test_init_without_spacy(self):
        """Test analyzer initialization when spaCy model is not available"""
        with patch('spacy.load', side_effect=OSError("Model not found")):
            analyzer = SentimentAnalyzer()
            assert analyzer.nlp is None
            assert analyzer.analyzer is not None  # VADER should still work
    
    def test_init_with_spacy(self):
        """Test analyzer initialization with spaCy model available"""
        mock_nlp = Mock()
        with patch('spacy.load', return_value=mock_nlp):
            analyzer = SentimentAnalyzer()
            assert analyzer.nlp is mock_nlp
            assert analyzer.analyzer is not None
    
    def test_analyze_sentiment_empty_text(self):
        """Test sentiment analysis with empty text"""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_sentiment("")
        
        assert result['sentiment_label'] == 'neutral'
        assert result['confidence'] == 0.0
        assert result['scores']['compound'] == 0.0
        assert result['text_length'] == 0
    
    def test_analyze_sentiment_positive_text(self):
        """Test sentiment analysis with positive medical content"""
        analyzer = SentimentAnalyzer()
        text = "Breakthrough cancer treatment shows excellent results with promising outcomes"
        
        result = analyzer.analyze_sentiment(text)
        
        assert result['sentiment_label'] in ['positive', 'neutral']  # Medical context is more conservative
        assert 0.0 <= result['confidence'] <= 1.0
        assert 'scores' in result
        assert 'positive' in result['scores']
        assert result['text_length'] > 0
    
    def test_analyze_sentiment_negative_text(self):
        """Test sentiment analysis with negative medical content"""
        analyzer = SentimentAnalyzer()
        text = "Cancer rates continue to rise with devastating effects on patients"
        
        result = analyzer.analyze_sentiment(text)
        
        assert result['sentiment_label'] in ['negative', 'neutral']
        assert 0.0 <= result['confidence'] <= 1.0
        assert result['scores']['negative'] > 0
    
    def test_analyze_sentiment_with_title(self):
        """Test sentiment analysis combining title and content"""
        analyzer = SentimentAnalyzer()
        title = "Medical Breakthrough"
        content = "Research shows positive results"
        
        result = analyzer.analyze_sentiment(content, title)
        
        assert result['processed_text_length'] > result['text_length']  # Title added to content
        assert result['sentiment_label'] in ['positive', 'negative', 'neutral']
    
    def test_medical_sentiment_thresholds(self):
        """Test medical-specific sentiment interpretation thresholds"""
        analyzer = SentimentAnalyzer()
        
        # Mock VADER scores for testing thresholds
        test_cases = [
            {'compound': 0.5, 'expected': 'positive'},    # Strong positive
            {'compound': 0.2, 'expected': 'positive'},    # Moderate positive
            {'compound': 0.05, 'expected': 'neutral'},    # Neutral
            {'compound': -0.2, 'expected': 'negative'},   # Moderate negative
            {'compound': -0.5, 'expected': 'negative'},   # Strong negative
        ]
        
        for case in test_cases:
            scores = {
                'pos': 0.3, 'neg': 0.1, 'neu': 0.6, 
                'compound': case['compound']
            }
            label, confidence = analyzer._interpret_medical_sentiment(scores)
            assert label == case['expected'], f"Failed for compound score {case['compound']}"
            assert 0.0 <= confidence <= 1.0
    
    def test_preprocess_text_without_spacy(self):
        """Test text preprocessing when spaCy is not available"""
        analyzer = SentimentAnalyzer()
        analyzer.nlp = None  # Simulate no spaCy
        
        text = "This is a test text"
        result = analyzer._preprocess_text(text)
        
        assert result == text  # Should return unchanged
    
    def test_analyze_batch(self):
        """Test batch analysis of multiple articles"""
        analyzer = SentimentAnalyzer()
        
        # Mock articles with proper attributes
        mock_article1 = Mock()
        mock_article1.summary = "Positive medical news"
        mock_article1.title = "Good news"
        mock_article1.id = 1
        mock_article1.content = "Positive medical news content"
        
        mock_article2 = Mock()
        mock_article2.summary = "Negative health update"
        mock_article2.title = "Bad news"
        mock_article2.id = 2
        mock_article2.content = "Negative health update content"
        
        mock_article3 = Mock()
        mock_article3.summary = ""
        mock_article3.title = ""
        mock_article3.id = 3
        mock_article3.content = ""
        
        articles = [mock_article1, mock_article2, mock_article3]
        
        results = analyzer.analyze_batch(articles)
        
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result['article_id'] == i + 1
            assert 'sentiment_label' in result
            assert 'confidence' in result

class TestSentimentGlobalInstance:
    """Test global sentiment analyzer instance management"""
    
    def test_get_sentiment_analyzer_singleton(self):
        """Test that get_sentiment_analyzer returns same instance"""
        analyzer1 = get_sentiment_analyzer()
        analyzer2 = get_sentiment_analyzer()
        
        assert analyzer1 is analyzer2  # Should be same instance
        assert isinstance(analyzer1, SentimentAnalyzer)
    
    @patch('services.nlp.src.sentiment._sentiment_analyzer', None)
    def test_get_sentiment_analyzer_creates_new(self):
        """Test that get_sentiment_analyzer creates new instance when needed"""
        analyzer = get_sentiment_analyzer()
        assert isinstance(analyzer, SentimentAnalyzer)

@pytest.mark.unit
class TestSentimentEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_analyze_very_long_text(self):
        """Test sentiment analysis with very long text"""
        analyzer = SentimentAnalyzer()
        long_text = "Medical research shows positive results. " * 1000
        
        result = analyzer.analyze_sentiment(long_text)
        
        assert result['sentiment_label'] in ['positive', 'negative', 'neutral']
        assert result['text_length'] > 10000
    
    def test_analyze_special_characters(self):
        """Test sentiment analysis with special characters and medical terms"""
        analyzer = SentimentAnalyzer()
        text = "Patient's condition improved 50% with new treatment (p<0.05)"
        
        result = analyzer.analyze_sentiment(text)
        
        assert result['sentiment_label'] in ['positive', 'negative', 'neutral']
        assert result['text_length'] > 0
    
    def test_analyze_multilingual_content(self):
        """Test sentiment analysis with mixed language content"""
        analyzer = SentimentAnalyzer()
        text = "Medical breakthrough: El tratamiento muestra resultados prometedores"
        
        result = analyzer.analyze_sentiment(text)
        
        # Should handle gracefully even with mixed languages
        assert result['sentiment_label'] in ['positive', 'negative', 'neutral']