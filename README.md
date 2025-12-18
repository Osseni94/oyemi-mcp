# Oyemi MCP Server

MCP (Model Context Protocol) server for the Oyemi semantic lexicon. Provides deterministic word-to-code mapping and valence analysis for AI agents like Claude, ChatGPT, and Gemini.

## Features

- **Semantic Encoding**: Convert words to deterministic semantic codes
- **Valence Analysis**: Analyze text sentiment using lexicon-based valence
- **Semantic Similarity**: Measure how similar two words are
- **Synonym/Antonym Lookup**: Find related words
- **Zero Runtime Dependencies**: No external NLP libraries needed at runtime

## Installation

```bash
pip install oyemi-mcp
```

Or install from source:

```bash
git clone https://github.com/Osseni94/oyemi-mcp
cd oyemi-mcp
pip install -e .
```

## Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "oyemi": {
      "command": "oyemi-mcp"
    }
  }
}
```

### Claude Code

Add to your MCP settings:

```json
{
  "mcpServers": {
    "oyemi": {
      "command": "oyemi-mcp"
    }
  }
}
```

## Available Tools

### `encode_word`
Encode a word to its semantic code.

```
encode_word("happy")
-> {
    "word": "happy",
    "code": "1023-00012-3-2-1",
    "pos": "adjective",
    "abstractness": "abstract",
    "valence": "positive"
}
```

### `analyze_text`
Analyze the valence/sentiment of text.

```
analyze_text("I feel hopeful but anxious about the future")
-> {
    "valence_score": 0.0,
    "sentiment": "neutral",
    "positive_words": ["hopeful"],
    "negative_words": ["anxious"],
    ...
}
```

### `semantic_similarity`
Compare two words semantically.

```
semantic_similarity("happy", "joyful")
-> {
    "similarity": 0.85,
    "relationship": "very similar"
}
```

### `find_synonyms`
Find synonyms for a word.

```
find_synonyms("happy")
-> {
    "synonyms": ["glad", "felicitous", "well-chosen"]
}
```

### `find_antonyms`
Find antonyms for a word.

```
find_antonyms("happy")
-> {
    "antonyms": ["unhappy"]
}
```

### `batch_encode`
Encode multiple words at once.

```
batch_encode(["happy", "sad", "neutral"])
-> {
    "results": [
        {"word": "happy", "valence": "positive"},
        {"word": "sad", "valence": "negative"},
        {"word": "neutral", "valence": "neutral"}
    ]
}
```

### `get_lexicon_info`
Get information about the lexicon.

```
get_lexicon_info()
-> {
    "name": "Oyemi",
    "version": "3.2.0",
    "word_count": 145014
}
```

## Code Format

Oyemi codes follow the format `HHHH-LLLLL-P-A-V`:

| Component | Description | Values |
|-----------|-------------|--------|
| HHHH | Semantic superclass | 4-digit category code |
| LLLLL | Synset ID | 5-digit unique identifier |
| P | Part of speech | 1=noun, 2=verb, 3=adj, 4=adv |
| A | Abstractness | 0=concrete, 1=mixed, 2=abstract |
| V | Valence | 0=neutral, 1=positive, 2=negative |

## Use Cases

- **AI Sentiment Analysis**: Let AI agents understand emotional tone
- **Semantic Grounding**: Provide concrete valence scores instead of guessing
- **Text Analysis**: Analyze documents, reviews, feedback
- **Word Relationships**: Find synonyms, antonyms, similar words

## License

MIT License

## Author

Kaossara Osseni - [grandnasser.com](https://grandnasser.com)
