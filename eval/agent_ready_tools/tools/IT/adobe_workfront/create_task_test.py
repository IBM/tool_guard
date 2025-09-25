from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
)
from agent_ready_tools.tools.IT.adobe_workfront.create_task import create_task


def test_create_task() -> None:
    """Verifies that the `create_task` tool can successfully create a task in Adobe Workfront."""

    # Define test data
    test_data = {
        "project_id": "68301d4f000e8a2fa77964c2db6de65e",
        "name": "Task",
        "priority": "NORMAL",
        "description": "Creating a new task in Adobe Workfront",
        "assigned_to_id": "6629314904c37a5dd4dd3cf79b5d5285",
        "task_id": "683067da001364d11b8fcf7ff8767330",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.create_task.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "data": {
                "ID": test_data["task_id"],
                "name": test_data["name"],
            }
        }
        # Create a task
        response = create_task(
            project_id=test_data["project_id"],
            name=test_data["name"],
            priority=test_data["priority"],
            description=test_data["description"],
            assigned_to_id=test_data["assigned_to_id"],
        )

        # Ensure that create_task() has executed and returned proper values
        assert response
        assert response.task_id == test_data["task_id"]
        assert response.name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="task",
            payload={
                "projectID": test_data["project_id"],
                "name": test_data["name"],
                "priority": int(AdobeWorkfrontPriority[test_data["priority"].upper()].value),
                "description": test_data["description"],
                "assignedToID": test_data["assigned_to_id"],
            },
        )
