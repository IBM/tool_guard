from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.outlook.get_organizations import get_organizations


def test_get_organizations() -> None:
    """Verify that the `get_organizations` tool can successfully return a list of organizations from
    Outlook event."""

    # Define test data:
    test_data = {"id": "0195ea87-1839-4df0-9739-bf7eec6de925", "name": "test_org"}

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_organizations.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["id"],
                    "displayName": test_data["name"],
                }
            ]
        }

        # Get Organizations
        response = get_organizations()

        # Ensure that get_organizations() executed and returned proper values
        assert response
        assert len(response.organizations)
        assert response.organizations[0].id == test_data["id"]
        assert response.organizations[0].name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with("organization")
