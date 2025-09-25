from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.get_folders import sharepoint_get_folders


def test_sharepoint_get_folders() -> None:
    """Tests that the get_folders gets the successfull."""

    test_data = {
        "site_id": "wxodomains.sharepoint.com,b8613266-b0a3-40d0-98ce-3b27481881b9,ec0156ed-2431-46c2-8a51-9a590ff910f6",
        "folder_id": "01JHX3AJTZ3OGMKKNX7VBJCYYS3PQGC6RB",
        "folder_name": "Test_Folder_1",
        "folder_path_url": "/Test_Folder_1",
        "web_url": "https://wxodomains.sharepoint.com/sites/wxosupport/Shared%20Documents/Test_Folder_1",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.get_folders.get_microsoft_client"
    ) as magic_sharepoint_client:
        # Create a mock client instance
        mock_client = MagicMock()
        magic_sharepoint_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["folder_id"],
                    "name": test_data["folder_name"],
                    "webUrl": test_data["web_url"],
                    "folder": {"childCount": 0},
                }
            ]
        }

        # Call the function
        response = sharepoint_get_folders(site_id=test_data["site_id"])

        assert response

        assert response.folders[0].folder_id == test_data["folder_id"]
        assert response.folders[0].folder_name == test_data["folder_name"]
        assert response.folders[0].folder_path_url == test_data["folder_path_url"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"/sites/{test_data["site_id"]}/drive/items",
            params={"$filter": "item", "$top": 50},
        )
