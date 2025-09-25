from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.add_list_item import add_list_item


def test_add_list_item() -> None:
    """Test that an item has been added to a list successfully in Microsoft Sharepoint using the
    `add_list_item` tool."""

    # Define test data:
    test_data = {
        "site_id": "ibmappcon.sharepoint.com,0ca33b1e-0e6c-4732-a347-85f18a01c33c,1f54f7f0-fbb0-46f2-afa4-22ff2f93cbba",
        "list_id": "c98136a8-737c-4afd-af07-ebd9e78da6b4",
        "title": "New Book Test 9",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.add_list_item.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {"fields": {"Title": test_data["title"]}}

        # Add list item
        response = add_list_item(
            title=test_data["title"],
            site_id=test_data["site_id"],
            list_id=test_data["list_id"],
        )

        # Ensure that add_list_item() executed and returned proper values
        assert response
        assert response.title == test_data["title"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"sites/{test_data['site_id']}/lists/{test_data['list_id']}/items",
            data={"fields": {"Title": test_data["title"]}},
        )
