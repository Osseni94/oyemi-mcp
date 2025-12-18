"""
Oyemi MCP Server - Semantic Analysis for AI Agents

Provides deterministic word-to-code mapping and valence analysis
through the Model Context Protocol. Zero runtime dependencies
beyond the Oyemi lexicon.

Author: Kaossara Osseni
Email: admin@grandnasser.com
Website: https://grandnasser.com
"""

import sys
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP(name="oyemi")

# Lazy load Oyemi to avoid import errors if not installed
_encoder_instance = None


def get_encoder():
    """Lazy load Oyemi Encoder instance."""
    global _encoder_instance

    if _encoder_instance is not None:
        return _encoder_instance

    try:
        from Oyemi import Encoder
        _encoder_instance = Encoder()
        return _encoder_instance
    except ImportError:
        raise ImportError(
            "oyemi is not installed. Install with: pip install oyemi"
        )


@mcp.tool()
def encode_word(word: str, all_senses: bool = False) -> dict:
    """
    Encode a word to its semantic code(s).

    Returns the deterministic semantic code for a word, which encodes:
    - Semantic superclass (category)
    - Synset ID (specific meaning)
    - Part of speech (noun, verb, adj, adv)
    - Abstractness (concrete, mixed, abstract)
    - Valence (neutral, positive, negative)

    Code format: HHHH-LLLLL-P-A-V

    Args:
        word: The word to encode
        all_senses: If True, return all senses; if False, return primary sense only

    Returns:
        Dictionary with semantic code(s) and parsed components

    Example:
        encode_word("happy")
        -> Returns code like "1023-00012-3-2-1" (adjective, abstract, positive)
    """
    try:
        enc = get_encoder()

        if not enc.contains(word):
            return {
                "word": word,
                "found": False,
                "error": f"Word '{word}' not found in lexicon"
            }

        if all_senses:
            parsed_codes = enc.encode_parsed(word)
            codes = [
                {
                    "code": p.raw,
                    "superclass": p.superclass,
                    "synset_id": p.synset_id,
                    "pos": p.pos_name,
                    "abstractness": p.abstractness_name,
                    "valence": p.valence_name,
                }
                for p in parsed_codes
            ]
            return {
                "word": word,
                "found": True,
                "sense_count": len(codes),
                "codes": codes,
            }
        else:
            primary = enc.get_primary_parsed(word)
            return {
                "word": word,
                "found": True,
                "code": primary.raw,
                "superclass": primary.superclass,
                "synset_id": primary.synset_id,
                "pos": primary.pos_name,
                "abstractness": primary.abstractness_name,
                "valence": primary.valence_name,
            }

    except Exception as e:
        return {"word": word, "error": str(e)}


@mcp.tool()
def analyze_text(text: str, min_word_length: int = 3) -> dict:
    """
    Analyze the valence/sentiment of a text string.

    Extracts words from the text, looks up their valence in the Oyemi
    lexicon, and computes an overall sentiment score. No external
    NLP dependencies required.

    Args:
        text: The text to analyze
        min_word_length: Minimum word length to include (default: 3)

    Returns:
        Dictionary with valence breakdown, score, and word lists

    Example:
        analyze_text("I feel hopeful but anxious about the future")
        -> Returns score, positive words (hopeful), negative words (anxious), etc.
    """
    try:
        enc = get_encoder()
        result = enc.analyze_text(text, min_word_length)

        return {
            "text": text[:200] + "..." if len(text) > 200 else text,
            "total_words": result.total_words,
            "analyzed_words": result.analyzed_words,
            "valence_score": round(result.valence_score, 4),
            "sentiment": result.sentiment,
            "positive_pct": round(result.positive_pct, 2),
            "negative_pct": round(result.negative_pct, 2),
            "neutral_pct": round(result.neutral_pct, 2),
            "positive_words": result.positive_words[:20],  # Limit for response size
            "negative_words": result.negative_words[:20],
            "neutral_words": result.neutral_words[:10],
            "unknown_words": result.unknown_words[:10],
        }

    except Exception as e:
        return {"text": text[:100], "error": str(e)}


@mcp.tool()
def semantic_similarity(word1: str, word2: str) -> dict:
    """
    Calculate semantic similarity between two words.

    Uses Oyemi's code-based distance calculation to measure how
    similar two words are semantically. Also checks for antonym
    relationships.

    Args:
        word1: First word
        word2: Second word

    Returns:
        Dictionary with similarity score (0-1), distance, and relationship info

    Example:
        semantic_similarity("happy", "joyful")
        -> Returns high similarity (~0.85)

        semantic_similarity("happy", "sad")
        -> Returns low similarity (~0.1, detected as antonyms)
    """
    try:
        from Oyemi import semantic_similarity as sim_func, word_distance, are_antonyms

        enc = get_encoder()

        # Check if words exist
        if not enc.contains(word1):
            return {"error": f"Word '{word1}' not found in lexicon"}
        if not enc.contains(word2):
            return {"error": f"Word '{word2}' not found in lexicon"}

        # Get similarity
        similarity = sim_func(word1, word2)
        distance, result = word_distance(word1, word2)

        # Check antonyms
        is_antonym = are_antonyms(word1, word2)

        response = {
            "word1": word1,
            "word2": word2,
            "similarity": round(similarity, 4),
            "distance": round(distance, 4),
            "is_antonym": is_antonym,
        }

        if result:
            response["shared_superclass"] = result.shared_superclass
            response["same_pos"] = result.same_pos

        # Interpretation
        if is_antonym:
            response["relationship"] = "antonyms"
        elif similarity >= 0.8:
            response["relationship"] = "very similar"
        elif similarity >= 0.6:
            response["relationship"] = "related"
        elif similarity >= 0.4:
            response["relationship"] = "somewhat related"
        else:
            response["relationship"] = "unrelated"

        return response

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def find_synonyms(word: str, limit: int = 10) -> dict:
    """
    Find synonyms for a word.

    Uses WordNet synset matching to find true synonyms (words that
    share the same synset). Filters by part of speech and abstractness.

    Args:
        word: The word to find synonyms for
        limit: Maximum number of synonyms to return (default: 10)

    Returns:
        Dictionary with list of synonyms

    Example:
        find_synonyms("happy")
        -> Returns ["glad", "felicitous", "well-chosen", ...]
    """
    try:
        enc = get_encoder()

        if not enc.contains(word):
            return {
                "word": word,
                "found": False,
                "error": f"Word '{word}' not found in lexicon"
            }

        synonyms = enc.find_synonyms(word, limit=limit)

        return {
            "word": word,
            "found": True,
            "synonyms": synonyms,
            "count": len(synonyms),
        }

    except Exception as e:
        return {"word": word, "error": str(e)}


@mcp.tool()
def find_antonyms(word: str) -> dict:
    """
    Find antonyms for a word.

    Returns words that are antonyms according to WordNet.

    Args:
        word: The word to find antonyms for

    Returns:
        Dictionary with list of antonyms

    Example:
        find_antonyms("happy")
        -> Returns ["unhappy", "sad", ...]
    """
    try:
        enc = get_encoder()

        if not enc.contains(word):
            return {
                "word": word,
                "found": False,
                "error": f"Word '{word}' not found in lexicon"
            }

        antonyms = enc.get_antonyms(word)

        return {
            "word": word,
            "found": True,
            "antonyms": antonyms,
            "count": len(antonyms),
        }

    except Exception as e:
        return {"word": word, "error": str(e)}


@mcp.tool()
def batch_encode(words: list[str]) -> dict:
    """
    Encode multiple words at once.

    Efficiently process multiple words in a single call.

    Args:
        words: List of words to encode

    Returns:
        Dictionary with results for each word

    Example:
        batch_encode(["happy", "sad", "neutral"])
        -> Returns codes and valence for each word
    """
    try:
        enc = get_encoder()

        results = []
        for word in words[:100]:  # Limit to 100 words
            if enc.contains(word):
                parsed = enc.get_primary_parsed(word)
                results.append({
                    "word": word,
                    "found": True,
                    "code": parsed.raw,
                    "valence": parsed.valence_name,
                    "pos": parsed.pos_name,
                })
            else:
                results.append({
                    "word": word,
                    "found": False,
                })

        found_count = sum(1 for r in results if r["found"])

        return {
            "total": len(words),
            "processed": len(results),
            "found": found_count,
            "results": results,
        }

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_lexicon_info() -> dict:
    """
    Get information about the Oyemi lexicon.

    Returns statistics about the loaded lexicon including word count,
    mapping count, and version information.

    Returns:
        Dictionary with lexicon statistics
    """
    try:
        from Oyemi import __version__

        enc = get_encoder()

        return {
            "name": "Oyemi",
            "version": __version__,
            "word_count": enc.word_count,
            "mapping_count": enc.mapping_count,
            "code_format": "HHHH-LLLLL-P-A-V",
            "code_description": {
                "HHHH": "Semantic superclass (4 digits)",
                "LLLLL": "Local synset ID (5 digits)",
                "P": "Part of speech (1=noun, 2=verb, 3=adj, 4=adv)",
                "A": "Abstractness (0=concrete, 1=mixed, 2=abstract)",
                "V": "Valence (0=neutral, 1=positive, 2=negative)",
            },
            "features": [
                "Deterministic encoding (same word always returns same code)",
                "Valence/sentiment analysis",
                "Semantic similarity measurement",
                "Synonym and antonym lookup",
                "Zero runtime NLP dependencies",
            ],
        }

    except Exception as e:
        return {"error": str(e)}


def main():
    """Run the Oyemi MCP server."""
    print("Oyemi MCP Server starting...", file=sys.stderr)

    try:
        enc = get_encoder()
        print(f"Lexicon loaded: {enc.word_count:,} words", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not load lexicon: {e}", file=sys.stderr)

    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
