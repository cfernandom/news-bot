"""
Medical Topic Classification for Breast Cancer News
Automatically categorizes articles into medical topic categories
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class MedicalTopic(Enum):
    """Medical topic categories for breast cancer news"""

    TREATMENT = "treatment"
    DIAGNOSIS = "diagnosis"
    PREVENTION = "prevention"
    RESEARCH = "research"
    SURGERY = "surgery"
    THERAPY = "therapy"
    SCREENING = "screening"
    GENETICS = "genetics"
    LIFESTYLE = "lifestyle"
    SUPPORT = "support"
    POLICY = "policy"
    GENERAL = "general"


@dataclass
class TopicResult:
    """Result of topic classification"""

    primary_topic: MedicalTopic
    confidence: float
    matched_keywords: List[str]
    topic_scores: Dict[MedicalTopic, float]


class MedicalTopicClassifier:
    """
    Rule-based medical topic classifier for breast cancer content
    Uses keyword matching with weighted scoring
    """

    def __init__(self):
        self.topic_keywords = {
            MedicalTopic.TREATMENT: {
                "high": [
                    "chemotherapy",
                    "immunotherapy",
                    "targeted therapy",
                    "treatment",
                    "therapy",
                    "medication",
                    "drug therapy",
                ],
                "medium": [
                    "treatment plan",
                    "clinical trial",
                    "protocol",
                    "regimen",
                    "combination therapy",
                ],
                "low": ["medicine", "pharmaceutical", "therapeutic"],
            },
            MedicalTopic.DIAGNOSIS: {
                "high": [
                    "diagnosis",
                    "diagnostic",
                    "biopsy",
                    "pathology",
                    "staging",
                    "grade",
                ],
                "medium": ["tumor marker", "imaging", "mri", "ct scan", "ultrasound"],
                "low": ["test result", "medical exam", "assessment"],
            },
            MedicalTopic.PREVENTION: {
                "high": ["prevention", "preventive", "risk reduction", "prophylactic"],
                "medium": ["lifestyle changes", "diet", "exercise", "healthy living"],
                "low": ["wellness", "health tips", "avoid"],
            },
            MedicalTopic.RESEARCH: {
                "high": [
                    "research",
                    "study",
                    "clinical trial",
                    "breakthrough",
                    "discovery",
                ],
                "medium": ["scientists", "researchers", "investigation", "findings"],
                "low": ["data", "analysis", "results"],
            },
            MedicalTopic.SURGERY: {
                "high": [
                    "surgery",
                    "surgical",
                    "mastectomy",
                    "lumpectomy",
                    "reconstruction",
                ],
                "medium": ["operation", "procedure", "surgeon", "operative"],
                "low": ["invasive", "minimally invasive"],
            },
            MedicalTopic.THERAPY: {
                "high": ["radiation therapy", "hormone therapy", "targeted therapy"],
                "medium": ["radiotherapy", "endocrine therapy", "adjuvant therapy"],
                "low": ["therapy", "therapeutic approach"],
            },
            MedicalTopic.SCREENING: {
                "high": ["screening", "mammogram", "mammography", "early detection"],
                "medium": ["breast exam", "self-exam", "clinical exam"],
                "low": ["checkup", "routine exam", "monitoring"],
            },
            MedicalTopic.GENETICS: {
                "high": [
                    "genetic",
                    "brca",
                    "hereditary",
                    "mutation",
                    "genetic testing",
                ],
                "medium": ["family history", "inherited", "gene", "dna"],
                "low": ["genetic counseling", "genetic risk"],
            },
            MedicalTopic.LIFESTYLE: {
                "high": ["lifestyle", "diet", "exercise", "nutrition", "weight"],
                "medium": ["physical activity", "healthy eating", "wellness"],
                "low": ["habits", "behavioral", "quality of life"],
            },
            MedicalTopic.SUPPORT: {
                "high": [
                    "support group",
                    "counseling",
                    "psychological support",
                    "patient support",
                ],
                "medium": ["emotional support", "mental health", "coping", "survivor"],
                "low": ["help", "assistance", "community"],
            },
            MedicalTopic.POLICY: {
                "high": ["policy", "healthcare policy", "insurance", "coverage"],
                "medium": ["regulation", "guidelines", "recommendations"],
                "low": ["healthcare system", "access", "cost"],
            },
        }

        # Scoring weights
        self.weights = {"high": 3.0, "medium": 2.0, "low": 1.0}

    def classify_article(
        self, title: str, summary: str, content: str = ""
    ) -> TopicResult:
        """
        Classify article into medical topic category

        Args:
            title: Article title
            summary: Article summary
            content: Full article content (optional)

        Returns:
            TopicResult with classification details
        """
        # Combine all text for analysis
        full_text = f"{title} {summary} {content}".lower()

        # Calculate scores for each topic
        topic_scores = {}
        matched_keywords = []

        for topic, keyword_groups in self.topic_keywords.items():
            score = 0.0
            topic_matches = []

            for weight_level, keywords in keyword_groups.items():
                weight = self.weights[weight_level]

                for keyword in keywords:
                    # Use word boundary matching for better accuracy
                    pattern = rf"\b{re.escape(keyword)}\b"
                    matches = len(re.findall(pattern, full_text))

                    if matches > 0:
                        score += matches * weight
                        topic_matches.append(keyword)

            topic_scores[topic] = score
            matched_keywords.extend(topic_matches)

        # Find primary topic (highest score)
        if not topic_scores or max(topic_scores.values()) == 0:
            primary_topic = MedicalTopic.GENERAL
            confidence = 0.0
        else:
            primary_topic = max(topic_scores, key=topic_scores.get)

            # Calculate confidence based on score distribution
            max_score = topic_scores[primary_topic]
            total_score = sum(topic_scores.values())
            confidence = max_score / total_score if total_score > 0 else 0.0

        return TopicResult(
            primary_topic=primary_topic,
            confidence=confidence,
            matched_keywords=list(set(matched_keywords)),
            topic_scores=topic_scores,
        )

    def get_topic_distribution(
        self, articles_data: List[Dict]
    ) -> Dict[MedicalTopic, int]:
        """
        Analyze topic distribution across multiple articles

        Args:
            articles_data: List of article dictionaries with title, summary, content

        Returns:
            Dictionary with topic counts
        """
        topic_counts = {topic: 0 for topic in MedicalTopic}

        for article in articles_data:
            result = self.classify_article(
                title=article.get("title", ""),
                summary=article.get("summary", ""),
                content=article.get("content", ""),
            )
            topic_counts[result.primary_topic] += 1

        return topic_counts


# Global classifier instance
_topic_classifier = None


def get_topic_classifier() -> MedicalTopicClassifier:
    """Get singleton topic classifier instance"""
    global _topic_classifier
    if _topic_classifier is None:
        _topic_classifier = MedicalTopicClassifier()
    return _topic_classifier
