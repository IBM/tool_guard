from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.create_group import create_group


def test_create_group() -> None:
    """Verifies that the `create_group` tool can successfully creates a group in Zendesk."""

    # Define test data
    test_data = {
        "group": {"group_name": "Watson Test", "description": "sample test data", "is_public": True}
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.create_group.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "group": {
                "name": test_data["group"]["group_name"],
                "description": test_data["group"]["description"],
                "is_public": test_data["group"]["is_public"],
            }
        }

        # Create a group
        response = create_group(
            group_name=test_data["group"]["group_name"],
            description=test_data["group"]["description"],
            is_public=test_data["group"]["is_public"],
        )

        # Ensure that create_group() executed and returned proper values
        assert response
        assert response.group_name == test_data["group"]["group_name"]
        assert response.description == test_data["group"]["description"]
        assert response.is_public == test_data["group"]["is_public"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="groups",
            payload={
                "group": {
                    "name": test_data["group"]["group_name"],
                    "description": test_data["group"]["description"],
                    "is_public": test_data["group"]["is_public"],
                }
            },
        )
