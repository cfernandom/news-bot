from typing import Iterable

from services.decision_engine.src.engine import decide
from services.decision_engine.src.models import DecisionResult
from services.nlp.src.models import NLPResult


def decide_publications(nlp_results: Iterable[NLPResult]) -> list[DecisionResult]:
    decisions = decide(nlp_results)
    return decisions
