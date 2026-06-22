from backend.providers.base import LLMProvider

def compute_relevancy(provider: LLMProvider, query: str, response: str) -> float:
    """
    Uses an LLM provider to evaluate how relevant the generated response is to the user query.
    Returns a score between 0.0 (completely irrelevant) and 1.0 (perfectly relevant).
    """
    prompt = f"""
You are an expert evaluator assessing AI assistant responses.
Rate the semantic RELEVANCY of the response to the user query on a scale from 0.0 to 1.0.

- 1.0: The response directly, fully, and accurately answers the query.
- 0.5: The response is partially relevant but misses key aspects or includes off-topic details.
- 0.0: The response is completely irrelevant or off-topic.

Query: {query}
Response: {response}

Output ONLY a single floating-point number representing the score (e.g. 0.85). Do not include code fences, markdown, or text.
"""
    try:
        raw_score = provider.generate(prompt).strip()
        # Parse float, removing any markdown code fences if present
        if raw_score.startswith("```"):
            raw_score = raw_score.split("```")[1]
            if raw_score.startswith("json"):
                raw_score = raw_score[4:]
            raw_score = raw_score.strip()
        score = float(raw_score)
        return max(0.0, min(1.0, score))
    except Exception as e:
        print(f"Error computing relevancy: {e}")
        # Default fallback if the API fails or outputs invalid format
        return 0.5
