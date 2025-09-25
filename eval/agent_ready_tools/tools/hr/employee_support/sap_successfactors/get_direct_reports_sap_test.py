from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_direct_reports_sap import (
    get_direct_reports_sap,
)


def test_get_direct_reports_sap() -> None:
    """Tests that the `get_direct_reports_sap` function returns the expected response."""
    # Define test data:
    test_data = {
        "user_id": "Tchin",
        "email": "tchin.test@example.com",
        "name": "Tomas Chin",
        "phone": "+48123456789",
        "title": "Software Engineer",
        "division": "Software",
        "department": "Artificial Intelligence",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_direct_reports_sap.get_sap_successfactors_client"
    ) as mock_sap_client, patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_direct_reports_sap.user_exists"
    ) as mock_user_exists:

        # Mock the user_exists function to return True
        mock_user_exists.return_value = True

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "userId": test_data["user_id"],
                        "email": test_data["email"],
                        "displayName": test_data["name"],
                        "homePhone": test_data["phone"],
                        "title": test_data["title"],
                        "division": test_data["division"],
                        "department": test_data["department"],
                    },
                ]
            }
        }

        # Get all direct reports
        response = get_direct_reports_sap(test_data["user_id"])

        # Ensure that get_direct_reports_sap() executed and returned proper values
        assert response
        assert len(response.direct_reports)
        assert response.direct_reports[0].user_id == test_data["user_id"]
        assert response.direct_reports[0].email == test_data["email"]
        assert response.direct_reports[0].name == test_data["name"]
        assert response.direct_reports[0].home_phone == test_data["phone"]
        assert response.direct_reports[0].title == test_data["title"]
        assert response.direct_reports[0].division == test_data["division"]
        assert response.direct_reports[0].department == test_data["department"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_any_call(
            entity="User", filter_expr=f"manager/userId eq '{test_data['user_id']}'"
        )
