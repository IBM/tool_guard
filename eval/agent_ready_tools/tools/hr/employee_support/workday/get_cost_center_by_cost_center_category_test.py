from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_cost_center_by_cost_center_category import (
    get_cost_center_by_cost_center_category,
)


def test_get_cost_center_by_cost_center_category() -> None:
    """Test that the `get_cost_center_by_cost_center_category` function returns the expected
    response."""

    # Define test data:
    test_data = {
        "category_id": "17a5e132b7881000140923f2a6c60109",
        "center_id": "3b122818d7934d1c8c663ddbe1937819",
        "center_descriptor": "10000 Office of CEO",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_cost_center_by_cost_center_category.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["center_id"],
                    "descriptor": test_data["center_descriptor"],
                }
            ],
        }

        # Get cost centers by categories
        response = get_cost_center_by_cost_center_category(test_data["category_id"])

        # Ensure that get_cost_center_by_cost_center_category() executed and returned proper values
        assert response
        assert len(response.costcenters)
        assert response.costcenters[0].id == test_data["center_id"]
        assert response.costcenters[0].descriptor == test_data["center_descriptor"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/staffing/v6/{mock_client.tenant_name}/values/organizationAssignmentChangesGroup/costCenters/{test_data['category_id']}"
        )
