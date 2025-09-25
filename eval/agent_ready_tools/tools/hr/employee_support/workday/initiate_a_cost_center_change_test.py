from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.initiate_a_cost_center_change import (
    initiate_a_cost_center_change,
)


def test_initiate_a_cost_center_change() -> None:
    """Test that cost center can be updated successfully by the `initiate_a_cost_center_change`
    tool."""

    # Define test data:
    test_data = {
        "cost_center_id": "9e6fa8ed0c7b4ec78cf047ce8265ad3e",
        "change_id": "dc4945b8b8be429e87564e01889c69f5",
        "user_id": "1c225f47274210094bb9c4c8ce9c0000",
        "effective_date": "2025-02-21T07:00:00.000Z",
        "descriptor": "20000 Office of CRMO",
        "status": "Successfully Completed",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.initiate_a_cost_center_change.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.post_create_organization_assignment_change.return_value = {
            "id": test_data["change_id"]
        }
        mock_client.patch_initiate_a_cost_center_change.return_value = {
            "costCenter": {
                "id": test_data["cost_center_id"],
                "descriptor": test_data["descriptor"],
            }
        }
        mock_client.post_submit_organization_assignment_change_id.return_value = {
            "businessProcessParameters": {"overallStatus": test_data["status"]},
            "error": "",
        }

        # Initiate a cost center change
        response = initiate_a_cost_center_change(
            cost_center_id=test_data["cost_center_id"],
            user_id=test_data["user_id"],
            effective_date=test_data["effective_date"],
        )

        # Ensure that initiate_a_cost_center_change() executed and returned proper values
        assert response.status == test_data["status"]
        assert response.cost_center_id == test_data["cost_center_id"]
        assert response.descriptor == test_data["descriptor"]

        # Ensure the API calls was made with expected parameters
        mock_client.post_create_organization_assignment_change.assert_called_once_with(
            {"date": test_data["effective_date"]}, test_data["user_id"]
        )
        mock_client.patch_initiate_a_cost_center_change.assert_called_once_with(
            {"costCenter": {"id": test_data["cost_center_id"]}}, test_data["change_id"]
        )
        mock_client.post_submit_organization_assignment_change_id.assert_called_once_with(
            payload={}, organization_assignment_change_id=test_data["change_id"]
        )


def test_initiate_a_cost_center_change_failure() -> None:
    """Test that cost center doesn't fail when return an error."""
    # Define test data:
    test_data = {
        "cost_center_id": "9e6fa8ed0c7b4ec78cf047ce8265ad3e",
        "effective_date": "2025-02-21T07:00:00.000Z",
        "user_id": "1c225f47274210094bb9c4c8ce9c0000",
        "descriptor": "There's at least 1 conflicting in-progress or completed event. For in-progress events, cancel or complete the events. For completed events, specify a date that's on or after the event, or rescind the event. Assign Organizations: Ella Phillips, Assign Organizations: Ella Phillips",
        "status": "Failed",
    }

    # Patch `get_workday_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.initiate_a_cost_center_change.get_workday_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.post_create_organization_assignment_change.return_value = {
            "error": "invalid request: validation errors",
            "errors": [
                {
                    "error": "There's at least 1 conflicting in-progress or completed event. For in-progress events, cancel or complete the events. For completed events, specify a date that's on or after the event, or rescind the event. Assign Organizations: Ella Phillips, Assign Organizations: Ella Phillips",
                    "code": "A389",
                }
            ],
        }

        # Initiate a cost center change
        response = initiate_a_cost_center_change(
            cost_center_id=test_data["cost_center_id"],
            user_id=test_data["user_id"],
            effective_date=test_data["effective_date"],
        )

        # Ensure that initiate_a_cost_center_change() executed and returned proper values
        assert response.status == test_data["status"]
        assert response.descriptor == test_data["descriptor"]

        # Ensure the API calls was made with expected parameters
        mock_client.post_create_organization_assignment_change.assert_called_once_with(
            {"date": test_data["effective_date"]}, test_data["user_id"]
        )
