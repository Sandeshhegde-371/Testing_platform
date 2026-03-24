"""
app/ai/agents/requirement_agent.py

LangChain agent responsible for Step 1 of the AI generation pipeline:
extracting structured requirements from raw enriched context.

Input:  Enriched context dict (prompt + Confluence content + Jira description)
Output: Structured list of user stories / requirements

This agent prepares and cleans the context so downstream agents
(TestCaseAgent, BDDAgent, SeleniumAgent) receive high-quality input.
"""

from typing import List


class RequirementAgent:
    """
    Extracts clean, structured requirements from raw mixed input.

    Responsibilities:
        - Deduplication of requirements across Confluence and Jira sources
        - Priority classification (critical | high | medium | low)
        - Scope boundary detection (in-scope vs out-of-scope)
        - Output a list of structured requirement dicts for downstream agents
    """

    def __init__(self, llm=None):
        """
        Args:
            llm: LangChain LLM instance (passed from AIService).
        """
        pass

    async def extract_requirements(self, enriched_context: dict) -> List[dict]:
        """
        Parse enriched context to extract structured requirements.

        Args:
            enriched_context: {prompt_text, confluence_content, jira_description}

        Returns:
            List[dict]: [
                {
                    "id": "REQ-001",
                    "title": str,
                    "description": str,
                    "priority": str,
                    "source": "confluence" | "jira" | "prompt"
                }
            ]
        """
        pass

    def _build_prompt(self, context: dict) -> str:
        """
        Construct the LLM prompt for requirement extraction.
        Loads template from app/ai/prompts/ and injects context.
        """
        pass
