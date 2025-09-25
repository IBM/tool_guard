from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_predefined_case_team_member import (
    update_predefined_case_team_member,
)


def test_update_predefined_case_team_member() -> None:
    """Tests that the `update_predefined_case_team_member` function returns the expected
    response."""

    # Define test data
    test_data = {
        "case_team_member_id": "0B5gL00000001AbSAI",
        "team_role_id": "0B7gL00000002oDSAQ",
    }

    expected_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_predefined_case_team_member.get_salesforce_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.salesforce_object.CaseTeamTemplateMember.update.return_value = expected_response

        # Update predefined case team member
        response = update_predefined_case_team_member(**test_data)

        # Assert the response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.CaseTeamTemplateMember.update.assert_called_once_with(
            test_data["case_team_member_id"],
            {"TeamRoleId": test_data["team_role_id"]},
        )
