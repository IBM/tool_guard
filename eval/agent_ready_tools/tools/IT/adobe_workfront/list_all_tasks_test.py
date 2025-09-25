from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_all_tasks import (
    ListTasksResponse,
    Task,
    list_all_tasks,
)


def test_list_all_tasks() -> None:
    """Verify that the `list_all_tasks` tool can successfully retrieve Adobe Workfront tasks."""

    # Define test data:
    test_data = {
        "task_id": "6679dd4a1d9a290d351b556193a2170c",
        "task_name": "Content - R1 - Writer Revisions",
        "task_number": "3",
        "status": "ADB",
        "project_start_date": "2025-05-15T09:00:00:000-0400",
        "project_complete_date": "2025-05-16T17:00:00:000-0400",
        "object_code": "TASK",
    }

    # Define parameters for the test
    limit = 100
    skip = 0

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_all_tasks.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["task_id"],
                    "name": test_data["task_name"],
                    "taskNumber": test_data["task_number"],
                    "status": test_data["status"],
                    "projectedStartDate": test_data["project_start_date"],
                    "projectedCompletionDate": test_data["project_complete_date"],
                    "objCode": test_data["object_code"],
                }
            ]
        }

        # List tasks of Adobe Workfront
        response = list_all_tasks(task_name=test_data["task_name"])

        # Ensure that list_all_tasks() executed and returned proper values
        assert response
        expected_data = ListTasksResponse(
            tasks=[
                Task(
                    task_id=test_data["task_id"],
                    task_name=test_data["task_name"],
                    task_number=test_data["task_number"],
                    status=test_data["status"],
                    project_start_date=test_data["project_start_date"],
                    project_complete_date=test_data["project_complete_date"],
                    object_code=test_data["object_code"],
                )
            ]
        )

        assert response == expected_data

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="task/search",
            params={
                "name": test_data["task_name"],
                "$$LIMIT": limit,
                "$$FIRST": skip,
            },
        )
