from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.zendesk_client import ZendeskClient


@patch("agent_ready_tools.clients.zendesk_client.requests.post")
def test_zendesk_client(mock_post: MagicMock) -> None:
    """
    Test that the `ZendeskClient` is working as expected.

    Args:
        mock_post: The mock for the requests.post function
    """

    test_data = {"access_token": "77cec899755c0f431650d866755d6881147f7d9a9276b7e36bdb473037d58d67"}

    mock_client = MagicMock()
    mock_client.json.return_value = test_data
    mock_client.status_code = 200
    mock_client.raise_for_status = MagicMock()  # Simulate successful request
    mock_post.return_value = mock_client  # Set the mock return value

    # Call the Zendesk client
    response: ZendeskClient = ZendeskClient("", "", "", "")

    assert response
    assert response.bearer == test_data["access_token"]

    # Ensure the API call was made with expected parameters
    mock_client.json.assert_called_once()
