# NLP Service API Documentation

## Overview

The PreventIA NLP service provides specialized text analysis for medical content, including sentiment analysis, keyword extraction, and relevance scoring. This service is optimized for breast cancer news articles.

## Architecture

```
NLP Service
├── SentimentAnalyzer    # VADER + spaCy sentiment analysis
├── NLPAnalyzer         # Keyword extraction + relevance scoring
└── Models              # Data structures and response types
```

## Core Components

### 1. Sentiment Analysis

#### SentimentAnalyzer Class

**Location**: `services/nlp/src/sentiment.py`

**Description**: Medical-specialized sentiment analyzer using VADER with adjusted thresholds for medical content.

##### Key Methods

```python
class SentimentAnalyzer:
    def analyze_sentiment(text: str, title: str = "") -> Dict[str, any]
```

**Parameters**:
- `text` (str): Main article content
- `title` (str, optional): Article title for combined analysis

**Returns**:
```python
{
    "sentiment_label": str,      # "positive", "negative", "neutral"
    "confidence": float,         # 0.0-1.0 confidence score
    "detailed_scores": {
        "compound": float,       # -1.0 to 1.0 overall sentiment
        "positive": float,       # 0.0-1.0 positive intensity
        "negative": float,       # 0.0-1.0 negative intensity  
        "neutral": float         # 0.0-1.0 neutral intensity
    }
}
```

**Medical Content Thresholds**:
- **Strong sentiment**: compound >= ±0.3
- **Moderate sentiment**: compound >= ±0.1 (confidence reduced 30%)
- **Neutral**: compound < ±0.1

##### Batch Processing

```python
def analyze_batch(articles: List[Dict]) -> List[Dict]
```

**Parameters**:
- `articles`: List of articles with `title` and `content` fields

**Returns**: List of sentiment results with same individual structure

**Performance**: ~2 articles/second, optimized for batch processing

### 2. NLP Analysis Pipeline

#### NLPAnalyzer Class

**Location**: `services/nlp/src/analyzer.py`

**Description**: Complete NLP analysis pipeline including keywords + sentiment.

##### Key Methods

```python
class NLPAnalyzer:
    def analyze_article(article: Article) -> NLPResult
```

**Parameters**:
- `article` (Article): Article object with `title`, `content`, `url` fields

**Returns**: `NLPResult` object with complete analysis

### 3. Data Models

#### SentimentResult

**Location**: `services/nlp/src/models.py`

```python
@dataclass
class SentimentResult:
    sentiment_label: str         # Classification label
    confidence: float           # Confidence score (0-1)
    detailed_scores: Dict       # VADER detailed breakdown
    processing_time: float      # Analysis duration in seconds
```

#### NLPResult (Enhanced)

```python
@dataclass  
class NLPResult:
    article: Article
    is_relevant: bool
    matched_keywords: List[str]
    relevance_score: float
    sentiment_data: Optional[SentimentResult] = None  # New in Phase 2
```

## API Usage Examples

### Basic Sentiment Analysis

```python
from services.nlp.src.sentiment import sentiment_analyzer

# Single article analysis
text = "New breakthrough treatment shows promising results..."
result = sentiment_analyzer.analyze_sentiment(text)

print(f"Sentiment: {result['sentiment_label']}")
print(f"Confidence: {result['confidence']:.3f}")
print(f"Compound Score: {result['detailed_scores']['compound']:.3f}")
```

### Batch Processing

```python
# Process multiple articles
articles = [
    {"title": "Cancer Research Update", "content": "..."},
    {"title": "Treatment Success Story", "content": "..."}
]

results = sentiment_analyzer.analyze_batch(articles)
for i, result in enumerate(results):
    print(f"Article {i+1}: {result['sentiment_label']} ({result['confidence']:.3f})")
```

### Full NLP Pipeline

```python
from services.nlp.src.analyzer import NLPAnalyzer

nlp_analyzer = NLPAnalyzer()
article = Article(title="...", content="...", url="...")

# Complete analysis: keywords + sentiment
result = nlp_analyzer.analyze_article(article)

print(f"Relevant: {result.is_relevant}")
print(f"Keywords: {result.matched_keywords}")
print(f"Sentiment: {result.sentiment_data.sentiment_label}")
```

## Configuration

### Environment Variables

```bash
# Optional: Enable spaCy preprocessing (adds 30% processing time, +15% accuracy)
NLP_USE_SPACY_PREPROCESSING=false

# Sentiment analysis thresholds (medical content optimized)
SENTIMENT_STRONG_THRESHOLD=0.3
SENTIMENT_MODERATE_THRESHOLD=0.1
```

### Dependencies

```python
# Core NLP dependencies (verified versions)
vaderSentiment==3.3.2
spacy==3.8.7
pandas==2.2.3
numpy==2.2.1
```

## Performance Characteristics

### Sentiment Analysis Benchmarks

| Operation | Time | Memory | Throughput |
|-----------|------|--------|------------|
| Single article | ~0.5s | <10MB | - |
| Batch (50 articles) | ~25s | <50MB | ~2 articles/s |
| With spaCy preprocessing | +30% time | +20% memory | +15% accuracy |

### Scaling Considerations

- **Memory usage**: Linear with batch size (~1MB per 100 articles)
- **CPU intensive**: VADER processing is CPU-bound
- **Concurrency**: Thread-safe for read operations
- **Caching**: Global analyzer instance reused for efficiency

## Error Handling

### Common Exceptions

```python
# Empty content handling
if not text or not text.strip():
    return {
        "sentiment_label": "neutral",
        "confidence": 0.0,
        "detailed_scores": {"compound": 0.0, "positive": 0.0, "negative": 0.0, "neutral": 1.0}
    }

# spaCy processing errors (fallback to raw text)
try:
    processed_text = self._preprocess_with_spacy(text)
except Exception:
    processed_text = text  # Fallback to original
```

### Error Response Format

```python
{
    "error": True,
    "error_type": "ProcessingError",
    "message": "Unable to process article content",
    "fallback_result": {
        "sentiment_label": "neutral",
        "confidence": 0.0
    }
}
```

## Testing

### Test Coverage

- **Unit tests**: 14 tests covering core sentiment analysis
- **Integration tests**: 6 tests for NLP pipeline integration
- **Performance tests**: Batch processing benchmarks
- **Edge cases**: Empty content, malformed text, special characters

### Running Tests

```bash
cd tests

# Sentiment analysis unit tests
pytest unit/test_nlp/test_sentiment.py -v

# Integration tests with database
pytest integration/test_nlp_pipeline.py -v

# Coverage report
pytest --cov=../services/nlp --cov-report=html
```

## Integration Guidelines

### Database Integration

```python
# Update article with sentiment data
async with db_manager.get_session() as session:
    article = await session.get(Article, article_id)
    
    sentiment_result = sentiment_analyzer.analyze_sentiment(
        article.content, article.title
    )
    
    article.sentiment_label = sentiment_result["sentiment_label"]
    article.sentiment_score = sentiment_result["detailed_scores"]["compound"]
    article.processing_status = "analyzed"
    
    await session.commit()
```

### Future REST API Integration

```python
# Planned FastAPI endpoints
@app.post("/api/nlp/sentiment")
async def analyze_sentiment(request: SentimentRequest):
    result = sentiment_analyzer.analyze_sentiment(
        request.text, request.title
    )
    return SentimentResponse(**result)

@app.post("/api/nlp/batch-sentiment") 
async def batch_sentiment(request: BatchSentimentRequest):
    results = sentiment_analyzer.analyze_batch(request.articles)
    return BatchSentimentResponse(results=results)
```

## Medical Content Specialization

### Why Medical Thresholds?

**Standard VADER thresholds**: ±0.05 (very sensitive)
**Medical content thresholds**: ±0.3 (conservative)

**Rationale**:
- Medical content tends toward neutral language
- Clinical terminology can trigger false sentiment
- Conservative thresholds reduce false positives
- Better accuracy for medical domain

### Threshold Tuning

```python
# Current medical-optimized thresholds
STRONG_SENTIMENT = 0.3      # Clear positive/negative sentiment
MODERATE_SENTIMENT = 0.1    # Mild sentiment (reduced confidence)
NEUTRAL_RANGE = 0.1         # Conservative neutral classification
```

**Validation results** (56 articles):
- Negative: 71% (40 articles) - Expected for cancer news
- Positive: 27% (15 articles) - Treatment breakthroughs
- Neutral: 2% (1 article) - Purely factual content

## Troubleshooting

### Common Issues

1. **Slow batch processing**
   - Solution: Use batch methods instead of individual calls
   - Disable spaCy preprocessing if not needed

2. **Memory usage high**
   - Solution: Process in smaller batches (25-50 articles)
   - Clear analyzer cache periodically

3. **Sentiment accuracy low**
   - Check article content quality
   - Verify medical content thresholds are appropriate
   - Consider enabling spaCy preprocessing

### Debug Mode

```python
# Enable detailed logging for troubleshooting
import logging
logging.getLogger('nlp.sentiment').setLevel(logging.DEBUG)

# Analyze with debug info
result = sentiment_analyzer.analyze_sentiment(text, debug=True)
```

## References

- [VADER Sentiment Analysis Paper](https://ojs.aaai.org/index.php/ICWSM/article/view/14550)
- [spaCy Documentation](https://spacy.io/usage)
- [ADR-004: Sentiment Analysis Decision](../../decisions/ADR-004-nlp-sentiment-analysis.md)
- [Phase 2 Implementation Results](../../implementation/phase-2-nlp-analytics.md)

---
**Last Updated**: 2025-06-28  
**API Version**: 2.0 (Phase 2)  
**Maintainer**: PreventIA Analytics Team