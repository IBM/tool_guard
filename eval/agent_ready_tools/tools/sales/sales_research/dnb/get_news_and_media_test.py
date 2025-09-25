# Assisted by watsonx Code Assistant
# test_get_news_and_media.py
# Import necessary modules and types.
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

# Import the function under test.
from agent_ready_tools.tools.sales.sales_research.dnb.get_news_and_media import (
    MAX_ITEMS,
    NewsItems,
    get_news_and_media,
)


def test_valid_duns_number() -> None:
    """Test that passing a valid duns_number results in a list of no more than 10 news items being
    returned successfully."""

    # Define test data:
    test_data: Dict[str, List[Any]] = {
        "newsItems": [
            {
                "publication_date": "2025-03-31",
                "reportedTimeStamp": "2025-03-31T12:00:00Z",
                "publicationSource": "Test Source",
                "newsCategories": ["Category1"],
                "title": "Test Title",
                "content": "Test Content",
                "referenceURL": "http://example.com/test-news",
            }
        ]
    }
    duns_number = "001368083"

    # Patch the get_dnb_client function in the module where it's imported.
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.get_news_and_media.get_dnb_client"
    ) as mock_get_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_client.get_request.return_value = test_data
        mock_get_dnb_client.return_value = mock_client

        # Call the function with a valid IBM's DUNS number.
        result = get_news_and_media(duns_number=duns_number)

        # Verify that get_request was called exactly once.
        mock_client.get_request.assert_called_once()

        if result is not None and result.data is not None:
            data = result.data
            # Verify that the result is an instance of NewsItems.
            assert isinstance(result, NewsItems)

            # Assert that the result contains a number of NewsItem objects up to MAX_ITEMS.
            assert len(data) <= MAX_ITEMS

            assert data[0].reported_date == test_data["newsItems"][0]["publication_date"]

            # Assert that each attribute of the first NewsItem is not empty.
            assert data[0].news_categories == test_data["newsItems"][0]["newsCategories"]
            assert data[0].title == test_data["newsItems"][0]["title"]
            assert data[0].content == test_data["newsItems"][0]["content"]
            assert data[0].reference_url == test_data["newsItems"][0]["referenceURL"]
