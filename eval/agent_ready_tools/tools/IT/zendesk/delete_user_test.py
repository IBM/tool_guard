from unittest.mock import MagicMock, patch

from requests.exceptions import HTTPError
from requests.models import Response

from agent_ready_tools.tools.IT.zendesk.delete_user import delete_user


def test_delete_user() -> None:
    """Tests that a user can be successfully deleted by the `delete_user` tool."""

    # Define test data:
    test_data = {
        "user_id": "1809734598969",
        "user_name": "testgo",
        "active_status": False,
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.delete_user.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.delete_request.return_value = {
            "user": {
                "name": test_data["user_name"],
                "active": test_data["active_status"],
            }
        }

        # Delete user
        response = delete_user(test_data["user_id"])

        # Ensure that delete_user() executed and returned proper values
        assert response
        assert response.user_name == test_data["user_name"]
        assert response.active_status == test_data["active_status"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(entity=f"users/{test_data['user_id']}")


def test_delete_user_exception() -> None:
    """Tests that the delete_user tool handles HTTPError exceptions properly."""

    # Define test data:
    test_data = {
        "user_id": "1809734598969",
        "error_title": "Invalid attribute",
        "error_message": "You do not have permission to delete this user",
        "http_code": 403,
    }

    # Create a mock response object
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = test_data["http_code"]
    mock_response.json.return_value = {
        "error": {
            "title": test_data["error_title"],
            "message": test_data["error_message"],
        }
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.delete_user.get_zendesk_client"
    ) as mock_zendesk_error_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_error_client.return_value = mock_client
        mock_client.delete_request.side_effect = HTTPError(response=mock_response)

        # Delete user
        response = delete_user(user_id=test_data["user_id"])

        # Ensure that delete_user() executed and returned proper values
        assert response
        assert response.error_message == test_data["error_title"]
        assert response.error_description == test_data["error_message"]
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(entity=f"users/{test_data['user_id']}")
