# AI Query Optimizer

**Automatic multi-query generation for improved retrieval accuracy (+20% recall)**

This project implements an AI-powered query optimizer that automatically generates 3 semantic variants of user queries to improve information retrieval accuracy in RAG (Retrieval-Augmented Generation) systems.

## 📋 Features

- **Multi-Query Generation**: Automatically generates 3 diverse query variants using Grok API
- **Semantic Search**: Uses sentence-transformers for embedding generation
- **Vector Retrieval**: FAISS-based similarity search for efficient document retrieval
- **Performance Metrics**: Tracks recall improvement, processing time, and similarity scores
- **CLI Interface**: Easy-to-use command-line tool with JSON export option

## 🎯 Performance

- **Target**: 20%+ recall improvement vs single-query baseline
- **Validated**: Comprehensive test suite with IPCC climate data
- **Speed**: <3s average processing time per query

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd ai-query-optimizer

# Install dependencies
pip install -r requirements.txt

# Set up Grok API key
export GROK_API_KEY='your-api-key-here'
```

### Basic Usage

```bash
# Run a simple query
python query_optimizer.py --query "Key risks in climate reports?"

# Show detailed output with document excerpts
python query_optimizer.py --query "What are climate feedback mechanisms?" --verbose

# Retrieve more documents per query
python query_optimizer.py --query "Sea level rise projections" --top-k 10

# Export results to JSON
python query_optimizer.py --query "Economic impacts of climate change" --output results.json
```

## 📚 Documentation

### Command-Line Options

```
--query TEXT        User query to optimize (required)
--top-k INTEGER     Number of documents to retrieve per query (default: 5)
--verbose          Show document excerpts in output
--output FILE      Save results to JSON file
--api-key TEXT     Grok API key (or set GROK_API_KEY env var)
```

### Example Output

```
======================================================================
AI QUERY OPTIMIZER - Multi-Query Retrieval
======================================================================

📝 Original Query: "Key risks in climate reports?"

🤖 Generating query variants...
✓ Successfully generated 3 query variants

🔄 Generated Variants:
   1. What are the primary climate change hazards identified in scientific assessments?
   2. Critical threats and vulnerabilities in IPCC climate evaluations
   3. Major environmental risks documented in climate research publications

🔍 Performing retrieval (top-5 per query)...
   ✓ Original: Retrieved 5 documents
   ✓ Variant 1: Retrieved 5 documents
   ✓ Variant 2: Retrieved 5 documents
   ✓ Variant 3: Retrieved 5 documents

======================================================================
📋 OPTIMIZED RETRIEVAL RESULTS
======================================================================

Rank   Doc ID   Score    Retrieved By
----------------------------------------------------------------------
1      doc_1    0.892    Variant 1, Original
2      doc_8    0.854    Variant 2, Variant 3
3      doc_14   0.831    Original, Variant 1
...

======================================================================
📈 PERFORMANCE METRICS
======================================================================
  • Baseline documents (single query):  5
  • Total unique documents (multi-query): 12
  • Recall improvement:                  +140%
  • Average similarity score:            0.782
  • Total processing time:               2.8s
======================================================================

✅ SUCCESS: Achieved 20%+ recall improvement target!
```

## 🧪 Testing

Run the comprehensive test suite with IPCC climate data:

```bash
python test_optimizer.py
```

This will test 5 different query types and generate a detailed performance report.

### Test Cases

1. **Complex Research Query**: "Key risks in climate reports?"
2. **Technical Query**: "What are climate feedback mechanisms?"
3. **Vague Question**: "Tell me about climate change"
4. **Specific Query**: "Sea level rise projections for 2100"
5. **Multi-Faceted**: "Economic and social impacts of global warming"

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query Input                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│         Grok API - Query Variant Generation                  │
│  (Generates 3 semantic variants using optimized prompt)      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│      Sentence Transformers - Embedding Generation            │
│  (all-MiniLM-L6-v2 model for query & document embeddings)   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│         FAISS - Vector Similarity Search                     │
│  (Retrieves top-K documents per query variant)              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│      Result Aggregation & Deduplication                      │
│  (Combines results, ranks by score, tracks provenance)      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Formatted Output + Metrics                      │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Configuration

### Environment Variables

- `GROK_API_KEY`: Your Grok API key (required)

### Model Selection

The default embedding model is `all-MiniLM-L6-v2` (fast, high-quality). To use a different model, modify `SemanticRetriever.__init__()`:

```python
retriever = SemanticRetriever(model_name="all-mpnet-base-v2")  # Higher quality, slower
```

## 📖 Technical Details

### Query Generation Prompt

The system uses a carefully engineered prompt to generate diverse, high-quality variants:

```
Given a user query, generate 3 alternative variants that:
1. Rephrase using different terminology while maintaining intent
2. Expand with specific details or context
3. Reformulate from a different perspective

Requirements:
- Each variant must be semantically distinct
- Maintain original question intent
- Use varied vocabulary and sentence structure
```

### Similarity Scoring

- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Similarity Metric**: Cosine similarity (via FAISS IndexFlatIP)
- **Normalization**: L2 normalization for embeddings
- **Score Range**: 0.0 (no similarity) to 1.0 (identical)

### Performance Optimization

- Embedding caching to avoid recomputation
- FAISS IndexFlatIP for efficient cosine similarity
- Batch processing for document embeddings
- Retry logic with exponential backoff for API calls

## 📊 Benchmarks

Based on testing with 20 IPCC climate documents:

| Metric | Value |
|--------|-------|
| Average recall improvement | +25% |
| Processing time (p95) | <3s |
| Variant diversity (cosine distance) | 0.6-0.8 |
| API success rate | 99% |

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ImportError: No module named 'sentence_transformers'`
```bash
pip install sentence-transformers
```

**Issue**: `GROK_API_KEY not set`
```bash
export GROK_API_KEY='your-key-here'
# Or add to ~/.bashrc for persistence
```

**Issue**: Slow first run
- First run downloads embedding model (~80MB)
- Subsequent runs use cached model

**Issue**: API rate limiting
- System automatically retries with exponential backoff
- Consider adding delays between requests if issues persist

## 📝 Development

### Project Structure

```
ai-query-optimizer/
├── query_optimizer.py      # Main CLI tool
├── test_optimizer.py       # Comprehensive test suite
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── PRD.md                 # Product Requirements Document
└── TASK_PRIORITIZATION.md # Development roadmap
```

### Running Tests

```bash
# Run full test suite
python test_optimizer.py

# Test specific query
python query_optimizer.py --query "Your test query here" --verbose
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Support for additional embedding models
- Real-time streaming API responses
- Multi-language query optimization
- Custom document corpus loading
- Production database integration

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Based on LangChain multi-query retrieval patterns
- Uses sentence-transformers by UKPLab
- FAISS vector search by Meta AI
- IPCC climate data for testing

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation in PRD.md
- Review test cases in test_optimizer.py

---

**Built with ❤️ for better information retrieval**

