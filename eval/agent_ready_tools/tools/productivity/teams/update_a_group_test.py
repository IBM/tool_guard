from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.update_a_group import update_a_group


def test_update_a_group() -> None:
    """Verifies that the `update_a_group` tool updates the group details in Microsoft Teams."""

    # Define test data:
    test_data = {
        "original_group_id": "8b3d3f0c-d94b-4a3a-8c1a-3f0d7262a9d0",
        "new_group_name": "Test group",
        "new_group_description": "Test description",
        "http_code": 204,
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.update_a_group.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.update_request.return_value = {"status_code": test_data["http_code"]}

        # Update a group
        response = update_a_group(
            original_group_id=test_data["original_group_id"],
            new_group_name=test_data["new_group_name"],
            new_group_description=test_data["new_group_description"],
        )

        # Ensure that update_a_group() executed and returned proper values
        assert response
        assert response.http_code == 204

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            endpoint=f"groups/{test_data['original_group_id']}",
            data={
                "displayName": test_data["new_group_name"],
                "description": test_data["new_group_description"],
            },
        )


def test_fail_update_a_group() -> None:
    """Verifies that the `update_a_group` tool shows the result for invalid data in Microsoft
    Teams."""

    # Define test data:
    test_data = {
        "original_group_id": "8b3d3f0c-d94b-4a3a-8c1a-3f0d7262a9d1",  # invalid data
        "new_group_name": "Test group",
        "new_group_description": "Test description",
        "http_code": 404,
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.update_a_group.get_microsoft_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.update_request.return_value = {"status_code": test_data["http_code"]}

        # Update a group
        response = update_a_group(
            original_group_id=test_data["original_group_id"],
            new_group_name=test_data["new_group_name"],
            new_group_description=test_data["new_group_description"],
        )

        # Ensure that update_a_group() executed and returned proper values
        assert response
        assert response.http_code == 404

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            endpoint=f"groups/{test_data['original_group_id']}",
            data={
                "displayName": test_data["new_group_name"],
                "description": test_data["new_group_description"],
            },
        )
