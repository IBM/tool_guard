from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_case_origin import list_case_origin
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseOrigin, PickListOptionsPair


def test_list_case_origin() -> None:
    """Verifies that the `list_case_origin` tool in Salesforce can successfully retrieve the origin
    of a case."""

    # Define test data
    test_data = {"case_origin": "Email"}

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_case_origin.get_salesforce_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "values": [{"value": test_data["case_origin"]}]
        }

        # Call the function
        response = list_case_origin()

        # Expected response
        expected_response = CaseOrigin(case_origin=test_data["case_origin"])

        # Verify the response
        assert response[0] == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            PickListOptionsPair.CaseOrigin.obj_api_name,
            PickListOptionsPair.CaseOrigin.field_api_name,
        )
