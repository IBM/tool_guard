from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_group_owners import get_group_owners


def test_get_group_owners() -> None:
    """Verify that the `get_group_owners` tool can successfully retrieve group owners fom Teams."""

    test_data = {
        "id": "123ab-456cd",
        "display_name": "test group",
        "user_principal_name": "principal name",
        "account_enabled": True,
    }

    with patch(
        "agent_ready_tools.tools.productivity.teams.get_group_owners.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": "123ab-456cd",
                    "displayName": "test group",
                    "accountEnabled": True,
                    "userPrincipalName": "principal name",
                }
            ]
        }

        response = get_group_owners("123ab-456cd")

        assert (
            response
            and response.owners[0].id == test_data["id"]
            and response.owners[0].display_name == test_data["display_name"]
            and response.owners[0].user_principal_name == test_data["user_principal_name"]
            and response.owners[0].account_enabled == test_data["account_enabled"]
        )

        mock_client.get_request.assert_called_once_with("groups/123ab-456cd/owners")
