from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_business_units_sap import (
    get_business_units_sap,
)


def test_get_business_units_sap() -> None:
    """Test that the `get_business_units_sap` function returns the expected response."""
    # Define test data:
    test_data = {
        "external_code": "SVCS",
        "name": "Services",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_business_units_sap.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "externalCode": test_data["external_code"],
                        "name": test_data["name"],
                    },
                ]
            }
        }

        # Get business units
        response = get_business_units_sap()

        # Ensure that get_business_units_sap() executed and returned proper values
        assert response
        assert len(response.business_units)
        assert response.business_units[0].business_unit_external_code == test_data["external_code"]
        assert response.business_units[0].business_unit_name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "FOBusinessUnit", select_expr=f"name,externalCode"
        )
