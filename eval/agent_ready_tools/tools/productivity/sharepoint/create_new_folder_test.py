from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.create_new_folder import create_new_folder


def test_create_new_folder() -> None:
    """Verify that the `create_new_folder` tool can successfully create a new folder in Microsoft
    Sharepoint."""

    # Define test data:
    test_data = {
        "site_id": "ibmappcon.sharepoint.com,0ca33b1e-0e6c-4732-a347-85f18a01c33c,1f54f7f0-fbb0-46f2-afa4-22ff2f93cbba",
        "parent_folder_id": "01KOJQNEAAPWKOGIIW3VDKUZYDQKPQYHF2",
        "folder_name": "Rahul_Test_Folder_9",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.create_new_folder.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {"name": test_data["folder_name"]}

        # Create new folder
        response = create_new_folder(
            site_id=test_data["site_id"],
            parent_folder_id=test_data["parent_folder_id"],
            folder_name=test_data["folder_name"],
        )

        # Ensure that create_new_folder() was executed and returned correct values
        assert response
        assert response.folder_name == test_data["folder_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint=f"sites/{test_data["site_id"]}/drive/items/{test_data["parent_folder_id"]}/children",
            data={
                "name": test_data["folder_name"],
                "folder": {},
                "@microsoft.graph.conflictBehavior": "rename",
            },
        )
