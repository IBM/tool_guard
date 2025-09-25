from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_time_types import (
    get_time_types,
)


def test_get_time_types() -> None:
    """Test that the `get_time_types` function returns the expected response."""
    # Define test data:
    test_data = {
        "country": "IND",
        "external_code": "PRIVILEGE LEAVE",
        "workflow_configuration": "Manager",
        "unit": "DAYS",
        "absence_class": "UNSPECIFIED",
        "category": "ABSENCE",
        "external_name": "INDIA PRIVILEGE LEAVE",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_time_types.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "externalCode": test_data["external_code"],
                        "workflowConfiguration": test_data["workflow_configuration"],
                        "unit": test_data["unit"],
                        "absenceClass": test_data["absence_class"],
                        "category": test_data["category"],
                        "externalName_en_US": test_data["external_name"],
                    }
                ]
            }
        }

        # Get time types
        response = get_time_types(country=test_data["country"])

        # Ensure that get_time_types() executed and returned proper values
        assert response
        assert len(response.time_types)
        assert response.time_types[0].external_code == test_data["external_code"]
        assert response.time_types[0].workflow_configuration == test_data["workflow_configuration"]
        assert response.time_types[0].unit == test_data["unit"]
        assert response.time_types[0].absence_class == test_data["absence_class"]
        assert response.time_types[0].category == test_data["category"]
        assert response.time_types[0].external_name == test_data["external_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="TimeType",
            params={"$format": "JSON"},
            filter_expr=f"country eq '{test_data["country"]}'",
            select_expr="country,externalCode,workflowConfiguration,unit,absenceClass,category,externalName_en_US",
        )
