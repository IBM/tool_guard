from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_benefits_plan import (
    get_benefits_plan,
)


def test_get_my_benefits_plan() -> None:
    """Test that the `get_my_benefits_plan` function returns the expected response."""
    # Define test data:
    test_data = {
        "user_id": "802981",
        "start_date": "2017-01-01",
        "external_name": "802981_Dental Plan US_12142016_133940",
        "currency": "USD",
        "amount": "100",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_benefits_plan.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "externalName": test_data["external_name"],
                        "effectiveStartDate": test_data["start_date"],
                        "currency": test_data["currency"],
                        "amount": test_data["amount"],
                    },
                ]
            }
        }

        # Get benefit plans
        response = get_benefits_plan(test_data["user_id"])

        # Ensure that get_benefits_plan() executed and returned proper values
        assert response
        assert len(response.benefits)
        assert response.benefits[0].effective_start_date == test_data["start_date"]
        assert response.benefits[0].external_name == test_data["external_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "BenefitEnrollment", filter_expr=f"workerId eq '{test_data['user_id']}'"
        )
