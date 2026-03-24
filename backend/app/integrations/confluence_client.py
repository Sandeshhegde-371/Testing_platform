"""
app/integrations/confluence_client.py

HTTP client for the Atlassian Confluence REST API.

Responsibilities:
    - Fetch Confluence page content by URL or page ID
    - Convert Confluence storage format (XHTML) to plain text for LLM input
    - Handle authentication via API token

Usage:
    client = ConfluenceClient()
    content = await client.get_page_content("https://org.atlassian.net/wiki/spaces/ENG/pages/123456")
"""


class ConfluenceClient:
    """
    Async HTTP client for Confluence REST API v2.
    Converts page content to plain text for AI context injection.
    """

    def __init__(self):
        """Initialise with base_url, user_email, and api_token from settings."""
        pass

    async def get_page_by_url(self, page_url: str) -> dict:
        """
        Resolve a Confluence page URL to its content.

        Steps:
            1. Extract space key and page title from URL.
            2. Call Confluence API to fetch page by title.
            3. Convert storage-format body to plain text.

        Args:
            page_url: Full Confluence page URL.

        Returns:
            dict: {title, plain_text_content, url, space_key, page_id}
        """
        pass

    async def get_page_by_id(self, page_id: str) -> dict:
        """
        Fetch a Confluence page by its numeric ID.

        Returns:
            dict: {title, plain_text_content, url}
        """
        pass

    def _storage_to_plain_text(self, storage_html: str) -> str:
        """
        Convert Confluence storage format (XML/XHTML) to clean plain text
        suitable for LLM context injection.

        Args:
            storage_html: Raw storage format body from Confluence API.

        Returns:
            str: Stripped plain text.
        """
        pass
