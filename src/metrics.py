"""
Custom metrics for text summarization evaluation.
"""

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams
from typing import List, Optional

class ReadabilityMetric(GEval):
    """
    Custom metric to evaluate the readability and grammar of generated summaries.
    
    Evaluates:
    - Grammar correctness
    - Sentence clarity
    - Overall fluency and readability
    """
    
    def __init__(
        self,
        threshold: float = 0.7,
        evaluation_params: Optional[List[LLMTestCaseParams]] = None,
        **kwargs
    ):
        """
        Initialize ReadabilityMetric.
        
        Args:
            threshold: Score threshold for PASS/FAIL (default: 0.7)
            evaluation_params: Parameters to evaluate (default: ACTUAL_OUTPUT)
        """
        if evaluation_params is None:
            evaluation_params = [LLMTestCaseParams.ACTUAL_OUTPUT]
        
        super().__init__(
            name="Readability",
            criteria="Evaluate the grammar, clarity, and overall fluency of the summary. "
                    "Consider sentence structure, vocabulary usage, and readability.",
            evaluation_params=evaluation_params,
            threshold=threshold,
            **kwargs
        )


class RelevanceMetric(GEval):
    """
    Custom metric to evaluate if the summary remains relevant to the original text.
    
    Evaluates:
    - Relevance of key points
    - Alignment with source material
    - Information accuracy
    """
    
    def __init__(
        self,
        threshold: float = 0.7,
        evaluation_params: Optional[List[LLMTestCaseParams]] = None,
        **kwargs
    ):
        """
        Initialize RelevanceMetric.
        
        Args:
            threshold: Score threshold for PASS/FAIL (default: 0.7)
            evaluation_params: Parameters to evaluate (default: ACTUAL_OUTPUT and EXPECTED_OUTPUT)
        """
        if evaluation_params is None:
            evaluation_params = [
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT
            ]
        
        super().__init__(
            name="Relevance",
            criteria="Evaluate how relevant the summary is to the original text. "
                    "Check if key points are captured and if any information is inaccurate.",
            evaluation_params=evaluation_params,
            threshold=threshold,
            **kwargs
        )


class ConcisennessMetric(GEval):
    """
    Custom metric to evaluate the conciseness of the summary.
    
    Evaluates:
    - Absence of redundancy
    - Efficient use of language
    - Appropriate length reduction
    """
    
    def __init__(
        self,
        threshold: float = 0.7,
        evaluation_params: Optional[List[LLMTestCaseParams]] = None,
        **kwargs
    ):
        """
        Initialize ConcisennessMetric.
        
        Args:
            threshold: Score threshold for PASS/FAIL (default: 0.7)
            evaluation_params: Parameters to evaluate (default: ACTUAL_OUTPUT)
        """
        if evaluation_params is None:
            evaluation_params = [LLMTestCaseParams.ACTUAL_OUTPUT]
        
        super().__init__(
            name="Conciseness",
            criteria="Evaluate the conciseness of the summary. "
                    "Check for redundancies, unnecessary details, and efficient language use. "
                    "The summary should be significantly shorter than the original while retaining key information.",
            evaluation_params=evaluation_params,
            threshold=threshold,
            **kwargs
        )


class FactualAccuracyMetric(GEval):
    """
    Custom metric to evaluate factual accuracy of the summary.
    
    Evaluates:
    - Factual correctness
    - No hallucinations or fabrications
    - Accurate representation of source material
    """
    
    def __init__(
        self,
        threshold: float = 0.7,
        evaluation_params: Optional[List[LLMTestCaseParams]] = None,
        **kwargs
    ):
        """
        Initialize FactualAccuracyMetric.
        
        Args:
            threshold: Score threshold for PASS/FAIL (default: 0.7)
            evaluation_params: Parameters to evaluate (default: ACTUAL_OUTPUT and RETRIEVAL_CONTEXT)
        """
        if evaluation_params is None:
            evaluation_params = [
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.RETRIEVAL_CONTEXT
            ]
        
        super().__init__(
            name="Factual Accuracy",
            criteria="Evaluate the factual accuracy of the summary against the source material. "
                    "Ensure no hallucinations, fabrications, or misleading statements are present.",
            evaluation_params=evaluation_params,
            threshold=threshold,
            **kwargs
        )
