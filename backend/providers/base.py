class LLMProvider:
    def generate(self, prompt: str) -> str:
        """
        Generates text output for the given text prompt.
        """
        raise NotImplementedError("LLMProvider subclasses must implement the generate method.")
