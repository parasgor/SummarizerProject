"""
Package initialization for summarizer_project.
"""

__version__ = "1.0.0"
__author__ = "AI Team"
__description__ = "Production-grade AI Summarizer Agent with comprehensive evaluation"

from src.agent import SummarizerAgent
from src.evaluation import evaluate_summaries, EvaluationResult
from src.metrics import (
    ReadabilityMetric,
    RelevanceMetric,
    ConcisennessMetric,
    FactualAccuracyMetric,
)

__all__ = [
    "SummarizerAgent",
    "evaluate_summaries",
    "EvaluationResult",
    "ReadabilityMetric",
    "RelevanceMetric",
    "ConcisennessMetric",
    "FactualAccuracyMetric",
]
