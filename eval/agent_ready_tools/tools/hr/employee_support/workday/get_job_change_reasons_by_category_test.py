from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_job_change_reasons_by_category import (
    get_job_change_reasons_by_category,
)


def test_get_job_change_reasons_by_category() -> None:
    """Tests that the `get_job_change_reasons_by_category` tool returns the expected response."""
    # Define test data:
    test_data = {
        "group_id": "340a97e88d1710001940bf683a2b01ba",
        "category_id": "e05854cff9244dbaad78d2e6555a74b7",
        "id": "9e616caff5b1480aab04f1ce22d7e7d4",
        "descriptor": "Money $$$",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_job_change_reasons_by_category.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "id": test_data["id"],
                    "descriptor": test_data["descriptor"],
                }
            ],
            "total": 1,
        }

        # Get job change reasons by category
        response = get_job_change_reasons_by_category(
            group_id=test_data["group_id"], category_id=test_data["category_id"]
        )

        # Ensure that get_job_change_reasons_by_category() executed and returned proper values
        assert response
        assert len(response.reasons)
        assert response.reasons[0].id == test_data["id"]
        assert response.reasons[0].descriptor == test_data["descriptor"]

        # Ensure the API call was made with expected parameters
        version = "v6"
        url = f"api/staffing/{version}/{mock_client.tenant_name}/values/jobChangesGroup/reason/{test_data['group_id']}/{test_data['category_id']}"
        mock_client.get_request.assert_called_once_with(url=url)
