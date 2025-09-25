from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.get_predefined_case_teams import (
    get_predefined_case_teams,
)
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseTeam


def test_get_predefined_case_teams() -> None:
    """Test that the `get_predefined_case_teams` function returns the expected response."""

    test_data = {
        "team_template_id": "01A",
        "name": "Test case team",
        "created_date": "2025-05-09T10:04:23.000+0000",
        "description": "Test case team description",
    }

    expected = CaseTeam(**test_data)  # type: ignore[arg-type]

    with patch(
        "agent_ready_tools.tools.IT.salesforce.get_predefined_case_teams.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["team_template_id"],
                "Name": test_data["name"],
                "CreatedDate": test_data["created_date"],
                "Description": test_data["description"],
            }
        ]

        response = get_predefined_case_teams()

        assert response
        assert response[0] == expected
