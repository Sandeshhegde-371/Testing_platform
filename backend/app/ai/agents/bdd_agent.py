"""
app/ai/agents/bdd_agent.py

LangChain agent responsible for Step 3 of the AI generation pipeline:
generating Gherkin BDD scenarios for each test case.

Input:  List of structured test case dicts from TestCaseAgent
Output: Gherkin feature file content (Feature + Scenario blocks) per test case
"""

from typing import List


class BDDAgent:
    """
    Converts structured test cases into Gherkin BDD feature files.

    Output format:
        Feature: <test case title>
          Scenario: <scenario name>
            Given <precondition>
            When  <action>
            Then  <expected outcome>
            And   <additional assertion>  # optional
    """

    def __init__(self, llm=None):
        """
        Args:
            llm: LangChain LLM instance.
        """
        pass

    async def generate(self, test_case: dict) -> str:
        """
        Generate a Gherkin feature file for a single test case.

        Args:
            test_case: Structured test case dict from TestCaseAgent.

        Returns:
            str: Gherkin feature file content.
        """
        pass

    async def generate_batch(self, test_cases: List[dict]) -> List[str]:
        """
        Generate Gherkin content for a list of test cases concurrently.

        Args:
            test_cases: List of structured test case dicts.

        Returns:
            List[str]: Gherkin feature content per test case (same order).
        """
        pass

    def _build_prompt(self, test_case: dict) -> str:
        """
        Build the LLM prompt using bdd_prompt.txt template.
        Injects test case title, description, steps, and expected outcome.
        """
        pass

    def _validate_gherkin(self, content: str) -> bool:
        """
        Basic structural validation of generated Gherkin.
        Checks that Feature and at least one Scenario block are present.
        """
        pass
