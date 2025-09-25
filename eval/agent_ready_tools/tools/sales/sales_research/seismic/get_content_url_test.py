from unittest.mock import MagicMock, patch

from agent_ready_tools.clients.seismic_client import SeismicClient
from agent_ready_tools.tools.sales.sales_research.seismic.get_content_url import (
    GetContentURLResponse,
    get_content_url,
)


def test_get_content_url() -> None:
    """Test that the seismic `get_content_url` function returns the expected response."""

    # Define test data:
    test_data = {
        "workspace_id": "8737594d-2254-4c73-b866-f9a4f810b718",
        "url": "https://newdownload.seismic.com/api/download/v1/blob?t=ibmsandbox&c=ibmsandbox-collaboration&id=",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.seismic.get_content_url.get_seismic_client"
    ) as mock_seismic_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_seismic_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "downloadUrl": f'{test_data["url"]}{test_data["workspace_id"]}'
        }

        # Get workspace content url
        response = get_content_url(test_data["workspace_id"])

        # Ensure that get_all_library_contents() executed and returned proper values
        assert response
        assert isinstance(response, GetContentURLResponse)
        assert response.url
        assert response.url == f'{test_data["url"]}{test_data["workspace_id"]}'

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            category=SeismicClient.INTEGRATION,
            endpoint="workspace",
            custom_path_suffix="/".join(["files", test_data["workspace_id"], "content"]),
            params={
                "redirect": "false",
            },
        )
