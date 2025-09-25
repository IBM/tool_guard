from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.ibm_planning_analytics_client import IBMPlanningAnalyticsClient


@patch("requests.get")
def test_ibm_pa_client_basic_auth(mock_get: MagicMock) -> None:
    """
    Test that the `IBMPlanningAnalyticsClient` is working as expected. Test
    `IBMPlanningAnalyticsClient._fetch_session_token` with mocked `requests.get`.

    Args:
        mock_get: The mock object for the requests.get function
    """

    # Define mock API response data
    cookies = {
        "paSession": "s%3AeUf1SKlKuFIdOXYPQNuSAR7wb3JfVT2W.m7KviYcZaZRWg4yT6VXjiOwPRuyz2a3Xvk0oR26WPHc",
        "SameSite": "None",
    }

    # Create a mock response instance for API requests
    mock_client_response = MagicMock()
    mock_client_response.cookies = MagicMock()
    mock_client_response.cookies.get_dict.return_value = cookies
    mock_client_response.status_code = 200  # Ensure no HTTP error
    mock_client_response.raise_for_status = MagicMock()  # Prevent raising errors
    mock_get.return_value = mock_client_response

    # Call the IBM PA client, _fetch_session_token is called implicitly in the initializer.
    client: IBMPlanningAnalyticsClient = IBMPlanningAnalyticsClient(
        base_url="", username="", password="", tenant_id="", model_name="", version=""
    )

    # Ensure that _fetch_session_token() executed and returned proper values
    assert client.pa_session == cookies["paSession"]
