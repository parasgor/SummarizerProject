"""
Basic usage example for the Summarizer Agent.
"""

from src.agent import SummarizerAgent

def main():
    """Basic summarization example."""
    
    # Initialize the agent
    agent = SummarizerAgent()
    
    # Example text to summarize
    text = """
    Artificial Intelligence has made remarkable progress in recent years, transforming various 
    industries from healthcare to finance. Machine learning models, particularly deep neural networks, 
    have achieved state-of-the-art results in tasks like image recognition, natural language processing, 
    and game playing. Companies are increasingly integrating AI into their products and services, 
    leading to improved efficiency and better user experiences. However, with great power comes 
    responsibility, and the field faces challenges related to bias, fairness, and ethical considerations 
    that must be addressed as AI becomes more prevalent in society.
    """
    
    print("=" * 80)
    print("📝 BASIC SUMMARIZER EXAMPLE")
    print("=" * 80)
    print("\nOriginal Text:")
    print(text)
    
    # Generate summary
    print("\nGenerating summary...")
    summary = agent.summarize(text)
    
    print("\n" + "-" * 80)
    print("Generated Summary:")
    print(summary)
    print("-" * 80)


if __name__ == "__main__":
    main()
