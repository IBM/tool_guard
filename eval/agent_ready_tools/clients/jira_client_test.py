from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.jira_client import JiraClient


@patch("agent_ready_tools.clients.jira_client.requests.get")
def test_jira_client(mock_client: MagicMock) -> None:
    """
    Test that the `JiraClient` is working as expected. Test `JiraClient.get_request` with mocked
    `requests.get`.

    Args:
        mock_client: The mock for the requests.get function
    """

    # Define mock API response data
    test_data = {"entity_data": "NmUzYWM4MWYxMDAwMTZl", "entity": "test-entity"}

    # Create a mock instance for API requests
    mock_client.return_value = MagicMock()
    mock_client.return_value.json.return_value = test_data
    mock_client.return_value.status_code = 200  # Ensure no HTTP error
    mock_client.return_value.raise_for_status = MagicMock()  # Prevent raising errors

    # Call the Jira client
    client: JiraClient = JiraClient("", "", "")

    # Call get_request function from Jira client
    response = client.get_request(entity=test_data["entity"])

    # Ensure that get_request() executed and returned proper values
    assert response
    assert response["entity_data"] == test_data["entity_data"]
    mock_client.assert_called_once()
