from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.create_predefined_case_team_member import (
    create_predefined_case_team_member,
)


def test_create_predefined_case_team_member() -> None:
    """Verifies that the `create_predefined_case_team_member` tool can successfully create a
    predefined case team member in Salesforce."""

    # Define test data
    test_data = {
        "member_id": "005gL000001qXQjQAM",
        "case_team_member_role_id": "0B7gL00000002zVSAQ",
        "team_template_id": "0B4gL0000001UbxSAE",
        "predefined_case_team_member_id": "0B5gL00000001XBSAY",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.create_predefined_case_team_member.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.CaseTeamTemplateMember.create.return_value = {
            "id": test_data["predefined_case_team_member_id"]
        }

        # Create a predefined case team member
        response = create_predefined_case_team_member(
            member_id=test_data["member_id"],
            case_team_member_role_id=test_data["case_team_member_role_id"],
            team_template_id=test_data["team_template_id"],
        )

        # Ensure that create_predefined_case_team_member() has executed and returned proper values
        assert response
        assert (
            response.predefined_case_team_member_id == test_data["predefined_case_team_member_id"]
        )

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.CaseTeamTemplateMember.create(
            payload={
                "MemberId": test_data["member_id"],
                "TeamRoleId": test_data["case_team_member_role_id"],
                "TeamTemplateId": test_data["team_template_id"],
            },
        )
