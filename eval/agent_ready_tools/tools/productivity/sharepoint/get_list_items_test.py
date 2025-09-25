from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.get_list_items import ListItem, get_list_items


def test_get_list_items() -> None:
    """Tests that the items of a list can be retrieved by the `get_list_items` tool."""

    # Define test data
    test_data = {
        "fields": {
            "Title": "Testing",
            "Active": True,
            "Attachments": False,
        },
        "site_id": "ibmappcon.sharepoint.com,66275c9d-54e5-4869-acb2-e5df23bc8edf,c8610d67-0958-4776-976b-d38877dcb67f",
        "list_name": "Sivasri",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.get_list_items.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {"value": [{"fields": test_data["fields"]}]}

        # Call the function
        response = get_list_items(test_data["site_id"], test_data["list_name"])

        # Verify that the list item matches the expected data
        expected_list_item = ListItem(
            fields={"Title": "Testing", "Active": True, "Attachments": False}
        )

        assert response.list_items[0] == expected_list_item

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"sites/{test_data['site_id']}/lists/{test_data['list_name']}/items",
            params={"expand": "fields"},
        )
