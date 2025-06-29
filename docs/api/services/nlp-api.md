# NLP Service API Documentation

---
**Document Metadata**
- **Version**: 2.0
- **Last Updated**: 2025-06-28
- **Maintainer**: Technical Team
- **Category**: API Documentation
- **Priority**: High
- **Status**: Approved
- **Language**: English (Technical Standard)
---

## Overview

The PreventIA NLP service provides specialized text analysis for medical content, including sentiment analysis, topic classification, keyword extraction, and relevance scoring. This service is optimized for breast cancer news articles with 106 articles successfully processed.

## Architecture

```
NLP Service
├── SentimentAnalyzer      # VADER + spaCy sentiment analysis
├── TopicClassifier        # Medical topic categorization (10 categories)
├── NLPAnalyzer           # Keyword extraction + relevance scoring
└── Models                # Data structures and response types
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

### 3. Topic Classification

#### MedicalTopicClassifier Class

**Location**: `services/nlp/src/topic_classifier.py`

**Description**: Rule-based medical topic classifier that categorizes breast cancer articles into 10 medical topic categories using weighted keyword matching.

##### Medical Topic Categories

```python
class MedicalTopic(Enum):
    TREATMENT = "treatment"      # 36.8% of articles
    RESEARCH = "research"        # 17.9% of articles  
    GENERAL = "general"          # 17.9% of articles
    SURGERY = "surgery"          # 11.3% of articles
    LIFESTYLE = "lifestyle"      # 3.8% of articles
    GENETICS = "genetics"        # 3.8% of articles
    DIAGNOSIS = "diagnosis"      # 3.8% of articles
    SCREENING = "screening"      # 2.8% of articles
    SUPPORT = "support"          # 0.9% of articles
    POLICY = "policy"            # 0.9% of articles
```

##### Key Methods

```python
class MedicalTopicClassifier:
    def classify_article(title: str, summary: str, content: str = "") -> TopicResult
```

**Parameters**:
- `title` (str): Article title
- `summary` (str): Article summary/description
- `content` (str, optional): Full article content

**Returns**:
```python
@dataclass
class TopicResult:
    primary_topic: MedicalTopic      # Highest scoring topic
    confidence: float                # 0.0-1.0 confidence score
    matched_keywords: List[str]      # Keywords that matched
    topic_scores: Dict[MedicalTopic, float]  # All topic scores
```

##### Keyword Weighting System

```python
# Scoring weights for keyword importance
weights = {
    "high": 3.0,      # Core medical terms
    "medium": 2.0,    # Related medical terms
    "low": 1.0        # General medical terms
}
```

**Example Classification**:
```python
from services.nlp.src.topic_classifier import get_topic_classifier

classifier = get_topic_classifier()
result = classifier.classify_article(
    title="New Chemotherapy Protocol Shows Promise",
    summary="Clinical trial demonstrates improved outcomes...",
    content="Researchers tested combination therapy..."
)

# Returns:
# TopicResult(
#     primary_topic=MedicalTopic.TREATMENT,
#     confidence=0.755,
#     matched_keywords=["chemotherapy", "clinical trial", "therapy"],
#     topic_scores={TREATMENT: 12.0, RESEARCH: 6.0, ...}
# )
```

##### Batch Processing

```python
def get_topic_distribution(articles_data: List[Dict]) -> Dict[MedicalTopic, int]
```

**Performance**: Processes 106 articles in ~30 seconds with 100% success rate

##### Production Usage

```bash
# Batch classify all articles without topic classification
python scripts/batch_topic_classification.py

# Expected output:
# ✅ 106/106 articles classified
# ✅ 10 medical topic categories
# ✅ Average confidence: 75.5% (treatment), 88.3% (surgery)
```

### 4. Data Models

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

#### 1. Sentiment Analysis Errors

**Problem**: `ModuleNotFoundError: No module named 'vaderSentiment'`
**Cause**: Missing dependencies
**Solution**:
```bash
# Install missing dependencies
pip install vaderSentiment spacy

# Download spaCy model
python -m spacy download en_core_web_sm
```

**Problem**: Incorrect sentiment classification for medical content
**Cause**: Using wrong thresholds or preprocessing
**Solution**:
```python
# Check thresholds are medical-optimized
analyzer = get_sentiment_analyzer()
# Should use ±0.3 thresholds, not ±0.05 standard

# Verify medical content adjustment
result = analyzer.analyze_sentiment("Cancer treatment breakthrough shows promise")
print(f"Compound score: {result['detailed_scores']['compound']}")
```

#### 2. Performance Issues

**Problem**: Slow batch processing (>5s per article)
**Causes**: 
- spaCy preprocessing enabled unnecessarily
- Large batch sizes
- Memory limitations

**Solutions**:
```python
# Disable spaCy for better performance
analyzer = SentimentAnalyzer(use_spacy=False)

# Use optimal batch size
batch_size = 25  # Instead of 100+
results = analyzer.analyze_batch(articles[:batch_size])

# Monitor memory usage
import psutil
print(f"Memory usage: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB")
```

**Problem**: Memory usage growing during batch processing
**Cause**: Memory leaks in long-running processes
**Solution**:
```python
# Process in chunks and clear cache
for chunk in chunks(articles, 50):
    results = analyzer.analyze_batch(chunk)
    # Process results
    results = None  # Clear reference
    gc.collect()    # Force garbage collection
```

#### 3. Integration Issues

**Problem**: Database connection errors during NLP processing
**Cause**: Connection pool exhaustion or timeout
**Solution**:
```python
# Use proper connection management
async with db_manager.get_session() as session:
    try:
        # Process articles
        result = analyze_article(article)
        # Update database
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Processing failed: {e}")
```

**Problem**: Inconsistent results across API calls
**Cause**: Different analyzer instances or configuration
**Solution**:
```python
# Use singleton pattern for consistency
analyzer = get_sentiment_analyzer()  # Global instance
# Instead of creating new instances each time
```

### Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `VADER lexicon not found` | Missing VADER data | `pip install vaderSentiment` |
| `spaCy model not found` | Missing language model | `python -m spacy download en_core_web_sm` |
| `Empty text provided` | No content to analyze | Validate input before processing |
| `Database connection failed` | DB unavailable | Check connection and retry |
| `Memory error` | Batch too large | Reduce batch size to 25-50 |

### Debug Mode

```python
# Enable detailed logging for troubleshooting
import logging
logging.basicConfig(level=logging.DEBUG)

# Create logger for NLP components
logger = logging.getLogger('nlp.sentiment')
logger.setLevel(logging.DEBUG)

# Analyze with debug info
result = sentiment_analyzer.analyze_sentiment(text, title="Debug Test")
logger.debug(f"Analysis result: {result}")

# Check processing time
import time
start = time.time()
result = sentiment_analyzer.analyze_sentiment(text)
processing_time = time.time() - start
logger.debug(f"Processing took {processing_time:.3f}s")
```

### Performance Benchmarking

```python
# Benchmark different configurations
import time

def benchmark_sentiment_analysis():
    test_texts = ["Medical breakthrough in cancer treatment..."] * 10
    
    # Test with spaCy preprocessing
    start = time.time()
    analyzer_spacy = SentimentAnalyzer(use_spacy=True)
    for text in test_texts:
        analyzer_spacy.analyze_sentiment(text)
    spacy_time = time.time() - start
    
    # Test without spaCy preprocessing
    start = time.time()
    analyzer_no_spacy = SentimentAnalyzer(use_spacy=False)
    for text in test_texts:
        analyzer_no_spacy.analyze_sentiment(text)
    no_spacy_time = time.time() - start
    
    print(f"With spaCy: {spacy_time:.3f}s")
    print(f"Without spaCy: {no_spacy_time:.3f}s")
    print(f"SpaCy overhead: {(spacy_time/no_spacy_time - 1)*100:.1f}%")

# Run benchmark
benchmark_sentiment_analysis()
```

### FAQ

#### Configuration Questions

**Q: Should I enable spaCy preprocessing?**
A: Only if accuracy is critical and you can accept 30% slower processing. For batch operations, usually not needed.

**Q: What batch size should I use?**
A: 25-50 articles for optimal memory/performance balance. Adjust based on available RAM.

**Q: How do I handle different languages?**
A: Currently optimized for English. For Spanish content, consider using language-specific VADER models.

#### Accuracy Questions

**Q: Why do some medical articles get classified as negative when they're neutral?**
A: Medical content naturally trends negative due to terminology. This is expected and accounted for in our thresholds.

**Q: How can I improve sentiment accuracy?**
A: Enable spaCy preprocessing, verify content quality, and ensure you're using medical-optimized thresholds (±0.3).

**Q: Can I customize the sentiment thresholds?**
A: Yes, but use caution. Medical content requires conservative thresholds to avoid false classifications.

## References

- [VADER Sentiment Analysis Paper](https://ojs.aaai.org/index.php/ICWSM/article/view/14550)
- [spaCy Documentation](https://spacy.io/usage)
- [ADR-004: Sentiment Analysis Decision](../../decisions/ADR-004-nlp-sentiment-analysis.md)
- [Phase 2 Implementation Results](../../implementation/phase-2-nlp-analytics.md)

---
**Last Updated**: 2025-06-28  
**API Version**: 2.0 (Phase 2)  
**Maintainer**: PreventIA Analytics Team