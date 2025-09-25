from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.search_divisions_by_business_unit import (
    search_divisions_by_business_unit,
)


def test_search_divisions_by_business_unit() -> None:
    """Test that the `search_divisions_by_business_unit` function returns the expected response."""
    # Define test data:
    test_data = {
        "external_code": "CORP_SVCS",
        "name": "Corporate Services",
        "division": "Corporate",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.search_divisions_by_business_unit.get_sap_successfactors_client"
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

        # Get divisions by business unit
        response = search_divisions_by_business_unit(test_data["division"])

        # Ensure that search_divisions_by_business_unit() executed and returned proper values
        assert response
        assert len(response.divisions)
        assert response.divisions[0].division_external_code == test_data["external_code"]
        assert response.divisions[0].division_name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "FODivision",
            filter_expr=f"cust_toBusinessUnit/name eq '{test_data['division']}'",
            select_expr=f"name,externalCode",
            expand_expr=f"cust_toBusinessUnit",
        )
