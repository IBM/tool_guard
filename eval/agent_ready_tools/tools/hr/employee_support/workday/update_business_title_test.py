from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.update_business_title import (
    update_business_title,
)


def test_update_business_title() -> None:
    """Test that the `update_business_title` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "3cc87e22d6a110010a9666f956dd0000",
        "title": "Director",
        "description": "Title Change: Logan McNeill",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.update_business_title.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.update_business_title.return_value = {
            "proposedBusinessTitle": test_data["title"],
            "descriptor": test_data["description"],
        }

        # Update business title
        response = update_business_title(
            user_id=test_data["user_id"], new_business_title=test_data["title"]
        )

        # Ensure that update_business_title() executed and returned proper values
        assert response
        assert response.new_business_title == test_data["title"]
        assert response.change_description == test_data["description"]

        # Ensure the API call was made with expected parameters
        mock_client.update_business_title.assert_called_once_with(
            user_id=test_data["user_id"], payload={"proposedBusinessTitle": test_data["title"]}
        )
