from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.get_contact_folders import (
    ContactFolder,
    get_contact_folders,
)


def test_get_contact_folders_first_item() -> None:
    """Tests that the first contact folder in the response matches the expected data."""

    # Define test data with explicit type annotation
    test_data: dict[str, str] = {
        "contact_folder_id": "AAMkADYyODVkMjM5LTFlZTctNGYxZi1hOGM4LWFiZjYyNzlkMT",
        "contact_folder_name": " ",
        "user_name": "user@example.com",
    }
    limit = 3
    skip = 1
    output_limit = 3
    output_skip = 4

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_contact_folders.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["contact_folder_id"],
                    "displayName": test_data["contact_folder_name"],
                }
            ],
            "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/contactFolders?%24top=3&%24skip=4",
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data["user_name"]}"

        # Call the function
        response = get_contact_folders(limit=limit, skip=skip)
        # Verify that the first contact folder matches the expected data
        expected_first_contact_folder = ContactFolder(
            contact_folder_id=test_data["contact_folder_id"],
            contact_folder_name=test_data["contact_folder_name"],
        )
        assert response.contact_folders[0] == expected_first_contact_folder
        assert response.limit == output_limit
        assert response.skip == output_skip

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            f"users/{test_data["user_name"]}/contactFolders", params={"$top": limit, "$skip": skip}
        )
