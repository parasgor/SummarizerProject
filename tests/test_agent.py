"""
Tests for the SummarizerAgent.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.agent import SummarizerAgent
from src.config import MODEL, TEMPERATURE, MAX_TOKENS


class TestSummarizerAgentInit:
    """Tests for SummarizerAgent initialization."""
    
    def test_init_with_default_params(self):
        """Test initialization with default parameters."""
        agent = SummarizerAgent()
        assert agent.model == MODEL
        assert agent.temperature == TEMPERATURE
        assert agent.max_tokens == MAX_TOKENS
    
    def test_init_with_custom_params(self):
        """Test initialization with custom parameters."""
        agent = SummarizerAgent(
            model="gpt-4",
            temperature=0.5,
            max_tokens=1000,
        )
        assert agent.model == "gpt-4"
        assert agent.temperature == 0.5
        assert agent.max_tokens == 1000
    
    def test_init_sets_system_message(self):
        """Test that system message is set correctly."""
        agent = SummarizerAgent()
        assert "summarizer" in agent.system_message.lower()


class TestSummarize:
    """Tests for the summarize method."""
    
    @patch('src.agent.OpenAI')
    def test_summarize_valid_text(self, mock_openai):
        """Test summarizing valid text."""
        # Mock the OpenAI response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "This is a summary."
        mock_client.chat.completions.create.return_value = mock_response
        
        agent = SummarizerAgent()
        result = agent.summarize("This is a long text that needs to be summarized properly.")
        
        assert result == "This is a summary."
        assert mock_client.chat.completions.create.called
    
    @patch('src.agent.OpenAI')
    def test_summarize_with_custom_prompt(self, mock_openai):
        """Test summarizing with custom prompt."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Summary with custom prompt."
        mock_client.chat.completions.create.return_value = mock_response
        
        agent = SummarizerAgent()
        custom_prompt = "Summarize in one sentence."
        result = agent.summarize("Long text here.", prompt=custom_prompt)
        
        assert result == "Summary with custom prompt."
        # Verify custom prompt was used
        call_args = mock_client.chat.completions.create.call_args
        assert custom_prompt in call_args[1]["messages"][1]["content"]
    
    def test_summarize_invalid_text_too_short(self):
        """Test that short text is rejected."""
        agent = SummarizerAgent()
        
        with pytest.raises(ValueError, match="Invalid text"):
            agent.summarize("short")
    
    def test_summarize_invalid_text_type(self):
        """Test that non-string input is rejected."""
        agent = SummarizerAgent()
        
        with pytest.raises(ValueError, match="Invalid text"):
            agent.summarize(123)


class TestSummarizeBatch:
    """Tests for the summarize_batch method."""
    
    @patch('src.agent.OpenAI')
    def test_summarize_batch_multiple_texts(self, mock_openai):
        """Test batch summarization of multiple texts."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        summaries = ["Summary 1.", "Summary 2.", "Summary 3."]
        mock_response_list = []
        for summary in summaries:
            mock_response = MagicMock()
            mock_response.choices[0].message.content = summary
            mock_response_list.append(mock_response)
        
        mock_client.chat.completions.create.side_effect = mock_response_list
        
        agent = SummarizerAgent()
        texts = [
            "This is the first text that needs summarization.",
            "This is the second text that needs summarization.",
            "This is the third text that needs summarization.",
        ]
        
        results = agent.summarize_batch(texts, delay=0)
        
        assert len(results) == 3
        assert results == summaries
    
    def test_summarize_batch_invalid_text(self):
        """Test that batch rejects invalid texts."""
        agent = SummarizerAgent()
        
        texts = [
            "This is a valid text for summarization.",
            "short",  # Invalid
        ]
        
        with pytest.raises(ValueError, match="Invalid texts"):
            agent.summarize_batch(texts)
    
    def test_summarize_batch_empty_list(self):
        """Test batch with empty list."""
        agent = SummarizerAgent()
        
        with pytest.raises(ValueError):
            agent.summarize_batch([])


class TestPromptManagement:
    """Tests for prompt management methods."""
    
    def test_set_prompt(self):
        """Test setting custom prompt."""
        agent = SummarizerAgent()
        new_prompt = "Summarize in bullet points."
        
        agent.set_prompt(new_prompt)
        
        assert agent.summarization_prompt == new_prompt
    
    def test_set_prompt_invalid(self):
        """Test that invalid prompt is rejected."""
        agent = SummarizerAgent()
        
        with pytest.raises(ValueError, match="non-empty string"):
            agent.set_prompt("")
        
        with pytest.raises(ValueError, match="non-empty string"):
            agent.set_prompt(None)
    
    def test_set_system_message(self):
        """Test setting custom system message."""
        agent = SummarizerAgent()
        new_message = "You are an expert summarizer."
        
        agent.set_system_message(new_message)
        
        assert agent.system_message == new_message


class TestConfiguration:
    """Tests for configuration management."""
    
    def test_get_config(self):
        """Test getting current configuration."""
        agent = SummarizerAgent()
        config = agent.get_config()
        
        assert "model" in config
        assert "temperature" in config
        assert "max_tokens" in config
        assert config["model"] == MODEL
    
    def test_update_config(self):
        """Test updating configuration."""
        agent = SummarizerAgent()
        
        agent.update_config(
            temperature=0.3,
            max_tokens=200,
        )
        
        assert agent.temperature == 0.3
        assert agent.max_tokens == 200
    
    def test_update_config_invalid_param(self):
        """Test that invalid parameters are rejected."""
        agent = SummarizerAgent()
        
        with pytest.raises(ValueError, match="Invalid parameters"):
            agent.update_config(invalid_param=123)
