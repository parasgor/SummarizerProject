"""
Advanced usage example with custom configuration and evaluation.
"""

from src.agent import SummarizerAgent
from src.evaluation import evaluate_summaries
from src.metrics import (
    ReadabilityMetric,
    RelevanceMetric,
    ConcisennessMetric,
    FactualAccuracyMetric,
)
from deepeval.metrics import (
    SummarizationMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)


def main():
    """Advanced summarization with custom configuration and evaluation."""
    
    print("=" * 100)
    print("🚀 ADVANCED SUMMARIZER EXAMPLE")
    print("=" * 100)
    
    # ========================================================================
    # Step 1: Initialize agent with custom configuration
    # ========================================================================
    print("\n1️⃣  Initializing agent with custom configuration...")
    
    agent = SummarizerAgent(
        model="gpt-4o-mini",
        temperature=0.5,  # Lower temperature for more deterministic output
        max_tokens=300,
        top_p=0.9,
    )
    
    # Set custom summarization prompt
    custom_prompt = (
        "Summarize the following text in exactly 2-3 sentences. "
        "Focus on the most important insights and implications."
    )
    agent.set_prompt(custom_prompt)
    
    print(f"✓ Agent initialized with model: {agent.model}")
    print(f"✓ Temperature: {agent.temperature}")
    print(f"✓ Max tokens: {agent.max_tokens}")
    
    # ========================================================================
    # Step 2: Prepare test data
    # ========================================================================
    print("\n2️⃣  Preparing test data...")
    
    test_data = [
        {
            "text": (
                "Quantum computing represents a paradigm shift in computation. Unlike classical computers "
                "that use bits (0 or 1), quantum computers use quantum bits or qubits that can exist in "
                "superposition. This allows quantum computers to process multiple possibilities simultaneously. "
                "Although quantum computers are still in early stages, they promise to solve complex problems "
                "in drug discovery, optimization, and cryptography that are infeasible for classical computers."
            ),
            "expected_summary": (
                "Quantum computers use qubits for superposition processing, offering faster solutions for "
                "complex problems in drug discovery and cryptography compared to classical computers."
            ),
            "prompt": custom_prompt,
        },
        {
            "text": (
                "Climate change is one of the most pressing global challenges of our time. Rising temperatures "
                "are causing polar ice caps to melt, sea levels to rise, and weather patterns to become more extreme. "
                "These changes threaten biodiversity, human health, and food security. Governments and organizations "
                "worldwide are investing in renewable energy and sustainability initiatives to mitigate these effects. "
                "Individual actions, combined with policy changes, are essential to address this crisis."
            ),
            "expected_summary": (
                "Climate change threatens biodiversity and human welfare through rising temperatures and extreme weather. "
                "Solutions require global investment in renewables and individual behavioral changes."
            ),
            "prompt": custom_prompt,
        },
    ]
    
    print(f"✓ Prepared {len(test_data)} test cases")
    
    # ========================================================================
    # Step 3: Generate summaries
    # ========================================================================
    print("\n3️⃣  Generating summaries...")
    
    for idx, item in enumerate(test_data, start=1):
        print(f"\n   Processing text {idx}...")
        item["generated_summary"] = agent.summarize(
            item["text"],
            prompt=item["prompt"]
        )
        print(f"   ✓ Generated summary length: {len(item['generated_summary'])} characters")
    
    # ========================================================================
    # Step 4: Define custom metrics
    # ========================================================================
    print("\n4️⃣  Configuring evaluation metrics...")
    
    custom_metrics = [
        SummarizationMetric(),
        ContextualPrecisionMetric(),
        ContextualRecallMetric(),
        ReadabilityMetric(threshold=0.7),
        RelevanceMetric(threshold=0.7),
        ConcisennessMetric(threshold=0.65),
        FactualAccuracyMetric(threshold=0.8),
    ]
    
    print(f"✓ Configured {len(custom_metrics)} evaluation metrics")
    for metric in custom_metrics:
        print(f"   - {metric.name} (threshold: {metric.threshold})")
    
    # ========================================================================
    # Step 5: Evaluate summaries
    # ========================================================================
    print("\n5️⃣  Evaluating summaries...")
    
    results = evaluate_summaries(
        test_data,
        prompt=custom_prompt,
        metrics=custom_metrics,
    )
    
    print("✓ Evaluation completed")
    
    # ========================================================================
    # Step 6: Display results
    # ========================================================================
    print("\n6️⃣  Displaying results...\n")
    
    results.print_report()
    
    # ========================================================================
    # Step 7: Get detailed statistics
    # ========================================================================
    print("\n7️⃣  Detailed Statistics:\n")
    
    aggregate_scores = results.get_aggregate_scores()
    pass_rates = results.get_pass_rates()
    
    print("Metric Performance:")
    print("-" * 60)
    for metric_name in sorted(aggregate_scores.keys()):
        score = aggregate_scores[metric_name]
        pass_rate = pass_rates[metric_name]
        status = "✓" if pass_rate >= 0.5 else "✗"
        print(
            f"{status} {metric_name:30s} | "
            f"Score: {score:.2f} | Pass Rate: {pass_rate:.0%}"
        )
    
    print("\nAgent Configuration:")
    print("-" * 60)
    config = agent.get_config()
    for key, value in config.items():
        if key != "summarization_prompt":
            print(f"  {key:25s}: {value}")


if __name__ == "__main__":
    main()
