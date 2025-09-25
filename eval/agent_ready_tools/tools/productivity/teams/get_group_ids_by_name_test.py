from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_group_ids_by_name import get_group_ids_by_name


def test_get_group_ids_by_name() -> None:
    """Verify that the `get_group_ids_by_name` tool can successfully retrieve group ids fom
    Teams."""

    test_data = {"id": "123ab-456cd", "display_name": "test group"}

    with patch(
        "agent_ready_tools.tools.productivity.teams.get_group_ids_by_name.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": "123ab-456cd",
                    "displayName": "test group",
                }
            ]
        }

        response = get_group_ids_by_name("test group")

        assert response and response.ids[0] == test_data["id"]

        mock_client.get_request.assert_called_once_with(
            "groups?$filter=displayName eq 'test group'"
        )
