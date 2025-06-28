"""
Sentiment Analysis Module for PreventIA News Analytics
Uses VADER sentiment analysis optimized for medical news content
"""

import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Medical news sentiment analyzer using VADER + spaCy"""
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.nlp = None
        self._load_spacy_model()
    
    def _load_spacy_model(self):
        """Load spaCy model with fallback options"""
        try:
            # Try to load English model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy English model not found. Installing...")
            # In production, model should be pre-installed
            # For now, we'll work without spaCy preprocessing
            self.nlp = None
    
    def analyze_sentiment(self, text: str, title: str = "") -> Dict[str, any]:
        """
        Analyze sentiment of medical news content
        
        Args:
            text: Article content/summary
            title: Article title (optional, for context)
            
        Returns:
            Dict with sentiment analysis results
        """
        if not text:
            return self._empty_result()
        
        # Combine title and text for better context
        full_text = f"{title} {text}" if title else text
        
        # Clean and preprocess text if spaCy is available
        if self.nlp:
            full_text = self._preprocess_text(full_text)
        
        # VADER sentiment analysis
        scores = self.analyzer.polarity_scores(full_text)
        
        # Medical news specific interpretation
        sentiment_label, confidence = self._interpret_medical_sentiment(scores)
        
        return {
            "sentiment_label": sentiment_label,
            "confidence": confidence,
            "scores": {
                "positive": scores["pos"],
                "negative": scores["neg"],
                "neutral": scores["neu"],
                "compound": scores["compound"]
            },
            "text_length": len(text),
            "processed_text_length": len(full_text)
        }
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text using spaCy for better sentiment analysis"""
        if not self.nlp:
            return text
        
        doc = self.nlp(text)
        
        # Remove stop words and keep meaningful tokens
        meaningful_tokens = [
            token.text for token in doc 
            if not token.is_stop and not token.is_punct and len(token.text) > 2
        ]
        
        return " ".join(meaningful_tokens)
    
    def _interpret_medical_sentiment(self, scores: Dict[str, float]) -> Tuple[str, float]:
        """
        Interpret VADER scores for medical news context
        Medical news tends to be more neutral, so we adjust thresholds
        """
        compound = scores["compound"]
        
        # More sensitive thresholds for medical content
        # Medical news requires more nuanced interpretation
        if compound >= 0.3:
            return "positive", abs(compound)
        elif compound <= -0.3:
            return "negative", abs(compound)
        elif compound >= 0.1:
            return "positive", abs(compound) * 0.7  # Lower confidence for borderline positive
        elif compound <= -0.1:
            return "negative", abs(compound) * 0.7  # Lower confidence for borderline negative
        else:
            return "neutral", 1 - abs(compound)
    
    def _empty_result(self) -> Dict[str, any]:
        """Return empty result for invalid input"""
        return {
            "sentiment_label": "neutral",
            "confidence": 0.0,
            "scores": {
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 1.0,
                "compound": 0.0
            },
            "text_length": 0,
            "processed_text_length": 0
        }
    
    def analyze_batch(self, articles: list) -> list:
        """Analyze sentiment for multiple articles efficiently"""
        results = []
        
        for article in articles:
            text = getattr(article, 'summary', '') or getattr(article, 'content', '')
            title = getattr(article, 'title', '')
            
            result = self.analyze_sentiment(text, title)
            result['article_id'] = getattr(article, 'id', None)
            results.append(result)
        
        return results

# Global instance for reuse
_sentiment_analyzer = None

def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get or create sentiment analyzer instance"""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer