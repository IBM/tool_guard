from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_case_priority import list_case_priority
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import (
    CasePriority,
    PickListOptionsPair,
)


def test_list_case_priority() -> None:
    """Verifies that the `list_case_priority` tool in Salesforce can successfully retrieve the
    priority of a case."""

    # Define test data
    test_data = {"case_priority": "High"}

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_case_priority.get_salesforce_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "values": [{"value": test_data["case_priority"]}]
        }

        # Call the function
        response = list_case_priority()

        # Expected response
        expected_response = CasePriority(case_priority=test_data["case_priority"])

        # Verify the response
        assert response[0] == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            PickListOptionsPair.CasePriority.obj_api_name,
            PickListOptionsPair.CasePriority.field_api_name,
        )
