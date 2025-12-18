# Oyemi MCP Server - Directory Submission

## Basic Information

- **Name**: oyemi-mcp
- **Version**: 0.1.0
- **Author**: Kaossara Osseni
- **Email**: admin@grandnasser.com
- **Website**: https://grandnasser.com

## Links

- **PyPI**: https://pypi.org/project/oyemi-mcp/
- **GitHub**: https://github.com/Osseni94/oyemi-mcp
- **Documentation**: https://grandnasser.com/docs/oyemi-mcp

## Description

MCP server for the Oyemi semantic lexicon. Provides deterministic word-to-code mapping and valence/sentiment analysis for AI agents like Claude, ChatGPT, and Gemini.

### Key Features

- **Semantic Encoding**: Convert words to deterministic semantic codes (HHHH-LLLLL-P-A-V format)
- **Valence Analysis**: Analyze text sentiment using lexicon-based valence scores
- **Semantic Similarity**: Measure how similar two words are semantically
- **Synonym/Antonym Lookup**: Find related words using WordNet synsets
- **Zero Runtime Dependencies**: No external NLP libraries needed at runtime
- **145,000+ Words**: Comprehensive English lexicon

### What Makes It Unique

Unlike ML-based sentiment tools, Oyemi provides:
- **Deterministic results**: Same input always returns same output
- **Explainable scores**: Based on WordNet semantic structure
- **No cloud dependencies**: Runs entirely locally
- **No API keys**: Free and open source

## Available Tools

| Tool | Description |
|------|-------------|
| `encode_word` | Get semantic code for a word |
| `analyze_text` | Analyze text valence/sentiment |
| `semantic_similarity` | Compare two words (0-1 score) |
| `find_synonyms` | Find synonyms for a word |
| `find_antonyms` | Find antonyms for a word |
| `batch_encode` | Encode multiple words at once |
| `get_lexicon_info` | Get lexicon statistics |

## Installation

```bash
pip install oyemi-mcp
```

## Configuration

### Claude Desktop

```json
{
  "mcpServers": {
    "oyemi": {
      "command": "oyemi-mcp"
    }
  }
}
```

## Categories

- Natural Language Processing
- Sentiment Analysis
- Semantic Analysis
- Text Processing
- Linguistics

## Tags

mcp, semantic-analysis, sentiment, valence, wordnet, nlp, claude, ai-tools

## License

MIT License
