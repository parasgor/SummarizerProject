"""
Evaluation module for summarizer outputs.
Handles metric evaluation and reporting.
"""

from typing import List, Dict, Any, Optional
from statistics import mean
from collections import defaultdict
from deepeval.metrics import (
    SummarizationMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    BiasMetric,
    ToxicityMetric,
    PromptAlignmentMetric,
)
from deepeval.test_case import LLMTestCase
from deepeval import evaluate
from tabulate import tabulate
from src.metrics import ReadabilityMetric
from src.config import (
    PASS_THRESHOLD,
    SCORE_DECIMAL_PLACES,
    TABLE_FORMAT,
)
from src.utils import setup_logger, format_score, format_percentage, get_readable_timestamp

logger = setup_logger(__name__)


class EvaluationResult:
    """
    Container for evaluation results with reporting capabilities.
    """
    
    def __init__(self, test_results: List[Any], metrics_config: Dict[str, Any]):
        """
        Initialize evaluation result.
        
        Args:
            test_results: List of test results from DeepEval
            metrics_config: Configuration used for evaluation
        """
        self.test_results = test_results
        self.metrics_config = metrics_config
        self._aggregate_data = None
        self._per_input_data = None
        logger.info(f"Created EvaluationResult with {len(test_results)} test cases")
    
    def _compute_aggregates(self) -> Dict[str, Dict[str, Any]]:
        """
        Compute aggregate metrics across all test cases.
        
        Returns:
            Dictionary with aggregated metric data
        """
        if self._aggregate_data is not None:
            return self._aggregate_data
        
        metrics_aggregates = defaultdict(lambda: {
            "scores": [],
            "passes": 0,
            "total": 0,
            "reasons": []
        })
        
        for test_result in self.test_results:
            for metric_data in getattr(test_result, "metrics_data", []):
                metric_name = metric_data.name
                metrics_aggregates[metric_name]["scores"].append(metric_data.score)
                metrics_aggregates[metric_name]["total"] += 1
                if metric_data.success:
                    metrics_aggregates[metric_name]["passes"] += 1
                if hasattr(metric_data, "reason") and metric_data.reason:
                    metrics_aggregates[metric_name]["reasons"].append(metric_data.reason)
        
        self._aggregate_data = dict(metrics_aggregates)
        return self._aggregate_data
    
    def _compute_per_input(self) -> List[Dict[str, Any]]:
        """
        Compute per-input average scores.
        
        Returns:
            List of per-input statistics
        """
        if self._per_input_data is not None:
            return self._per_input_data
        
        per_input = []
        for idx, test_result in enumerate(self.test_results, start=1):
            metrics_scores = [
                metric_data.score
                for metric_data in getattr(test_result, "metrics_data", [])
            ]
            
            if metrics_scores:
                avg_score = mean(metrics_scores)
                per_input.append({
                    "input_idx": idx,
                    "average_score": avg_score,
                    "num_metrics": len(metrics_scores),
                    "passed": avg_score >= PASS_THRESHOLD,
                })
            else:
                per_input.append({
                    "input_idx": idx,
                    "average_score": 0.0,
                    "num_metrics": 0,
                    "passed": False,
                })
        
        self._per_input_data = per_input
        return self._per_input_data
    
    def get_aggregate_scores(self) -> Dict[str, float]:
        """Get average scores per metric."""
        aggregates = self._compute_aggregates()
        return {
            name: mean(data["scores"]) if data["scores"] else 0.0
            for name, data in aggregates.items()
        }
    
    def get_pass_rates(self) -> Dict[str, float]:
        """Get pass rates per metric."""
        aggregates = self._compute_aggregates()
        return {
            name: (data["passes"] / data["total"]) if data["total"] > 0 else 0.0
            for name, data in aggregates.items()
        }
    
    def get_per_input_scores(self) -> List[Dict[str, Any]]:
        """Get per-input statistics."""
        return self._compute_per_input()
    
    def get_overall_stats(self) -> Dict[str, float]:
        """Get overall statistics across all metrics and inputs."""
        all_scores = []
        all_passed = 0
        all_total = 0
        
        for test_result in self.test_results:
            for metric_data in getattr(test_result, "metrics_data", []):
                all_scores.append(metric_data.score)
                all_total += 1
                if metric_data.success:
                    all_passed += 1
        
        return {
            "overall_average_score": mean(all_scores) if all_scores else 0.0,
            "overall_pass_rate": (all_passed / all_total) if all_total > 0 else 0.0,
            "total_metrics": all_total,
            "total_passed": all_passed,
        }
    
    def print_report(self) -> None:
        """Print formatted evaluation report."""
        print("\n" + "=" * 120)
        print("📊 SUMMARIZER EVALUATION REPORT")
        print("=" * 120)
        print(f"Generated: {get_readable_timestamp()}\n")
        
        # Aggregate metrics
        print("\n" + "-" * 120)
        print("🔍 Aggregate Metrics")
        print("-" * 120 + "\n")
        
        aggregates = self._compute_aggregates()
        aggregate_data = []
        
        for metric_name in sorted(aggregates.keys()):
            data = aggregates[metric_name]
            avg_score = mean(data["scores"]) if data["scores"] else 0.0
            pass_rate = (data["passes"] / data["total"] * 100) if data["total"] > 0 else 0.0
            
            aggregate_data.append([
                metric_name,
                format_score(avg_score),
                format_percentage(pass_rate),
                data["total"],
            ])
        
        print(tabulate(
            aggregate_data,
            headers=["Metric", "Avg Score", "Pass Rate", "Total Tests"],
            tablefmt=TABLE_FORMAT,
        ))
        
        # Per-input scores
        print("\n" + "-" * 120)
        print("💡 Per-Input Average Scores")
        print("-" * 120 + "\n")
        
        per_input = self._compute_per_input()
        per_input_data = [
            [
                f"Input #{item['input_idx']}",
                format_score(item['average_score']),
                "✓ PASS" if item['passed'] else "✗ FAIL",
            ]
            for item in per_input
        ]
        
        print(tabulate(
            per_input_data,
            headers=["Input", "Average Score", "Status"],
            tablefmt=TABLE_FORMAT,
        ))
        
        # Overall statistics
        print("\n" + "-" * 120)
        print("📈 Overall Statistics")
        print("-" * 120 + "\n")
        
        overall = self.get_overall_stats()
        stats_data = [
            ["Overall Average Score", format_score(overall["overall_average_score"])],
            ["Overall Pass Rate", format_percentage(overall["overall_pass_rate"])],
            ["Total Metrics Evaluated", overall["total_metrics"]],
            ["Total Passed", overall["total_passed"]],
        ]
        
        print(tabulate(stats_data, headers=["Metric", "Value"], tablefmt=TABLE_FORMAT))
        print("\n" + "=" * 120 + "\n")


def evaluate_summaries(
    test_data: List[Dict[str, str]],
    prompt: Optional[str] = None,
    metrics: Optional[List] = None,
) -> EvaluationResult:
    """
    Evaluate generated summaries using multiple metrics.
    
    Args:
        test_data: List of test cases with keys:
                   - text: Original text
                   - generated_summary: Generated summary
                   - expected_summary: Reference summary (optional)
                   - prompt: Summarization prompt (optional)
        prompt: Default prompt to use if not in test_data
        metrics: List of metrics to evaluate (uses defaults if None)
    
    Returns:
        EvaluationResult object with report methods
    
    Raises:
        ValueError: If test_data is invalid
    """
    if not test_data:
        raise ValueError("test_data cannot be empty")
    
    # Use default metrics if none provided
    if metrics is None:
        metrics = [
            SummarizationMetric(),
            ContextualPrecisionMetric(),
            ContextualRecallMetric(),
            BiasMetric(),
            ToxicityMetric(),
            PromptAlignmentMetric(
                prompt_instructions=prompt or "Summarize concisely."
            ),
            ReadabilityMetric(),
        ]
    
    logger.info(f"Starting evaluation of {len(test_data)} summaries")
    logger.info(f"Using {len(metrics)} metrics")
    
    test_cases = []
    for idx, item in enumerate(test_data):
        if "text" not in item or "generated_summary" not in item:
            raise ValueError(
                f"Test case {idx} missing required keys: 'text' or 'generated_summary'"
            )
        
        # Create test case
        test_case = LLMTestCase(
            input=item.get("text", ""),
            actual_output=item.get("generated_summary", ""),
            expected_output=item.get("expected_summary", ""),
            retrieval_context=[item.get("text", "")],
        )
        test_cases.append(test_case)
    
    logger.info(f"Running evaluation on {len(test_cases)} test cases")
    
    # Run evaluation
    evaluation_result = evaluate(test_cases, metrics=metrics)
    test_results = getattr(evaluation_result, "test_results", [evaluation_result])
    
    logger.info("Evaluation completed successfully")
    
    return EvaluationResult(
        test_results=test_results,
        metrics_config={
            "num_metrics": len(metrics),
            "num_test_cases": len(test_cases),
            "metrics": [getattr(m, 'name', m.__class__.__name__) for m in metrics],
        }
    )
