"""
app/ai/agents/testcase_agent.py

LangChain agent responsible for Step 2 of the AI generation pipeline:
generating structured test case definitions from extracted requirements.

Input:  List of structured requirements from RequirementAgent
Output: List of test case dicts (title, description, type, tags, steps)
"""

from typing import List


class TestCaseAgent:
    """
    Generates a structured list of test cases from normalised requirements.

    Produces:
        - Test case title
        - Plain-language description
        - Type (UI | API | Regression)
        - Tags (smoke, regression, auth, etc.)
        - Test steps (Given/When/Then in plain form, pre-BDD)
        - Preconditions
        - Expected outcomes
    """

    def __init__(self, llm=None):
        """
        Args:
            llm: LangChain LLM instance.
        """
        pass

    async def generate(self, requirements: List[dict], options: dict) -> List[dict]:
        """
        Generate a list of test case definitions from requirements.

        Args:
            requirements : Output from RequirementAgent.extract_requirements().
            options      : {test_type, max_cases}

        Returns:
            List[dict]: [
                {
                    "title": str,
                    "description": str,
                    "type": str,
                    "tags": List[str],
                    "preconditions": str,
                    "steps": List[str],
                    "expected_outcome": str
                }
            ]
        """
        pass

    def _build_prompt(self, requirements: List[dict], options: dict) -> str:
        """
        Build the LLM prompt from the testcase_prompt.txt template.
        Injects requirements and generation options as context.
        """
        pass
