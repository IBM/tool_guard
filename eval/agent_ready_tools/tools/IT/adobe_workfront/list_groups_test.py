from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_groups import list_groups


def test_list_groups() -> None:
    """Verify that the `list_groups` tool can successfully retrieve Adobe Workfront groups."""

    # Define test data:
    test_data = {
        "group_id": "67e31bf000039691906bcb89410a7f65",
        "group_name": "Apptio Data team",
        "group_description": "Apptio Data team",
        "object_code": "GROUP",
        "public_visibility": False,
    }
    limit = 100
    skip = 0

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_groups.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["group_id"],
                    "name": test_data["group_name"],
                    "objCode": test_data["object_code"],
                    "description": test_data["group_description"],
                    "isPublic": test_data["public_visibility"],
                }
            ]
        }

        # List groups of adobe workfront
        response = list_groups(group_name=test_data["group_name"]).groups[0]

        # Ensure that list_groups() executed and returned proper values
        assert response
        assert response.group_id == test_data["group_id"]
        assert response.group_name == test_data["group_name"]
        assert response.group_description == test_data["group_description"]
        assert response.public_visibility == test_data["public_visibility"]
        assert response.object_code == test_data["object_code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="group/search",
            params={
                "name": test_data["group_name"],
                "$$LIMIT": limit,
                "$$FIRST": skip,
            },
        )
