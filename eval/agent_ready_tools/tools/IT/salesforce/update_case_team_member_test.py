from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_case_team_member import update_case_team_member


def test_update_case_team_member() -> None:
    """Tests that the `update_case_team_member` function returns the expected response."""

    # Define test data
    test_data = {
        "case_team_member_id": "0B6fJ0000000UHRSA2",
        "case_team_member_role_id": "0B7fJ0000000qOPSAY",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_case_team_member.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.CaseTeamMember.update.return_value = test_response

        # Update a case team member
        response = update_case_team_member(**test_data)

        # Ensure that update_case_team_member() executes and returns proper values
        assert response
        assert response == test_response

        # Ensure that API call was made with expected parameters
        mock_client.salesforce_object.CaseTeamMember.update(
            test_data, test_data["case_team_member_role_id"]
        )
