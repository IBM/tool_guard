from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_predefined_case_team import (
    update_predefined_case_team,
)


def test_update_predefined_case_team() -> None:
    """Tests that the `update_predefined_case_team` function returns the expected response."""

    # Define test data
    test_data = {
        "team_template_id": "0B4gL0000001N4DSAU",
        "name": "Updated Team Name",
        "description": "Updated team description",
    }

    expected_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_predefined_case_team.get_salesforce_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.salesforce_object.CaseTeamTemplate.update.return_value = expected_response

        # Update predefined case team
        response = update_predefined_case_team(**test_data)

        # Assert the response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.CaseTeamTemplate.update.assert_called_once_with(
            test_data["team_template_id"],
            {
                "Name": test_data["name"],
                "Description": test_data["description"],
            },
        )
