#!/bin/bash
# Quick Start Demo for AI Query Optimizer

echo "========================================================================"
echo "  AI QUERY OPTIMIZER - Quick Start Demo"
echo "========================================================================"
echo ""

# Check for API key
if [ -z "$GROK_API_KEY" ]; then
    echo "❌ Error: GROK_API_KEY environment variable not set"
    echo ""
    echo "To set your API key, run:"
    echo "  export GROK_API_KEY='your-api-key-here'"
    echo ""
    echo "Or add it to your shell profile for persistence:"
    echo "  echo 'export GROK_API_KEY=\"your-api-key-here\"' >> ~/.bashrc"
    echo ""
    exit 1
fi

echo "✅ GROK_API_KEY found"
echo ""

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python3 -c "import requests, sentence_transformers, faiss" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some dependencies missing. Installing..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed"
else
    echo "✅ All dependencies installed"
fi
echo ""

# Demo query
DEMO_QUERY="Key risks in climate reports?"

echo "========================================================================"
echo "  Running Demo Query"
echo "========================================================================"
echo "Query: \"$DEMO_QUERY\""
echo ""

python3 query_optimizer.py --query "$DEMO_QUERY" --verbose

echo ""
echo "========================================================================"
echo "  Demo Complete!"
echo "========================================================================"
echo ""
echo "Try more queries:"
echo "  python3 query_optimizer.py --query \"What are climate feedback mechanisms?\""
echo "  python3 query_optimizer.py --query \"Sea level rise projections\" --top-k 10"
echo "  python3 query_optimizer.py --query \"Economic impacts\" --output results.json"
echo ""
echo "Run full test suite:"
echo "  python3 test_optimizer.py"
echo ""

