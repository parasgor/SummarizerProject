"""
Configuration module for the Summarizer Agent.
Contains all configurable parameters and constants.
"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# ============================================================================
# API Configuration
# ============================================================================

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in .env file")

MODEL = "gpt-4o-mini"
TEMPERATURE = 0.7
MAX_TOKENS = 500
TOP_P = 0.95

# ============================================================================
# Summarization Configuration
# ============================================================================

# Default summarization prompt
DEFAULT_SUMMARIZATION_PROMPT = (
    "Summarize the text in 3 concise sentences, focusing on main points and key information."
)

# System message for the summarizer
SYSTEM_MESSAGE = "You are a professional summarizer specializing in creating concise, accurate summaries."

# ============================================================================
# Evaluation Configuration
# ============================================================================

# Metrics to evaluate
METRICS_TO_EVALUATE = [
    "SummarizationMetric",
    "ContextualPrecisionMetric",
    "ContextualRecallMetric",
    "BiasMetric",
    "ToxicityMetric",
    "PromptAlignmentMetric",
    "ReadabilityMetric",
]

# Performance thresholds
PASS_THRESHOLD = 0.7  # Score >= 0.7 is considered PASS
MIN_SCORE = 0.0
MAX_SCORE = 1.0

# ============================================================================
# Evaluation Report Configuration
# ============================================================================

# Table format for output
TABLE_FORMAT = "grid"

# Number of decimal places for scores
SCORE_DECIMAL_PLACES = 2

# Enable detailed logging
VERBOSE_LOGGING = os.getenv("VERBOSE_LOGGING", "false").lower() == "true"

# ============================================================================
# Batch Processing Configuration
# ============================================================================

# Default batch size
DEFAULT_BATCH_SIZE = 10

# Delay between batch requests (seconds) to respect rate limits
BATCH_REQUEST_DELAY = 0.5

# ============================================================================
# Logging Configuration
# ============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "summarizer_agent.log"

# ============================================================================
# File Paths
# ============================================================================

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================================
# Constants
# ============================================================================

# Supported models
SUPPORTED_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]

# Metric result categories
METRIC_CATEGORIES = {
    "quality": ["SummarizationMetric"],
    "precision": ["ContextualPrecisionMetric"],
    "recall": ["ContextualRecallMetric"],
    "safety": ["BiasMetric", "ToxicityMetric"],
    "alignment": ["PromptAlignmentMetric"],
    "readability": ["ReadabilityMetric"],
}
