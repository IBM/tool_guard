from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_address_types import (
    get_address_types_sap,
)


def test_get_address_types() -> None:
    """Test that the `get_address_types_sap` function returns the expected response."""
    # Define test data:
    test_data = {
        "address_type_1": "benefits",
        "address_type_2": "business",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_address_types.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "d": {
                "picklistOptions": {
                    "results": [
                        {"externalCode": test_data["address_type_1"]},
                        {"externalCode": test_data["address_type_2"]},
                    ]
                }
            }
        }

        # Approve the request
        response = get_address_types_sap()

        # Ensure that get_address_types_sap() executed and returned proper values
        assert response
        assert response.address_types[0] == test_data["address_type_1"]
        assert response.address_types[1] == test_data["address_type_2"]

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(picklist_field="addressType")
