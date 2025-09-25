from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
    AdobeWorkfrontTaskStatus,
)
from agent_ready_tools.tools.IT.adobe_workfront.update_task import (
    UpdateTaskResponse,
    adobe_update_task,
)


def test_adobe_update_task() -> None:
    """Verifies that the `update_task` tool can successfully update a task in Adobe Workfront."""

    test_data = {
        "task_id": "6835657d0005849536fced3c914f6719",
        "name": "Task update",
        "status": "IN_PROGRESS",
        "priority": "Low",
        "description": "Updating a task in Adobe Workfront",
        "assigned_to_id": "6629314904c37a5dd4dd3cf79b5d5285",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.update_task.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "data": {
                "ID": test_data["task_id"],
                "name": test_data["name"],
                "status": AdobeWorkfrontTaskStatus[test_data["status"].upper()].value,
            }
        }
        # Update a task
        response = adobe_update_task(
            task_id=test_data["task_id"],
            name=test_data["name"],
            status=test_data["status"],
            priority=test_data["priority"],
            description=test_data["description"],
            assigned_to_id=test_data["assigned_to_id"],
        )

        expected_response = UpdateTaskResponse(
            task_id=str(test_data["task_id"]),
            name=str(test_data["name"]),
            status=str(test_data["status"]),
        )

        # Ensure that create_task() has executed and returned proper values
        assert response == expected_response
        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            entity=f"task/{test_data['task_id']}",
            payload={
                "name": test_data["name"],
                "status": AdobeWorkfrontTaskStatus[test_data["status"].upper()].value,
                "priority": AdobeWorkfrontPriority[test_data["priority"].upper()].value,
                "description": test_data["description"],
                "assignedToID": test_data["assigned_to_id"],
            },
        )
