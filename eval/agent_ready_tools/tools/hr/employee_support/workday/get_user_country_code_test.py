from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_user_country_code import (
    get_user_country_code,
)


def test_get_user_country_code() -> None:
    """Tests that the `get_user_country_code` tool is functioning properly."""

    # Define test data:
    test_data = {
        "user_id": "3aa5550b7fe348b98d7b5741afc65534",
        "country_code": "USA",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_user_country_code.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "primaryJob": {
                "location": {"country": {"ISO_3166-1_Alpha-3_Code": test_data["country_code"]}}
            }
        }

        # Get user's country code
        response = get_user_country_code(user_id=test_data["user_id"])

        # Ensure that get_user_country_code() executed and returned proper values
        assert response
        assert response.country_code == test_data["country_code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            url=f"api/staffing/v6/{mock_client.tenant_name}/workers/{test_data['user_id']}"
        )
