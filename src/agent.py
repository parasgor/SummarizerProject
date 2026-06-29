"""
Core Summarizer Agent implementation.
Handles text summarization using OpenAI's GPT models.
"""

import time
from typing import List, Optional
from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    TOP_P,
    DEFAULT_SUMMARIZATION_PROMPT,
    SYSTEM_MESSAGE,
    BATCH_REQUEST_DELAY,
)
from src.utils import setup_logger, validate_text

logger = setup_logger(__name__)


class SummarizerAgent:
    """
    AI-powered text summarizer using OpenAI's GPT models.
    
    Features:
    - Single text summarization
    - Batch processing
    - Custom prompts
    - Configurable model parameters
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = MODEL,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        top_p: float = TOP_P,
        system_message: str = SYSTEM_MESSAGE,
    ):
        """
        Initialize the SummarizerAgent.
        
        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
            model: Model to use (default: gpt-4o-mini)
            temperature: Temperature for generation (default: 0.7)
            max_tokens: Maximum tokens in response (default: 500)
            top_p: Top P for nucleus sampling (default: 0.95)
            system_message: System prompt for the model (default: professional summarizer)
        """
        self.client = OpenAI(api_key=api_key or OPENAI_API_KEY)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.system_message = system_message
        self.summarization_prompt = DEFAULT_SUMMARIZATION_PROMPT
        
        logger.info(f"Initialized SummarizerAgent with model: {model}")
    
    def summarize(self, text: str, prompt: Optional[str] = None) -> str:
        """
        Summarize a single text.
        
        Args:
            text: Text to summarize
            prompt: Custom summarization prompt (optional)
        
        Returns:
            Generated summary
        
        Raises:
            ValueError: If text is invalid
            Exception: If API call fails
        """
        # Validate input
        if not validate_text(text):
            raise ValueError(f"Invalid text: must be between 10 and 10000 characters")
        
        # Use custom prompt or default
        prompt_to_use = prompt or self.summarization_prompt
        
        logger.debug(f"Summarizing text of length: {len(text)}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": f"{prompt_to_use}\n\nText:\n{text}"},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"Successfully generated summary of length: {len(summary)}")
            return summary
        
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            raise
    
    def summarize_batch(
        self,
        texts: List[str],
        prompt: Optional[str] = None,
        delay: float = BATCH_REQUEST_DELAY,
    ) -> List[str]:
        """
        Summarize multiple texts with delay between requests.
        
        Args:
            texts: List of texts to summarize
            prompt: Custom summarization prompt (optional)
            delay: Delay between requests in seconds (default: 0.5)
        
        Returns:
            List of summaries in the same order as input texts
        
        Raises:
            ValueError: If any text is invalid
        """
        logger.info(f"Starting batch summarization of {len(texts)} texts")
        
        # Validate all texts
        invalid_texts = [
            idx for idx, text in enumerate(texts)
            if not validate_text(text)
        ]
        
        if invalid_texts:
            raise ValueError(f"Invalid texts at indices: {invalid_texts}")
        
        summaries = []
        for idx, text in enumerate(texts):
            try:
                summary = self.summarize(text, prompt)
                summaries.append(summary)
                
                # Add delay between requests (except after last request)
                if idx < len(texts) - 1:
                    time.sleep(delay)
            
            except Exception as e:
                logger.error(f"Error summarizing text {idx}: {str(e)}")
                raise
        
        logger.info(f"Completed batch summarization of {len(texts)} texts")
        return summaries
    
    def set_prompt(self, prompt: str) -> None:
        """
        Set custom summarization prompt.
        
        Args:
            prompt: Custom prompt string
        """
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must be a non-empty string")
        
        self.summarization_prompt = prompt
        logger.info("Updated summarization prompt")
    
    def set_system_message(self, message: str) -> None:
        """
        Set custom system message for the model.
        
        Args:
            message: System message string
        """
        if not isinstance(message, str) or not message.strip():
            raise ValueError("System message must be a non-empty string")
        
        self.system_message = message
        logger.info("Updated system message")
    
    def get_config(self) -> dict:
        """
        Get current agent configuration.
        
        Returns:
            Dictionary with current configuration
        """
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "system_message": self.system_message,
            "summarization_prompt": self.summarization_prompt,
        }
    
    def update_config(self, **kwargs) -> None:
        """
        Update agent configuration.
        
        Args:
            **kwargs: Configuration parameters to update
        
        Raises:
            ValueError: If invalid parameter provided
        """
        valid_params = {
            "model", "temperature", "max_tokens", "top_p",
            "system_message", "summarization_prompt"
        }
        
        invalid_params = set(kwargs.keys()) - valid_params
        if invalid_params:
            raise ValueError(f"Invalid parameters: {invalid_params}")
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        logger.info(f"Updated configuration: {kwargs}")
