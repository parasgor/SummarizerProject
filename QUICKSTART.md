# Quick Reference Guide

## Installation & Setup

### 1. Clone and Setup
```bash
git clone https://github.com/parasgor/SummarizerProject.git
cd SummarizerProject
chmod +x setup.sh
./setup.sh
```

Or using Make:
```bash
make setup
```

### 2. Configure API Key
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
export OPENAI_API_KEY="your-key-here"
```

## Quick Start Examples

### Basic Summarization
```python
from src.agent import SummarizerAgent

agent = SummarizerAgent()
summary = agent.summarize("Your long text here...")
print(summary)
```

### Batch Processing
```python
from src.agent import SummarizerAgent

agent = SummarizerAgent()
texts = ["Text 1...", "Text 2...", "Text 3..."]
summaries = agent.summarize_batch(texts)
```

### Evaluation
```python
from src.agent import SummarizerAgent
from src.evaluation import evaluate_summaries

agent = SummarizerAgent()

test_data = [
    {
        "text": "Original text...",
        "generated_summary": agent.summarize("Original text..."),
        "expected_summary": "Reference summary...",
    }
]

results = evaluate_summaries(test_data)
results.print_report()
```

### Custom Configuration
```python
agent = SummarizerAgent(
    model="gpt-4o",
    temperature=0.5,
    max_tokens=500,
)

agent.set_prompt("Summarize in 2 sentences, focusing on key insights.")
```

## Common Make Commands

```bash
make help              # Show all available commands
make setup            # Setup development environment
make install          # Install dependencies
make install-dev      # Install with dev tools
make test             # Run tests with coverage
make test-fast        # Run tests without coverage
make lint             # Check code style
make format           # Format code
make check            # Run all checks
make run-basic        # Run basic example
make run-advanced     # Run advanced example
make run-batch        # Run batch example
make clean            # Remove build artifacts
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v

# Using Make
make test-cov
make test-fast
```

## Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Or using Make
make format

# Check formatting
make format-check

# Lint
make lint

# Type checking
make type-check

# Run all checks
make check
```

## Project Structure

```
summarizer_project_prod/
├── src/                          # Source code
│   ├── __init__.py
│   ├── agent.py                  # Core summarizer agent
│   ├── evaluation.py             # Evaluation logic
│   ├── metrics.py                # Custom metrics
│   ├── config.py                 # Configuration
│   └── utils.py                  # Utilities
├── tests/                        # Test suite
│   ├── test_agent.py
│   ├── test_evaluation.py
│   ├── test_integration.py
│   └── test_metrics.py
├── examples/                     # Usage examples
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   └── batch_processing.py
├── .env.example                  # Environment template
├── .gitignore
├── setup.py                      # Package setup
├── setup.sh                      # Quick setup script
├── pyproject.toml                # Project config
├── pytest.ini                    # Pytest config
├── Makefile                      # Make commands
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
├── CONTRIBUTING.md               # Contribution guide
├── CHANGELOG.md                  # Version history
├── LICENSE                       # MIT License
└── .github/workflows/            # CI/CD configuration
    └── tests.yml
```

## API Reference Summary

### SummarizerAgent

**Methods:**
- `summarize(text, prompt=None)` → str
- `summarize_batch(texts, prompt=None, delay=0.5)` → List[str]
- `set_prompt(prompt)` → None
- `set_system_message(message)` → None
- `get_config()` → dict
- `update_config(**kwargs)` → None

**Properties:**
- `model`, `temperature`, `max_tokens`, `top_p`
- `system_message`, `summarization_prompt`

### EvaluationResult

**Methods:**
- `get_aggregate_scores()` → Dict[str, float]
- `get_pass_rates()` → Dict[str, float]
- `get_per_input_scores()` → List[Dict]
- `get_overall_stats()` → Dict[str, float]
- `print_report()` → None

### evaluate_summaries()

```python
evaluate_summaries(
    test_data: List[Dict],
    prompt: Optional[str] = None,
    metrics: Optional[List] = None,
) → EvaluationResult
```

## Configuration

Edit `src/config.py` to customize:

```python
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.7
MAX_TOKENS = 500
DEFAULT_SUMMARIZATION_PROMPT = "Summarize concisely..."
PASS_THRESHOLD = 0.7
METRICS_TO_EVALUATE = [...]  # List of metric names
```

## Metrics

**Built-in Metrics:**
- `SummarizationMetric` - Quality of summarization
- `ContextualPrecisionMetric` - Precision of context use
- `ContextualRecallMetric` - Recall of important context
- `BiasMetric` - Bias detection
- `ToxicityMetric` - Toxicity detection
- `PromptAlignmentMetric` - Alignment with prompt

**Custom Metrics:**
- `ReadabilityMetric` - Grammar and fluency
- `RelevanceMetric` - Relevance to source
- `ConcisennessMetric` - Conciseness evaluation
- `FactualAccuracyMetric` - Factual accuracy

## Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional
LOG_LEVEL=INFO
VERBOSE_LOGGING=false
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key not found | Check `.env` file and OPENAI_API_KEY |
| Import errors | Run `pip install -r requirements.txt` |
| Tests failing | Run `pytest -v` for details, check mocks |
| Rate limits | Use batch with delays, or `summarize_batch()` |
| Coverage low | Add tests for uncovered code paths |

## Performance Tips

1. **Batch Processing**: Use `summarize_batch()` for multiple texts
2. **Prompt Engineering**: Customize prompts for better results
3. **Model Selection**: Use `gpt-3.5-turbo` for cost, `gpt-4` for quality
4. **Temperature**: Lower (0.5) for consistent, higher (0.9) for creative
5. **Caching**: Store summaries to avoid re-processing

## Support & Resources

- **Issues**: https://github.com/parasgor/SummarizerProject/issues
- **Discussions**: https://github.com/parasgor/SummarizerProject/discussions
- **Documentation**: See README.md
- **Contributing**: See CONTRIBUTING.md

## Running Examples

```bash
# Basic example
python examples/basic_usage.py

# Advanced example (requires config)
python examples/advanced_usage.py

# Batch processing
python examples/batch_processing.py

# Or using Make
make run-basic
make run-advanced
make run-batch
```

---

For more information, see README.md and the examples directory.
