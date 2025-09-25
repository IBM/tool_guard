from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_account_types import list_account_types
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import (
    AccountType,
    PickListOptionsPair,
)


def test_list_account_types() -> None:
    """Verifies that the `list_account_types` tool in Salesforce can successfully retrieve the types
    of an account."""

    # Define test data
    test_data = {"account_type": "Prospect"}

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_account_types.get_salesforce_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "values": [{"value": test_data["account_type"]}]
        }

        # Call the function
        response = list_account_types()

        # Expected response
        expected_response = AccountType(account_type=test_data["account_type"])

        # Verify the response
        assert response
        assert response[0] == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            PickListOptionsPair.AccountType.obj_api_name,
            PickListOptionsPair.AccountType.field_api_name,
        )
