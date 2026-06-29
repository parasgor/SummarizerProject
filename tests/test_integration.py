"""
Integration tests for the Summarizer project.
"""

import pytest
import os
from unittest.mock import patch, Mock
from src.agent import SummarizerAgent
from src.evaluation import evaluate_summaries
from src.utils import validate_text, load_json_data, save_json_data


class TestIntegrationSummarizeAndEvaluate:
    """Integration tests for summarization and evaluation workflow."""
    
    @patch('src.agent.OpenAI')
    @patch('src.evaluation.evaluate')
    def test_complete_workflow(self, mock_evaluate, mock_openai):
        """Test complete workflow from summarization to evaluation."""
        # Setup mocks
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock summarization response
        mock_response = Mock()
        mock_response.choices[0].message.content = "AI is transforming industries."
        mock_client.chat.completions.create.return_value = mock_response
        
        # Mock evaluation response
        mock_eval_result = Mock()
        mock_eval_result.test_results = [Mock()]
        mock_eval_result.test_results[0].metrics_data = []
        mock_evaluate.return_value = mock_eval_result
        
        # Run workflow
        agent = SummarizerAgent()
        
        text = "Artificial intelligence is transforming industries across the world."
        summary = agent.summarize(text)
        
        test_data = [
            {
                "text": text,
                "generated_summary": summary,
                "expected_summary": "AI is changing industries.",
            }
        ]
        
        result = evaluate_summaries(test_data)
        
        assert summary == "AI is transforming industries."
        assert result is not None
    
    @patch('src.agent.OpenAI')
    def test_batch_summarization_workflow(self, mock_openai):
        """Test batch summarization workflow."""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        summaries = ["Summary 1.", "Summary 2.", "Summary 3."]
        mock_responses = []
        for summary in summaries:
            mock_response = Mock()
            mock_response.choices[0].message.content = summary
            mock_responses.append(mock_response)
        
        mock_client.chat.completions.create.side_effect = mock_responses
        
        agent = SummarizerAgent()
        texts = [
            "This is text 1 that needs summarization here.",
            "This is text 2 that needs summarization here.",
            "This is text 3 that needs summarization here.",
        ]
        
        results = agent.summarize_batch(texts, delay=0)
        
        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)


class TestIntegrationUtilities:
    """Integration tests for utility functions."""
    
    def test_text_validation_workflow(self):
        """Test text validation in context."""
        agent = SummarizerAgent()
        
        # Valid text
        valid_text = "This is a valid text for summarization that is long enough."
        assert validate_text(valid_text)
        
        # Invalid texts
        assert not validate_text("")
        assert not validate_text("short")
        assert not validate_text(None)
    
    def test_json_file_operations(self, tmp_path):
        """Test JSON file operations."""
        test_file = tmp_path / "test.json"
        
        test_data = {
            "text": "Sample text for testing.",
            "expected_summary": "Sample summary.",
        }
        
        # Save
        save_json_data(test_data, str(test_file))
        assert test_file.exists()
        
        # Load
        loaded_data = load_json_data(str(test_file))
        assert loaded_data == test_data
    
    def test_json_load_nonexistent_file(self):
        """Test that loading nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            load_json_data("/nonexistent/path/file.json")


class TestConfigurationIntegration:
    """Integration tests for configuration."""
    
    def test_agent_config_persistence(self):
        """Test that agent configuration persists across calls."""
        agent = SummarizerAgent()
        
        custom_prompt = "Summarize in bullet points."
        agent.set_prompt(custom_prompt)
        
        config = agent.get_config()
        assert config["summarization_prompt"] == custom_prompt
    
    def test_multiple_agent_instances(self):
        """Test that multiple agent instances maintain separate configs."""
        agent1 = SummarizerAgent(temperature=0.5)
        agent2 = SummarizerAgent(temperature=0.9)
        
        assert agent1.temperature == 0.5
        assert agent2.temperature == 0.9
        
        agent1.set_prompt("Prompt 1")
        agent2.set_prompt("Prompt 2")
        
        assert agent1.get_config()["summarization_prompt"] == "Prompt 1"
        assert agent2.get_config()["summarization_prompt"] == "Prompt 2"


class TestErrorHandling:
    """Integration tests for error handling."""
    
    @patch('src.agent.OpenAI')
    def test_api_error_handling(self, mock_openai):
        """Test handling of API errors."""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Simulate API error
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        agent = SummarizerAgent()
        
        with pytest.raises(Exception, match="API Error"):
            agent.summarize("This is a long text that needs summarization here.")
    
    def test_invalid_configuration(self):
        """Test invalid configuration handling."""
        agent = SummarizerAgent()
        
        # Try to update with invalid parameter
        with pytest.raises(ValueError):
            agent.update_config(nonexistent_param="value")
        
        # Agent should still be usable
        config = agent.get_config()
        assert config is not None
