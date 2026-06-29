"""
Tests for the evaluation module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.evaluation import evaluate_summaries, EvaluationResult
from statistics import mean


class TestEvaluationResult:
    """Tests for EvaluationResult class."""
    
    def create_mock_test_result(self, metric_scores: dict) -> Mock:
        """Helper to create a mock test result."""
        mock_result = Mock()
        mock_metrics_data = []
        
        for metric_name, score in metric_scores.items():
            metric = Mock()
            metric.name = metric_name
            metric.score = score
            metric.success = score >= 0.7
            metric.reason = f"Test reason for {metric_name}"
            mock_metrics_data.append(metric)
        
        mock_result.metrics_data = mock_metrics_data
        return mock_result
    
    def test_compute_aggregates(self):
        """Test aggregate computation."""
        test_results = [
            self.create_mock_test_result({
                "Metric1": 0.8,
                "Metric2": 0.6,
            }),
            self.create_mock_test_result({
                "Metric1": 0.9,
                "Metric2": 0.7,
            }),
        ]
        
        result = EvaluationResult(test_results, {})
        aggregates = result._compute_aggregates()
        
        assert "Metric1" in aggregates
        assert "Metric2" in aggregates
        assert len(aggregates["Metric1"]["scores"]) == 2
    
    def test_get_aggregate_scores(self):
        """Test getting aggregate scores."""
        test_results = [
            self.create_mock_test_result({"Metric1": 0.8}),
            self.create_mock_test_result({"Metric1": 0.6}),
        ]
        
        result = EvaluationResult(test_results, {})
        scores = result.get_aggregate_scores()
        
        assert scores["Metric1"] == 0.7  # (0.8 + 0.6) / 2
    
    def test_get_pass_rates(self):
        """Test getting pass rates."""
        test_results = [
            self.create_mock_test_result({"Metric1": 0.8}),  # Pass
            self.create_mock_test_result({"Metric1": 0.6}),  # Fail (< 0.7)
        ]
        
        result = EvaluationResult(test_results, {})
        pass_rates = result.get_pass_rates()
        
        assert pass_rates["Metric1"] == 0.5  # 1 pass out of 2
    
    def test_get_per_input_scores(self):
        """Test getting per-input scores."""
        test_results = [
            self.create_mock_test_result({"Metric1": 0.8, "Metric2": 0.9}),
            self.create_mock_test_result({"Metric1": 0.6, "Metric2": 0.7}),
        ]
        
        result = EvaluationResult(test_results, {})
        per_input = result.get_per_input_scores()
        
        assert len(per_input) == 2
        assert per_input[0]["input_idx"] == 1
        assert per_input[0]["average_score"] == 0.85  # (0.8 + 0.9) / 2
        assert per_input[0]["passed"] == True  # >= 0.7
        
        assert per_input[1]["average_score"] == 0.65  # (0.6 + 0.7) / 2
        assert per_input[1]["passed"] == False  # < 0.7
    
    def test_get_overall_stats(self):
        """Test getting overall statistics."""
        test_results = [
            self.create_mock_test_result({"Metric1": 0.8, "Metric2": 0.9}),
            self.create_mock_test_result({"Metric1": 0.6, "Metric2": 0.7}),
        ]
        
        result = EvaluationResult(test_results, {})
        stats = result.get_overall_stats()
        
        assert "overall_average_score" in stats
        assert "overall_pass_rate" in stats
        assert "total_metrics" in stats
        assert stats["total_metrics"] == 4  # 2 inputs × 2 metrics
    
    def test_print_report(self, capsys):
        """Test report printing."""
        test_results = [
            self.create_mock_test_result({"Metric1": 0.8}),
        ]
        
        result = EvaluationResult(test_results, {})
        result.print_report()
        
        captured = capsys.readouterr()
        assert "EVALUATION REPORT" in captured.out
        assert "Metric1" in captured.out


class TestEvaluateSummaries:
    """Tests for evaluate_summaries function."""
    
    def test_evaluate_summaries_valid_input(self):
        """Test evaluation with valid input."""
        test_data = [
            {
                "text": "This is a long text about machine learning that needs to be summarized.",
                "generated_summary": "This is about machine learning.",
                "expected_summary": "Machine learning overview.",
            }
        ]
        
        with patch('src.evaluation.evaluate') as mock_evaluate:
            mock_result = Mock()
            mock_result.test_results = [Mock()]
            mock_result.test_results[0].metrics_data = []
            mock_evaluate.return_value = mock_result
            
            result = evaluate_summaries(test_data)
            
            assert isinstance(result, EvaluationResult)
            assert mock_evaluate.called
    
    def test_evaluate_summaries_missing_required_keys(self):
        """Test that missing required keys are caught."""
        test_data = [
            {
                "text": "Some text here.",
                # Missing "generated_summary"
            }
        ]
        
        with pytest.raises(ValueError, match="required keys"):
            evaluate_summaries(test_data)
    
    def test_evaluate_summaries_empty_input(self):
        """Test that empty input is rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            evaluate_summaries([])
    
    def test_evaluate_summaries_default_metrics(self):
        """Test that default metrics are used when none provided."""
        test_data = [
            {
                "text": "This is a long text that needs summarization here.",
                "generated_summary": "This is a summary.",
            }
        ]
        
        with patch('src.evaluation.evaluate') as mock_evaluate:
            mock_result = Mock()
            mock_result.test_results = [Mock()]
            mock_result.test_results[0].metrics_data = []
            mock_evaluate.return_value = mock_result
            
            evaluate_summaries(test_data)
            
            # Check that metrics were passed
            call_args = mock_evaluate.call_args
            metrics = call_args[1]["metrics"]
            assert len(metrics) > 0
    
    def test_evaluate_summaries_custom_metrics(self):
        """Test evaluation with custom metrics."""
        test_data = [
            {
                "text": "This is a long text that needs summarization here.",
                "generated_summary": "This is a summary.",
            }
        ]
        
        custom_metrics = []  # Empty list of custom metrics
        
        with patch('src.evaluation.evaluate') as mock_evaluate:
            mock_result = Mock()
            mock_result.test_results = [Mock()]
            mock_result.test_results[0].metrics_data = []
            mock_evaluate.return_value = mock_result
            
            evaluate_summaries(test_data, metrics=custom_metrics)
            
            # Check that custom metrics were used
            call_args = mock_evaluate.call_args
            metrics = call_args[1]["metrics"]
            assert metrics == custom_metrics
    
    def test_evaluate_summaries_with_prompt(self):
        """Test evaluation with custom prompt."""
        test_data = [
            {
                "text": "This is a long text that needs summarization here.",
                "generated_summary": "This is a summary.",
            }
        ]
        
        custom_prompt = "Summarize in 2 sentences."
        
        with patch('src.evaluation.evaluate') as mock_evaluate:
            mock_result = Mock()
            mock_result.test_results = [Mock()]
            mock_result.test_results[0].metrics_data = []
            mock_evaluate.return_value = mock_result
            
            evaluate_summaries(test_data, prompt=custom_prompt)
            
            assert mock_evaluate.called
