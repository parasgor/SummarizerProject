"""
Utility functions for the Summarizer Agent project.
"""

import json
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.config import LOG_LEVEL, LOG_FORMAT, LOG_FILE

# ============================================================================
# Logging Setup
# ============================================================================

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with console and file handlers.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# ============================================================================
# File I/O Functions
# ============================================================================

def load_json_data(file_path: str) -> Any:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
    
    Returns:
        Loaded data
    
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_data(data: Any, file_path: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save the JSON file
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_text_file(file_path: str) -> str:
    """
    Load text from a file.
    
    Args:
        file_path: Path to the text file
    
    Returns:
        File contents as string
    
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_text_file(content: str, file_path: str) -> None:
    """
    Save text to a file.
    
    Args:
        content: Text content to save
        file_path: Path to save the text file
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# ============================================================================
# Data Processing Functions
# ============================================================================

def truncate_text(text: str, max_length: int = 150, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested dictionary.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator for keys
    
    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# ============================================================================
# Validation Functions
# ============================================================================

def validate_text(text: str, min_length: int = 10, max_length: int = 10000) -> bool:
    """
    Validate text for summarization.
    
    Args:
        text: Text to validate
        min_length: Minimum length required
        max_length: Maximum length allowed
    
    Returns:
        True if text is valid, False otherwise
    """
    if not isinstance(text, str):
        return False
    
    text = text.strip()
    
    if len(text) < min_length:
        return False
    
    if len(text) > max_length:
        return False
    
    return True

def validate_test_case(test_case: Dict[str, str]) -> bool:
    """
    Validate a test case dictionary.
    
    Args:
        test_case: Test case to validate
    
    Returns:
        True if test case is valid
    """
    required_keys = {"text", "expected_summary"}
    
    if not isinstance(test_case, dict):
        return False
    
    if not all(key in test_case for key in required_keys):
        return False
    
    if not validate_text(test_case["text"]):
        return False
    
    if not isinstance(test_case["expected_summary"], str):
        return False
    
    return True

# ============================================================================
# Formatting Functions
# ============================================================================

def format_percentage(value: float) -> str:
    """Format a decimal value as percentage string."""
    return f"{value * 100:.2f}%"

def format_score(value: float, decimals: int = 2) -> str:
    """Format a score with specified decimal places."""
    return f"{value:.{decimals}f}"

def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()

def get_readable_timestamp() -> str:
    """Get current timestamp in human-readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============================================================================
# Error Handling Functions
# ============================================================================

def safe_get(d: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary with default.
    
    Args:
        d: Dictionary
        key: Key to get
        default: Default value if key not found
    
    Returns:
        Value or default
    """
    return d.get(key, default)

def retry_operation(func, max_retries: int = 3, delay: float = 1.0):
    """
    Retry an operation with exponential backoff.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        delay: Initial delay between retries
    
    Returns:
        Result of function
    
    Raises:
        Exception: If all retries fail
    """
    import time
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay * (2 ** attempt))
