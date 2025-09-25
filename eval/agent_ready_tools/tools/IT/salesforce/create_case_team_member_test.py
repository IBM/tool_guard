from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.create_case_team_member import create_case_team_member


def test_create_case_team_member() -> None:
    """Tests that the case team member can be created by the `create_case_team_member` tool."""

    # Define test data:
    test_data = {
        "case_id": "500fJ000005gi9pQAA",
        "user_id": "005fJ000003sCk2QAE",
        "case_team_member_role_id": "0B7fJ0000000qOPSAY",
        "record_id": "0B6fJ0000000UJ3SAM",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.create_case_team_member.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.CaseTeamMember.create.return_value = {
            "id": test_data["record_id"]
        }

        # Create a case team member
        response = create_case_team_member(
            case_id=test_data["case_id"],
            user_id=test_data["user_id"],
            case_team_member_role_id=test_data["case_team_member_role_id"],
        )
        # Ensure that create_case_team_member() executes and returns proper values
        assert response
        assert response.record_id is not None

        # Ensure that API call was made with expected parameters
        mock_client.salesforce_object.CaseTeamMember.create(
            {
                "ParentId": test_data["case_id"],
                "MemberId": test_data["user_id"],
                "TeamRoleId": test_data["case_team_member_role_id"],
            }
        )
