from typing import Iterable

from services.decision_engine.src.config import PUBLISH_THRESHOLD
from services.decision_engine.src.models import DecisionResult
from services.nlp.src.models import NLPResult


def decide(nlp_results: Iterable[NLPResult]) -> list[DecisionResult]:
    """
    Aplica la regla de decisión a cada resultado NLP.

    - Publicar si score ≥ PUBLISH_THRESHOLD.
    - Todas las decisiones se devuelven junto con la razón.
    """
    decisions = []
    for n in nlp_results:
        dr = DecisionResult.from_nlp(n, PUBLISH_THRESHOLD)
        decisions.append(dr)
    return decisions
