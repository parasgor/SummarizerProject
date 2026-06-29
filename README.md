# AI Summarizer Agent 📝

A production-grade AI summarizer agent that uses OpenAI's GPT models to generate high-quality text summaries with comprehensive evaluation metrics.

## Features ✨

- **Intelligent Summarization**: Uses GPT-4o-mini to generate concise, accurate summaries
- **Multi-Metric Evaluation**: Evaluates summaries using 7 advanced metrics:
  - Summarization Quality
  - Contextual Precision
  - Contextual Recall
  - Bias Detection
  - Toxicity Detection
  - Prompt Alignment
  - Readability
- **Production Ready**: Follows enterprise-grade code structure and best practices
- **Comprehensive Testing**: Includes unit tests, integration tests, and evaluation tests
- **Detailed Reporting**: Generates aggregate and per-input performance reports

## Project Structure 📁

```
summarizer_project/
├── src/
│   ├── __init__.py
│   ├── agent.py                 # Core summarizer agent
│   ├── evaluation.py            # Evaluation logic with DeepEval
│   ├── metrics.py               # Custom metrics definitions
│   ├── config.py                # Configuration and constants
│   └── utils.py                 # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_agent.py           # Unit tests for agent
│   ├── test_evaluation.py       # Unit tests for evaluation
│   ├── test_integration.py      # Integration tests
│   └── test_metrics.py          # Tests for custom metrics
├── examples/
│   ├── basic_usage.py           # Basic usage example
│   ├── advanced_usage.py        # Advanced usage with custom config
│   └── batch_processing.py      # Batch processing example
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup configuration
├── pytest.ini                   # Pytest configuration
└── README.md                    # This file
```

## Installation 🚀

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/summarizer-agent.git
cd summarizer-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage 📖

### Basic Usage

```python
from src.agent import SummarizerAgent

# Initialize agent
agent = SummarizerAgent()

# Summarize text
text = "Your long text here..."
summary = agent.summarize(text)
print(summary)
```

### With Evaluation

```python
from src.agent import SummarizerAgent
from src.evaluation import evaluate_summaries

agent = SummarizerAgent()

# Prepare test data
test_data = [
    {
        "text": "Original text...",
        "expected_summary": "Expected summary..."
    }
]

# Generate summaries
for item in test_data:
    item["generated_summary"] = agent.summarize(item["text"])

# Evaluate
results = evaluate_summaries(test_data)

# Print results
results.print_report()
```

### Batch Processing

```python
from src.agent import SummarizerAgent
from src.utils import load_json_data

agent = SummarizerAgent()

# Load batch data
texts = load_json_data("data/texts.json")

# Process batch
summaries = agent.summarize_batch(texts)

# Save results
for idx, summary in enumerate(summaries):
    print(f"Summary {idx}: {summary}")
```

## Configuration 🔧

Edit `src/config.py` to customize:

```python
# Model configuration
MODEL = "gpt-4o-mini"
TEMPERATURE = 0.7
MAX_TOKENS = 500

# Summarization prompt
SUMMARIZATION_PROMPT = "Summarize in 3 concise sentences, focusing on main points."

# Evaluation metrics to use
METRICS_TO_EVALUATE = [
    "SummarizationMetric",
    "ContextualPrecisionMetric",
    "ContextualRecallMetric",
    "BiasMetric",
    "ToxicityMetric",
    "PromptAlignmentMetric",
    "ReadabilityMetric",
]

# Thresholds
PASS_THRESHOLD = 0.7
MIN_SCORE = 0.0
MAX_SCORE = 1.0
```

## API Reference 📚

### SummarizerAgent

Main agent class for text summarization.

#### Methods

**`summarize(text: str, prompt: Optional[str] = None) -> str`**
- Summarizes a single text
- Parameters:
  - `text`: The text to summarize
  - `prompt`: Custom summarization prompt (optional)
- Returns: Generated summary string

**`summarize_batch(texts: List[str]) -> List[str]`**
- Summarizes multiple texts
- Parameters:
  - `texts`: List of texts to summarize
- Returns: List of summaries

**`set_prompt(prompt: str) -> None`**
- Sets custom summarization prompt
- Parameters:
  - `prompt`: Custom prompt string

### EvaluationResult

Contains evaluation results and provides reporting methods.

#### Methods

**`get_aggregate_scores() -> Dict[str, float]`**
- Returns average scores per metric

**`get_pass_rates() -> Dict[str, float]`**
- Returns pass rates per metric

**`get_per_input_scores() -> List[float]`**
- Returns average scores per input

**`print_report() -> None`**
- Prints formatted evaluation report

## Testing 🧪

Run tests with pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v
```

## Examples 💡

See the `examples/` directory for:
- Basic usage
- Advanced configuration
- Batch processing
- Custom metrics

## Performance Considerations ⚡

- **API Costs**: Each summarization costs ~$0.001 USD
- **Latency**: Average response time ~2-3 seconds per text
- **Rate Limits**: Default is 500 RPM (requests per minute)
- **Batch Processing**: Use `summarize_batch()` for multiple texts

## Troubleshooting 🔧

### Issue: "OpenAI API key not found"
**Solution**: Ensure `.env` file exists with `OPENAI_API_KEY` set

### Issue: "Import error from deepeval"
**Solution**: Reinstall dependencies:
```bash
pip install --upgrade deepeval
```

### Issue: Rate limit exceeded
**Solution**: Add delays between requests or use batch processing with delays

## Contributing 🤝

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License 📄

This project is licensed under the MIT License - see LICENSE file for details.

## Support 💬

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the examples directory

## Changelog 📝

### v1.0.0 (2024)
- Initial release
- Core summarizer agent
- 7 evaluation metrics
- Comprehensive test suite
- Full documentation

## Credits 🙌

- Built with [OpenAI GPT-4o-mini](https://openai.com/)
- Evaluation powered by [DeepEval](https://github.com/confident-ai/deepeval)
- Testing with [Pytest](https://pytest.org/)

---

**Made with ❤️ for the AI community**
