from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_job_change_reasons_categories import (
    get_job_change_reasons_categories,
)


def test_get_job_change_reasons_categories() -> None:
    """Tests that the `get_job_change_reasons_categories` tool returns the expected response."""

    # Define test data:
    test_data = {
        "href": "https://maps.app.goo.gl/kh155mtnfWrsWc5f6",
        "descriptor": "Money $$$",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_job_change_reasons_categories.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "href": test_data["href"],
                    "descriptor": test_data["descriptor"],
                }
            ],
        }

        # Get job change reasons categories
        response = get_job_change_reasons_categories()

        # Ensure that get_job_change_reasons_categories() executed and returned proper values
        assert response
        assert len(response.categories)
        assert response.categories[0].href == test_data["href"]
        assert response.categories[0].descriptor == test_data["descriptor"]

        # Ensure the API call was made with expected parameters
        version = "v6"
        url = f"api/staffing/{version}/{mock_client.tenant_name}/values/jobChangesGroup/reason"
        mock_client.get_request.assert_called_once_with(url=url)
