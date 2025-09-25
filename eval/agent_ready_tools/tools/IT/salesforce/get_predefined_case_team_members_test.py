from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.get_predefined_case_team_members import (
    get_predefined_case_team_members,
)
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import PredefinedCaseTeamMember


def test_get_predefined_case_teams() -> None:
    """Test that the `get_predefined_case_team_members` function returns the expected response."""

    test_data = {
        "id": "0B5f",
        "member_id": "005f",
        "created_date": "2025-05-09T10:04:23.000+0000",
        "team_template_id": "0B4",
    }

    expected = PredefinedCaseTeamMember(**test_data)  # type: ignore[arg-type]

    with patch(
        "agent_ready_tools.tools.IT.salesforce.get_predefined_case_team_members.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["id"],
                "MemberId": test_data["member_id"],
                "CreatedDate": test_data["created_date"],
                "TeamTemplateId": test_data["team_template_id"],
            }
        ]

        response = get_predefined_case_team_members()

        assert response
        assert response[0] == expected
