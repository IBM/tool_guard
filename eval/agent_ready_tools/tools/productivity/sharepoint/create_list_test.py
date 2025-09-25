from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.create_list import create_list


def test_create_list() -> None:
    """Verifies that the `create_list` tool can successfully create a list in Microsoft
    SharePoint."""

    # Define test data:
    test_data = {
        "site_id": "ibmappcon.sharepoint.com,2ca6fa25-e7c7-4a8f-9631-6714acca7c31,1f54f7f0-fbb0-46f2-afa4-22ff2f93cbba",
        "display_name": "Listingmock1",
        "description": "this is list description3",
        "list_name": "Listingmock1",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.create_list.get_microsoft_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.post_request.return_value = {"displayName": test_data["list_name"]}

        # Create Microsoft SharePoint list
        response = create_list(
            site_id=test_data["site_id"],
            display_name=test_data["display_name"],
            description=test_data["description"],
        )

        # Ensure that create_list() executed and returned proper values
        assert response
        assert response.list_name == test_data["list_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"sites/{test_data['site_id']}/lists",
            data={
                "displayName": test_data["display_name"],
                "description": test_data["description"],
            },
        )
