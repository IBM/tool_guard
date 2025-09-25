from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.google_drive.create_a_folder_google_drive import (
    create_a_folder_google_drive,
)


def test_create_a_folder() -> None:
    """Verifies that the `create_a_folder` tool can successfully create a folder in Google Drive."""

    # Define test data
    test_data = {
        "folder_name": "Sharan Folder1",
        "description": "This is a Sharan Folder1",
    }

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.google_drive.create_a_folder_google_drive.get_google_client"
    ) as mock_google_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_google_client.return_value = mock_client
        mock_client.post_request.return_value = {"name": test_data["folder_name"]}

        # Create a team channel
        response = create_a_folder_google_drive(
            folder_name=test_data["folder_name"],
            description=test_data["description"],
        )

        # Ensure that create_a_folder() executed and returned proper values
        assert response
        assert response.folder_name == test_data["folder_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="files",
            payload={
                "name": test_data["folder_name"],
                "description": test_data["description"],
                "parents": [None],
                "mimeType": "application/vnd.google-apps.folder",
            },
        )


def test_create_a_child_folder() -> None:
    """Verifies that the `create_a_folder` tool can successfully create a folder under parent folder
    in Google Drive."""

    # Define test data
    test_data = {
        "folder_name": "Sharan Folder2",
        "description": "This is a Sharan Folder2",
        "parent_id": "1HNzV02R9doV-BPe45g-D7-p03je4ZJAm",
    }

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.google_drive.create_a_folder_google_drive.get_google_client"
    ) as mock_google_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_google_client.return_value = mock_client
        mock_client.post_request.return_value = {"name": test_data["folder_name"]}

        # Create a team channel
        response = create_a_folder_google_drive(
            folder_name=test_data["folder_name"],
            description=test_data["description"],
            parent_id=test_data["parent_id"],
        )

        # Ensure that create_a_folder() executed and returned proper values
        assert response
        assert response.folder_name == test_data["folder_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="files",
            payload={
                "name": test_data["folder_name"],
                "description": test_data["description"],
                "parents": [test_data["parent_id"]],
                "mimeType": "application/vnd.google-apps.folder",
            },
        )
