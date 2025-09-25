from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.search_departments_by_division_and_country import (
    search_departments_by_division_and_country,
)


def test_search_departments_by_division_and_country() -> None:
    """Test that the `search_departments_by_division_and_country` function returns the expected
    response."""
    # Define test data:
    test_data = {
        "external_code": "5000017",
        "name": "Operations IN",
        "division": "Manufacturing",
        "country": "IND",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.search_departments_by_division_and_country.get_sap_successfactors_client"
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

        # Get departments by division and country
        response = search_departments_by_division_and_country(
            test_data["division"], test_data["country"]
        )

        # Ensure that search_departments_by_division_and_country() executed and returned proper values
        assert response
        assert len(response.departments)
        assert response.departments[0].department_external_code == test_data["external_code"]
        assert response.departments[0].department_name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "FODepartment",
            filter_expr=f"cust_toDivision/name eq '{test_data['division']}' and cust_toLegalEntity/country eq '{test_data['country']}'",
            select_expr=f"name,externalCode",
            expand_expr=f"cust_toDivision,cust_toLegalEntity",
        )
