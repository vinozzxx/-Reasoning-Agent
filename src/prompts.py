
# src/prompts.py
from pathlib import Path

def load_prompt(filename: str) -> str:
    """
    Loads a prompt template from the prompts/ folder.
    """
    base = Path(__file__).parents[1] / "prompts" / filename
    if not base.exists():
        raise FileNotFoundError(f"Prompt file not found: {base}")
    return base.read_text(encoding="utf-8")


# Preload all prompts here
planner_prompt = load_prompt("planner_prompt.txt")
executor_prompt = load_prompt("executor_prompt.txt")
verifier_prompt = load_prompt("verifier_prompt.txt")
