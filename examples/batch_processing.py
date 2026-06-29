"""
Batch processing example for summarizing multiple texts.
"""

import json
from src.agent import SummarizerAgent
from src.utils import save_json_data, get_readable_timestamp


def main():
    """Batch process multiple texts for summarization."""
    
    print("=" * 100)
    print("📦 BATCH PROCESSING EXAMPLE")
    print("=" * 100)
    
    # Initialize agent
    agent = SummarizerAgent()
    
    # Sample batch of texts to summarize
    batch_texts = [
        {
            "id": "tech_001",
            "text": (
                "Blockchain technology, originally developed for Bitcoin, has evolved beyond cryptocurrency. "
                "It provides a distributed, immutable ledger system that can be applied to supply chain management, "
                "healthcare records, intellectual property, and more. The key advantages are transparency, security, "
                "and reduced need for intermediaries. However, challenges include scalability, energy consumption, "
                "and regulatory clarity that need to be addressed."
            )
        },
        {
            "id": "health_001",
            "text": (
                "Personalized medicine uses genetic, environmental, and lifestyle data to tailor treatments to individuals. "
                "Recent advances in genomic sequencing and AI have made it more accessible and affordable. "
                "This approach promises better outcomes, fewer side effects, and more efficient use of healthcare resources. "
                "However, privacy concerns and the need for standardized protocols remain significant challenges."
            )
        },
        {
            "id": "energy_001",
            "text": (
                "Renewable energy sources like solar, wind, and hydroelectric power are becoming increasingly cost-competitive "
                "with fossil fuels. Advances in battery storage technology are addressing intermittency issues. "
                "Many countries have committed to net-zero emissions targets, driving massive investments in clean energy infrastructure. "
                "The transition requires overcoming grid modernization challenges and managing economic impacts on fossil fuel industries."
            )
        },
        {
            "id": "ai_001",
            "text": (
                "Large Language Models (LLMs) have revolutionized natural language processing. Models like GPT-4 can perform "
                "a wide range of tasks including translation, question answering, and code generation. "
                "Their capabilities raise both exciting possibilities and serious concerns about misinformation, bias, and job displacement. "
                "Responsible development and deployment of LLMs requires robust evaluation frameworks and ethical guidelines."
            )
        },
        {
            "id": "space_001",
            "text": (
                "Commercial space exploration has entered a new era with companies like SpaceX and Blue Origin. "
                "Reusable rockets have dramatically reduced launch costs, making space more accessible. "
                "Plans include space tourism, orbital manufacturing, and lunar/Mars exploration. "
                "This democratization of space access could lead to unprecedented scientific discoveries and economic opportunities."
            )
        },
    ]
    
    print(f"\n📥 Loading {len(batch_texts)} texts for summarization...\n")
    
    # Process batch
    results = []
    for idx, item in enumerate(batch_texts, start=1):
        print(f"[{idx}/{len(batch_texts)}] Processing {item['id']}...", end=" ")
        
        summary = agent.summarize(item['text'])
        
        result = {
            "id": item['id'],
            "original_length": len(item['text']),
            "summary": summary,
            "summary_length": len(summary),
            "compression_ratio": len(summary) / len(item['text']),
        }
        results.append(result)
        
        print(f"✓ ({result['summary_length']} chars)")
    
    # Display results
    print("\n" + "=" * 100)
    print("📊 BATCH PROCESSING RESULTS")
    print("=" * 100 + "\n")
    
    total_original = sum(r['original_length'] for r in results)
    total_summary = sum(r['summary_length'] for r in results)
    avg_compression = sum(r['compression_ratio'] for r in results) / len(results)
    
    for result in results:
        print(f"\n📄 {result['id']}")
        print("-" * 100)
        print(f"Original length: {result['original_length']} chars")
        print(f"Summary length: {result['summary_length']} chars")
        print(f"Compression ratio: {result['compression_ratio']:.2%}")
        print(f"\nSummary:")
        print(f"  {result['summary']}")
    
    # Summary statistics
    print("\n" + "=" * 100)
    print("📈 SUMMARY STATISTICS")
    print("=" * 100)
    print(f"\nTotal texts processed: {len(results)}")
    print(f"Total original characters: {total_original:,}")
    print(f"Total summary characters: {total_summary:,}")
    print(f"Average compression ratio: {avg_compression:.2%}")
    print(f"Overall reduction: {(1 - avg_compression):.2%}")
    
    # Save results to JSON
    output_file = f"batch_results_{get_readable_timestamp().replace(' ', '_').replace(':', '-')}.json"
    save_json_data(
        {
            "timestamp": get_readable_timestamp(),
            "total_processed": len(results),
            "statistics": {
                "total_original_chars": total_original,
                "total_summary_chars": total_summary,
                "average_compression_ratio": avg_compression,
                "overall_reduction_percentage": 1 - avg_compression,
            },
            "results": results,
        },
        output_file
    )
    
    print(f"\n✓ Results saved to: {output_file}")
    print("\n" + "=" * 100 + "\n")


if __name__ == "__main__":
    main()
