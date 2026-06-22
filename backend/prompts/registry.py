import os
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "templates"

class PromptRegistry:
    @staticmethod
    def get_template(name: str, version: int = 1) -> str:
        """
        Reads a prompt template file by name and version.
        Example: get_template("domain_analysis", 1) loads templates/domain_analysis_v1.txt
        """
        filename = f"{name}_v{version}.txt"
        filepath = PROMPTS_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Prompt template not found at {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def format_prompt(cls, name: str, version: int = 1, **kwargs) -> str:
        """
        Loads and formats a template with provided keyword arguments.
        """
        template = cls.get_template(name, version)
        return template.format(**kwargs)
