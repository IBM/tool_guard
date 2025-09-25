from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_contract import (
    delete_contract,
)


def test_delete_contract() -> None:
    """Verifies that the `delete_contract` tool can successfully delete a contract from
    Salesforce."""

    # Define test data:
    test_data = {
        "contract_id": "800fJ000005ZuqrQAC",
        "http_code": 204,
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_contract.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Contract.delete.return_value = test_data["http_code"]

        # Delete a file
        delete_response = delete_contract(test_data["contract_id"])

        # Ensure that delete_contract() executed and returned proper values
        assert delete_response
        assert delete_response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Contract.delete.assert_called_once_with(
            test_data["contract_id"]
        )
