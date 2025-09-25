from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.get_all_folders_items import (
    get_all_folders_items,
)


def test_get_all_folders_items() -> None:
    """Verify that the `get_all_folders_items` tool can successfully retrieve items fom
    Sharepoint."""

    folder_test_data = {
        "id": "7981d51f-003e",
        "name": "test_folder",
    }

    file_test_data = {
        "id": "b6b4-08c44a98f1db",
        "name": "test.txt",
    }

    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.get_all_folders_items.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": folder_test_data["id"],
                    "name": folder_test_data["name"],
                },
                {
                    "id": file_test_data["id"],
                    "name": file_test_data["name"],
                },
            ]
        }

        response = get_all_folders_items("https://ibmappcon.sharepoint.com", "1234ab-56")

        assert (
            response
            and response.items[0].id == folder_test_data["id"]
            and response.items[0].name == folder_test_data["name"]
            and response.items[1].id == file_test_data["id"]
            and response.items[1].name == file_test_data["name"]
        )

        mock_client.get_request.assert_called_once_with(
            "/sites/https://ibmappcon.sharepoint.com/drive/items/1234ab-56/children"
        )
