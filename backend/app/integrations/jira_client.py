"""
app/integrations/jira_client.py

HTTP client for the Atlassian Jira REST API.

Responsibilities:
    - Fetch Jira issue details (summary, description, acceptance criteria)
    - Search for issues by JQL query
    - Authenticate using API token (Basic auth via base64)

Usage:
    client = JiraClient()
    issue = await client.get_issue("ESHOP-4521")
"""


class JiraClient:
    """
    Async HTTP client for Jira REST API v3.
    Base URL and credentials loaded from settings.
    """

    def __init__(self):
        """Initialise with base_url, user_email, and api_token from settings."""
        pass

    async def get_issue(self, ticket_key: str) -> dict:
        """
        Fetch a Jira issue by key.

        Args:
            ticket_key: Jira issue key (e.g. "ESHOP-4521").

        Returns:
            dict: {summary, description, acceptance_criteria, labels, priority}

        Raises:
            IntegrationError: If Jira returns 401 / 404 / 429 / 5xx.
        """
        pass

    async def search_issues(self, jql: str, max_results: int = 50) -> list:
        """
        Search Jira issues using JQL.

        Args:
            jql        : JQL query string.
            max_results: Maximum number of issues to return.

        Returns:
            list[dict]: List of simplified issue dicts.
        """
        pass

    async def get_project_info(self, project_key: str) -> dict:
        """
        Fetch basic metadata about a Jira project.

        Returns:
            dict: {key, name, description, lead}
        """
        pass
