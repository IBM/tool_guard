from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_cost_center_categories import (
    get_cost_center_categories,
)


def test_get_cost_center_categories() -> None:
    """Test that the `get_cost_center_categories` function returns the expected response."""

    # Define test data:
    test_data = {
        "category_id": "17a5e132b7881000140923f2a6c60109",
        "category_name": "Organizations",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_cost_center_categories.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["category_id"],
                    "descriptor": test_data["category_name"],
                }
            ],
        }

        # Get cost centers categories
        response = get_cost_center_categories()

        # Ensure that get_cost_center_categories() executed and returned proper values
        assert response
        assert len(response.categories)
        assert response.categories[0].cost_center_categories_id == test_data["category_id"]
        assert response.categories[0].cost_center_category_name == test_data["category_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/staffing/v6/{mock_client.tenant_name}/values/organizationAssignmentChangesGroup/costCenters/"
        )
