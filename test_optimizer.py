#!/usr/bin/env python3
"""
Test script for AI Query Optimizer using IPCC climate data.

This script runs comprehensive tests to validate the 20%+ recall improvement claim.
"""

import sys
import os
import time
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from query_optimizer import QueryOptimizer, load_sample_documents


# Extended IPCC-inspired test corpus
IPCC_TEST_DOCUMENTS = [
    "Climate change represents an urgent and potentially irreversible threat to human societies and the planet. The Intergovernmental Panel on Climate Change (IPCC) provides comprehensive assessments of climate science.",
    
    "Key risks from climate change include increased heat-related mortality, food insecurity from crop failures, water scarcity in drought-prone regions, and damage to critical infrastructure from extreme weather events.",
    
    "Sea level rise poses significant threats to coastal communities and small island nations. Projections indicate global mean sea level could rise by 0.43 to 0.84 meters by 2100 under moderate emission scenarios.",
    
    "Climate feedback mechanisms, such as ice-albedo feedback and permafrost thawing, can accelerate warming. As ice melts, darker surfaces absorb more solar radiation, creating a self-reinforcing cycle.",
    
    "Adaptation strategies must be implemented alongside mitigation efforts. These include building resilient infrastructure, developing drought-resistant crops, and establishing early warning systems for extreme weather.",
    
    "The primary driver of observed warming since the mid-20th century is anthropogenic greenhouse gas emissions, particularly CO2 from fossil fuel combustion and deforestation.",
    
    "Ecosystem disruption from climate change threatens biodiversity globally. Coral reefs face bleaching events from ocean warming, while shifting temperature zones force species migration and habitat loss.",
    
    "Economic impacts of climate change include reduced agricultural productivity, increased costs for coastal protection, higher insurance premiums, and disrupted supply chains from extreme weather events.",
    
    "Climate tipping points represent thresholds beyond which changes become irreversible on human timescales. Examples include Amazon rainforest dieback, Greenland ice sheet collapse, and Atlantic meridional overturning circulation shutdown.",
    
    "Mitigation requires rapid decarbonization across all sectors: transitioning to renewable energy, improving energy efficiency, electrifying transportation, and implementing carbon capture technologies.",
    
    "Social vulnerability to climate impacts varies by geography, income, and demographic factors. Low-income communities and developing nations face disproportionate risks despite contributing least to historical emissions.",
    
    "Climate models project temperature increases of 1.5°C to 4.5°C by 2100 depending on emission pathways. Limiting warming to 1.5°C requires achieving net-zero CO2 emissions by 2050.",
    
    "Ocean acidification from absorbed CO2 threatens marine ecosystems. Increasing acidity reduces calcium carbonate availability, impacting shellfish, corals, and organisms with calcium-based structures.",
    
    "Extreme weather event attribution science has advanced significantly, allowing researchers to quantify the influence of climate change on specific hurricanes, heat waves, and droughts.",
    
    "Climate justice principles emphasize that those least responsible for emissions face the greatest impacts. International climate agreements must address equity, capacity building, and technology transfer to developing nations.",
    
    "Arctic warming is occurring at twice the global average rate, a phenomenon known as Arctic amplification. This accelerated warming leads to sea ice loss, permafrost degradation, and methane release.",
    
    "Agricultural systems face multiple climate-related challenges including changing precipitation patterns, increased pest pressures, heat stress during critical growth periods, and soil degradation from extreme weather.",
    
    "Renewable energy deployment must accelerate dramatically to meet climate targets. Solar and wind power costs have declined significantly, making clean energy economically competitive with fossil fuels in many regions.",
    
    "Climate-related displacement is becoming a major humanitarian concern. Rising seas, droughts, and extreme weather are forcing populations to migrate, creating climate refugees and geopolitical tensions.",
    
    "Carbon pricing mechanisms, including carbon taxes and cap-and-trade systems, can provide economic incentives for emission reductions. However, political challenges and competitiveness concerns complicate implementation."
]


TEST_QUERIES = [
    {
        "query": "Key risks in climate reports?",
        "description": "Complex query covering multiple aspects",
        "expected_docs": [1, 2, 8, 14]  # Indices of highly relevant documents
    },
    {
        "query": "What are climate feedback mechanisms?",
        "description": "Technical query requiring specific knowledge",
        "expected_docs": [3, 15]
    },
    {
        "query": "Tell me about climate change",
        "description": "Vague, broad query",
        "expected_docs": [0, 5, 6, 11]
    },
    {
        "query": "Sea level rise projections for 2100",
        "description": "Specific query with temporal constraint",
        "expected_docs": [2, 11]
    },
    {
        "query": "Economic and social impacts of global warming",
        "description": "Multi-faceted query combining domains",
        "expected_docs": [7, 10, 14]
    }
]


def run_single_test(optimizer: QueryOptimizer, test_case: Dict, test_num: int, total_tests: int):
    """Run a single test case and return results."""
    
    print("\n" + "="*80)
    print(f"TEST {test_num}/{total_tests}: {test_case['description']}")
    print("="*80)
    print(f"Query: \"{test_case['query']}\"")
    print(f"Expected relevant docs: {test_case['expected_docs']}")
    
    # Run optimization
    results = optimizer.optimize(test_case['query'], top_k=5)
    
    # Analyze results
    metrics = results['metrics']
    aggregated = results['aggregated_results']
    
    # Check which expected docs were retrieved
    retrieved_indices = [doc_idx for doc_idx, _, _, _ in aggregated]
    expected = test_case['expected_docs']
    
    found_expected = [idx for idx in expected if idx in retrieved_indices]
    missed_expected = [idx for idx in expected if idx not in retrieved_indices]
    
    # Calculate precision metrics
    precision = len(found_expected) / len(retrieved_indices) if retrieved_indices else 0
    recall = len(found_expected) / len(expected) if expected else 0
    
    print(f"\n📊 Results Summary:")
    print(f"   • Baseline documents: {metrics['baseline_documents']}")
    print(f"   • Multi-query documents: {metrics['total_unique_documents']}")
    print(f"   • Recall improvement: +{metrics['recall_improvement_pct']}%")
    print(f"   • Processing time: {metrics['processing_time_sec']}s")
    print(f"   • Found {len(found_expected)}/{len(expected)} expected documents")
    if missed_expected:
        print(f"   • Missed documents: {missed_expected}")
    
    # Determine pass/fail
    target_met = metrics['recall_improvement_pct'] >= 20
    status = "✅ PASS" if target_met else "⚠️  BELOW TARGET"
    print(f"\n{status}")
    
    return {
        "test_case": test_case['description'],
        "query": test_case['query'],
        "metrics": metrics,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "passed": target_met
    }


def run_all_tests(api_key: str):
    """Run all test cases and generate summary report."""
    
    print("\n" + "="*80)
    print("🧪 AI QUERY OPTIMIZER - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print(f"Test corpus: {len(IPCC_TEST_DOCUMENTS)} IPCC climate documents")
    print(f"Test cases: {len(TEST_QUERIES)}")
    print("Target: 20%+ recall improvement per test\n")
    
    # Initialize optimizer
    optimizer = QueryOptimizer(api_key, IPCC_TEST_DOCUMENTS)
    
    # Run tests
    test_results = []
    start_time = time.time()
    
    for i, test_case in enumerate(TEST_QUERIES, 1):
        try:
            result = run_single_test(optimizer, test_case, i, len(TEST_QUERIES))
            test_results.append(result)
            time.sleep(1)  # Rate limiting between tests
        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            test_results.append({
                "test_case": test_case['description'],
                "query": test_case['query'],
                "error": str(e),
                "passed": False
            })
    
    total_time = time.time() - start_time
    
    # Generate summary report
    print("\n" + "="*80)
    print("📈 FINAL TEST REPORT")
    print("="*80)
    
    passed_tests = sum(1 for r in test_results if r.get('passed', False))
    total_tests = len(test_results)
    
    print(f"\n✅ Tests Passed: {passed_tests}/{total_tests} ({100*passed_tests/total_tests:.0f}%)")
    
    # Calculate aggregate metrics
    valid_results = [r for r in test_results if 'metrics' in r]
    if valid_results:
        avg_improvement = sum(r['metrics']['recall_improvement_pct'] for r in valid_results) / len(valid_results)
        avg_precision = sum(r.get('precision', 0) for r in valid_results) / len(valid_results)
        avg_recall = sum(r.get('recall', 0) for r in valid_results) / len(valid_results)
        avg_time = sum(r['metrics']['processing_time_sec'] for r in valid_results) / len(valid_results)
        
        print(f"\n📊 Aggregate Metrics:")
        print(f"   • Average recall improvement: +{avg_improvement:.1f}%")
        print(f"   • Average precision: {avg_precision:.3f}")
        print(f"   • Average recall: {avg_recall:.3f}")
        print(f"   • Average processing time: {avg_time:.2f}s")
        print(f"   • Total test time: {total_time:.2f}s")
        
        # Success criteria
        print(f"\n🎯 Success Criteria:")
        if avg_improvement >= 20:
            print(f"   ✅ Target met: {avg_improvement:.1f}% average improvement (target: 20%)")
        else:
            print(f"   ⚠️  Below target: {avg_improvement:.1f}% average improvement (target: 20%)")
        
        if passed_tests >= 0.8 * total_tests:
            print(f"   ✅ Test pass rate acceptable: {100*passed_tests/total_tests:.0f}% (target: 80%)")
        else:
            print(f"   ⚠️  Low pass rate: {100*passed_tests/total_tests:.0f}% (target: 80%)")
    
    # Detailed results table
    print(f"\n📋 Detailed Results:")
    print(f"{'#':<3} {'Query':<40} {'Improvement':<12} {'Status':<10}")
    print("-" * 80)
    for i, result in enumerate(test_results, 1):
        query = result['query'][:37] + "..." if len(result['query']) > 40 else result['query']
        improvement = f"+{result['metrics']['recall_improvement_pct']}%" if 'metrics' in result else "ERROR"
        status = "PASS" if result.get('passed', False) else "FAIL"
        print(f"{i:<3} {query:<40} {improvement:<12} {status:<10}")
    
    print("="*80 + "\n")
    
    # Final verdict
    if passed_tests == total_tests and avg_improvement >= 20:
        print("🎉 ALL TESTS PASSED! The AI Query Optimizer successfully achieves 20%+ recall improvement.")
    elif passed_tests >= 0.8 * total_tests:
        print("✅ Most tests passed. Consider prompt tuning for edge cases.")
    else:
        print("⚠️  Multiple test failures. Review prompt engineering and retrieval logic.")
    
    return test_results


def main():
    # Get API key
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        print("❌ Error: GROK_API_KEY environment variable not set")
        print("   Set it with: export GROK_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Run tests
    run_all_tests(api_key)


if __name__ == "__main__":
    main()

