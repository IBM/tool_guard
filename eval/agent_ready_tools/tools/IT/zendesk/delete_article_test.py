from unittest.mock import MagicMock, patch

from requests import HTTPError
from requests.models import Response

from agent_ready_tools.tools.IT.zendesk.delete_article import delete_article


def test_delete_article() -> None:
    """Tests that an article can be successfully deleted by the `delete_article` tool."""

    # Define test data:
    test_data = {"article_id": "48498391782297", "http_code": 204}

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.delete_article.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.delete_request.return_value = {"status_code": test_data["http_code"]}

        # Delete article
        response = delete_article(test_data["article_id"])

        # Ensure that delete_article() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity=f"help_center/articles/{test_data['article_id']}"
        )


def test_delete_article_exception() -> None:
    """Tests that an article deletion handles exceptions properly by the `delete_article` tool."""

    # Define test data:
    test_data = {
        "article_id": "48498391782297",
        "error": "RecordNotFound",
        "description": "Not found",
        "http_code": 404,
    }

    # Create a mock response object
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = test_data["http_code"]
    mock_response.json.return_value = {
        "error": test_data["error"],
        "description": test_data["description"],
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.delete_article.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.delete_request.side_effect = HTTPError(response=mock_response)

        # Delete article
        response = delete_article(test_data["article_id"])

        # Ensure that delete_article() executed and returned proper values
        assert response
        assert response.error_message == test_data["error"]
        assert response.error_description == test_data["description"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity=f"help_center/articles/{test_data['article_id']}"
        )
