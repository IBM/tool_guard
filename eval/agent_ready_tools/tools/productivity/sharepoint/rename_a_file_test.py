from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.rename_a_file import rename_a_file


def test_rename_a_file() -> None:
    """Verifies that the `rename_a_file` tool can successfully rename a Microsoft SharePoint
    file."""

    # Define test data:
    test_data = {
        "site_id": "ibmappcon.sharepoint.com,0ca33b1e-0e6c-4732-a347-85f18a01c33c,1f54f7f0-fbb0-46f2-afa4-22ff2f93cbba",
        "file_id": "3272145F-8F60-4648-AB11-70FFF110AD15",
        "new_file_name": "Naga.docx",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.rename_a_file.get_microsoft_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "name": test_data["new_file_name"],
        }

        # Rename a file
        response = rename_a_file(
            site_id=test_data["site_id"],
            file_id=test_data["file_id"],
            new_file_name=test_data["new_file_name"],
        )

        # Ensure that rename_a_file() executed and returned proper values
        assert response
        assert response.new_file_name == test_data["new_file_name"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            endpoint=f"sites/{test_data['site_id']}/drive/items/{test_data['file_id']}",
            data={
                "name": test_data["new_file_name"],
            },
        )
