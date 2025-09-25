from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.create_predefined_case_team import (
    create_predefined_case_team,
)
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseTeamTemplate


def test_create_predefined_case_team() -> None:
    """Verifies that the `create_predefined_case_team` tool can successfully create a predefined
    case team in Salesforce."""

    # Define test data
    test_data = CaseTeamTemplate(
        id="001gL0000054RzdQAE", name="Test Template Unique", description="Test description"
    )

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.create_predefined_case_team.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client

        # Mock the Salesforce API response
        mock_client.salesforce_object.CaseTeamTemplate.create.return_value = {"id": test_data.id}

        # Call the function
        response = create_predefined_case_team(
            name=test_data.name,
            description=test_data.description,
        )

        # Validate response
        assert response == test_data

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.CaseTeamTemplate.create.assert_called_once_with(
            {
                "Name": test_data.name,
                "Description": test_data.description,
            }
        )
