from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_case_reason import list_case_reason
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseReason, PickListOptionsPair


def test_list_case_reason() -> None:
    """Verifies that the `list_case_reason` tool in Salesforce can successfully retrieve the reasons
    for a case."""

    # Define test data
    test_data = {"case_reason": "Performance"}

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_case_reason.get_salesforce_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "values": [{"value": test_data["case_reason"]}]
        }

        # Call the function
        response = list_case_reason()

        # Expected response
        expected_response = CaseReason(case_reason=test_data["case_reason"])

        # Verify the response
        assert response[0] == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            PickListOptionsPair.CaseReason.obj_api_name,
            PickListOptionsPair.CaseReason.field_api_name,
        )
