from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.seismic_client import SeismicClient


@patch("agent_ready_tools.clients.seismic_client.requests.post")
def test_seismic_client(mock_client: MagicMock) -> None:
    """
    Test that the `SeismicClient` is working as expected. Test `SeismicClient.get_request` with
    mocked requests.post.

    Args:
        mock_client: The mock for the requests.post function.
    """

    # Define mock API test data
    token_response = {"access_token": "NmUzYWM4MWYxMDAwMTZl"}
    test_data = {
        "endpoint": "generative",
        "category": "search",
        "version": "v1",
    }
    api_response = {"result": "success"}

    # Create a mock instance for API requests
    mock_client.return_value = MagicMock()
    mock_client.return_value.json.return_value = token_response
    mock_client.return_value.status_code = 200
    mock_client.return_value.raise_for_status = MagicMock()

    # Call the SeismicClient client
    client = SeismicClient("", "", "", "", "")

    # Ensure that SeismicClient() executed and returned proper values
    # Ensure that the bearer token was set correctly
    assert client.headers["Authorization"] == f"Bearer {token_response['access_token']}"

    # Define mock API response data for a normal request
    mock_client.return_value.json.return_value = api_response

    # Call post_request function from SeismicClient
    response = client.post_request(
        endpoint=test_data["endpoint"], category=test_data["category"], version=test_data["version"]
    )

    # Ensure that post_request() executed and returned proper values
    assert response == api_response

    # Ensure the API call was made with expected parameters
    mock_client.assert_called_with(
        url=f"{client.base_url}/{test_data['category']}/{test_data['version']}/{test_data['endpoint']}",
        headers=client.headers,
        json=None,
        params={"$format": "JSON"},
    )
