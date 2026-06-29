"""
Tests for custom metrics.
"""

import pytest
from src.metrics import (
    ReadabilityMetric,
    RelevanceMetric,
    ConcisennessMetric,
    FactualAccuracyMetric,
)


class TestReadabilityMetric:
    """Tests for ReadabilityMetric."""
    
    def test_readability_metric_init(self):
        """Test ReadabilityMetric initialization."""
        metric = ReadabilityMetric()
        
        assert metric.name == "Readability"
        assert metric.threshold == 0.7
        assert metric.criteria is not None
    
    def test_readability_metric_custom_threshold(self):
        """Test ReadabilityMetric with custom threshold."""
        metric = ReadabilityMetric(threshold=0.8)
        
        assert metric.threshold == 0.8


class TestRelevanceMetric:
    """Tests for RelevanceMetric."""
    
    def test_relevance_metric_init(self):
        """Test RelevanceMetric initialization."""
        metric = RelevanceMetric()
        
        assert metric.name == "Relevance"
        assert metric.threshold == 0.7
        assert metric.criteria is not None
    
    def test_relevance_metric_custom_threshold(self):
        """Test RelevanceMetric with custom threshold."""
        metric = RelevanceMetric(threshold=0.75)
        
        assert metric.threshold == 0.75


class TestConcisennessMetric:
    """Tests for ConcisennessMetric."""
    
    def test_conciseness_metric_init(self):
        """Test ConcisennessMetric initialization."""
        metric = ConcisennessMetric()
        
        assert metric.name == "Conciseness"
        assert metric.threshold == 0.7
        assert metric.criteria is not None
    
    def test_conciseness_metric_custom_threshold(self):
        """Test ConcisennessMetric with custom threshold."""
        metric = ConcisennessMetric(threshold=0.65)
        
        assert metric.threshold == 0.65


class TestFactualAccuracyMetric:
    """Tests for FactualAccuracyMetric."""
    
    def test_factual_accuracy_metric_init(self):
        """Test FactualAccuracyMetric initialization."""
        metric = FactualAccuracyMetric()
        
        assert metric.name == "Factual Accuracy"
        assert metric.threshold == 0.7
        assert metric.criteria is not None
    
    def test_factual_accuracy_metric_custom_threshold(self):
        """Test FactualAccuracyMetric with custom threshold."""
        metric = FactualAccuracyMetric(threshold=0.9)
        
        assert metric.threshold == 0.9


class TestMetricsCriteria:
    """Tests for metrics criteria content."""
    
    def test_all_metrics_have_meaningful_criteria(self):
        """Test that all metrics have meaningful criteria."""
        metrics = [
            ReadabilityMetric(),
            RelevanceMetric(),
            ConcisennessMetric(),
            FactualAccuracyMetric(),
        ]
        
        for metric in metrics:
            assert metric.criteria is not None
            assert len(metric.criteria) > 10  # Should have substantial criteria
            assert isinstance(metric.criteria, str)
    
    def test_metrics_names_are_unique(self):
        """Test that metric names are unique."""
        metrics = [
            ReadabilityMetric(),
            RelevanceMetric(),
            ConcisennessMetric(),
            FactualAccuracyMetric(),
        ]
        
        names = [m.name for m in metrics]
        assert len(names) == len(set(names))  # All unique
