from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_direct_reports import (
    get_direct_reports,
)


def test_get_direct_reports() -> None:
    """Test that the `get_direct_reports` function returns the expected response."""

    # Define test data:
    test_data = {
        "id": "de52fbe58bc84c8b90883502f9f868ed",
        "user_id": "b7cbc44db56a4de292c3d0358c8c86c6",
        "name": "Blair White",
        "business_title": "Software Test Engineer",
        "email": "bwhite@workday.net",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_direct_reports.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["user_id"],
                    "descriptor": test_data["name"],
                    "businessTitle": test_data["business_title"],
                    "primaryWorkEmail": test_data["email"],
                }
            ],
            "total": 1,
        }

        # Get direct reports
        response = get_direct_reports(user_id=test_data["id"])

        # Ensure that get_direct_reports() executed and returned proper values
        assert response
        assert len(response.direct_reports)
        assert response.direct_reports[0].user_id == test_data["user_id"]
        assert response.direct_reports[0].name == test_data["name"]
        assert response.direct_reports[0].business_title == test_data["business_title"]
        assert response.direct_reports[0].email == test_data["email"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/v1/{mock_client.tenant_name}/workers/{test_data['id']}/directReports"
        )
