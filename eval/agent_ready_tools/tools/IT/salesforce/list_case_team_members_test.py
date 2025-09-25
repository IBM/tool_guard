from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_case_team_members import list_case_team_members
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseTeamMember


def test_list_case_team_members() -> None:
    """Tests that the `list_case_team_members` tool returns the expected response."""

    # Define mock response data
    test_data = [
        CaseTeamMember(
            case_team_member_id="0B6gL00000001grSAA",
            case_id="500gL000003rHNZQA2",
            member_id="005gL000001qXQjQAM",
            team_role_id="0B7gL000000023RSAQ",
            create_date="2025-04-29T14:11:27.000+0000",
            created_by_id="005gL000001qXQjQAM",
        )
    ]

    expected: list[CaseTeamMember] = test_data

    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_case_team_members.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create mock client and set up return value
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data[0].case_team_member_id,
                "ParentId": test_data[0].case_id,
                "MemberId": test_data[0].member_id,
                "TeamRoleId": test_data[0].team_role_id,
                "CreatedDate": test_data[0].create_date,
                "CreatedById": test_data[0].created_by_id,
            }
        ]

        # Call the function
        response = list_case_team_members(
            "MemberId= '005gL000001qXQjQAM' AND TeamRoleId= '0B7gL000000023RSAQ' AND CreatedDate = 2025-04-29"
        )

        # Assertions
        assert response == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, ParentId, MemberId, TeamRoleId, CreatedDate, CreatedById FROM CaseTeamMember WHERE MemberId = '005gL000001qXQjQAM' AND TeamRoleId = '0B7gL000000023RSAQ' AND CreatedDate = 2025-04-29"
        )


def test_list_case_team_members_without_filter() -> None:
    """Tests that the `list_case_team_members` tool returns the expected response."""

    # Define mock response data
    test_data = [
        CaseTeamMember(
            case_team_member_id="0B6gL00000001grSAA",
            case_id="500gL000003rHNZQA2",
            member_id="005gL000001qXQjQAM",
            team_role_id="0B7gL000000023RSAQ",
            create_date="2025-04-29T14:11:27.000+0000",
            created_by_id="005gL000001qXQjQAM",
        ),
        CaseTeamMember(
            case_team_member_id="0B6gL00000001k5SAA",
            case_id="500gL000003u95KQAQ",
            member_id="005gL000001qXQjQAM",
            team_role_id="0B7gL000000028HSAQ",
            create_date="2025-05-05T11:53:42.000+0000",
            created_by_id="005gL000001qXQjQAM",
        ),
    ]

    expected: list[CaseTeamMember] = test_data

    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_case_team_members.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create mock client and set up return value
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data[0].case_team_member_id,
                "ParentId": test_data[0].case_id,
                "MemberId": test_data[0].member_id,
                "TeamRoleId": test_data[0].team_role_id,
                "CreatedDate": test_data[0].create_date,
                "CreatedById": test_data[0].created_by_id,
            },
            {
                "Id": test_data[1].case_team_member_id,
                "ParentId": test_data[1].case_id,
                "MemberId": test_data[1].member_id,
                "TeamRoleId": test_data[1].team_role_id,
                "CreatedDate": test_data[1].create_date,
                "CreatedById": test_data[1].created_by_id,
            },
        ]

        # Call the function
        response = list_case_team_members()

        # Assertions
        assert response[1] == expected[1]

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, ParentId, MemberId, TeamRoleId, CreatedDate, CreatedById FROM CaseTeamMember "
        )
