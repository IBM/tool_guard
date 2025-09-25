from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_case_team_member_roles import (
    list_case_team_member_roles,
)
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseTeamRole


def test_list_case_team_member_roles() -> None:
    """Test that the `list_case_team_member_roles` function returns the expected response."""

    test_data = [
        CaseTeamRole(
            case_team_member_role_id="0B7gL000000023RSAQ",
            case_team_member_role_name="Support manager",
            access_level="Edit",
            created_date="2025-04-24T17:03:33.000+0000",
        ),
        CaseTeamRole(
            case_team_member_role_id="0B7gL000000028HSAQ",
            case_team_member_role_name="Manager",
            access_level="Edit",
            created_date="2025-04-24T17:06:02.000+0000",
        ),
    ]

    expected: list[CaseTeamRole] = test_data

    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_case_team_member_roles.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data[0].case_team_member_role_id,
                "Name": test_data[0].case_team_member_role_name,
                "AccessLevel": test_data[0].access_level,
                "CreatedDate": test_data[0].created_date,
            },
            {
                "Id": test_data[1].case_team_member_role_id,
                "Name": test_data[1].case_team_member_role_name,
                "AccessLevel": test_data[1].access_level,
                "CreatedDate": test_data[1].created_date,
            },
        ]

        response = list_case_team_member_roles("Name= Manager OR Name= Support manager")

        assert response == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, Name, AccessLevel, CreatedDate FROM CaseTeamRole WHERE Name = 'Manager' OR Name = 'Support manager'"
        )
