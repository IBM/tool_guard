from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.get_files import sharepoint_get_files


def test_sharepoint_get_files() -> None:
    """Tests that the get_files gets the successfull."""

    test_data = {
        "site_id": "wxodomains.sharepoint.com,b8613266-b0a3-40d0-98ce-3b27481881b9,ec0156ed-2431-46c2-8a51-9a590ff910f6",
        "file_id": "01JHX3AJRIM7E7MMSA2NE2SPJHQCJLK4T5",
        "file_name": "Document12.docx",
        "file_path_url": "Document12.docx",
        "web_url": "https://wxodomains.sharepoint.com/sites/wxosupport/_layouts/15/Doc.aspx?sourcedoc=%7BF6C96728-4032-49D3-A93D-278092B5727D%7D&file=Document.docx&action=default&mobileredirect=true",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.get_files.get_microsoft_client"
    ) as magic_sharepoint_client:
        # Create a mock client instance
        mock_client = MagicMock()
        magic_sharepoint_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["file_id"],
                    "name": test_data["file_name"],
                    "webUrl": test_data["web_url"],
                    "file": {"childCount": 0},
                }
            ]
        }

        # Call the function
        response = sharepoint_get_files(site_id=test_data["site_id"])

        assert response

        assert response.files[0].file_id == test_data["file_id"]
        assert response.files[0].file_name == test_data["file_name"]
        assert response.files[0].file_path_url == test_data["file_path_url"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"/sites/{test_data["site_id"]}/drive/items",
            params={"$filter": "item", "$top": 50},
        )
