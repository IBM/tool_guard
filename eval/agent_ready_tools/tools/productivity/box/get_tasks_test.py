from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.get_tasks import BoxFileTasks, get_tasks


def test_get_tasks_with_all_data() -> None:
    """Test that the tasks of a file can be retrieved successfully."""

    # Define test data:
    test_data = {
        "file_id": "1809845773276",
        "task_id": "33385199546",
        "action": "complete",
        "message": "test",
        "created_by": "csprod2",
        "creation_date": "2025-03-25",
        "assigned_to": "csprod2",
        "due_date": "2025-03-25",
        "is_completed": True,
        "completion_date": "2025-03-24",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.get_tasks.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "entries": [
                {
                    "id": test_data["task_id"],
                    "action": test_data["action"],
                    "message": test_data["message"],
                    "created_by": {"name": test_data["created_by"]},
                    "created_at": test_data["creation_date"],
                    "task_assignment_collection": {
                        "entries": [
                            {
                                "assigned_to": {"name": test_data["assigned_to"]},
                                "completed_at": test_data["completion_date"],
                            }
                        ]
                    },
                    "due_at": test_data["due_date"],
                    "is_completed": test_data["is_completed"],
                }
            ]
        }

        # Get tasks of a file
        response = get_tasks(test_data["file_id"]).box_file_tasks[:1]

        expected_response = [
            BoxFileTasks(
                task_id="33385199546",
                action="complete",
                message="test",
                created_by="csprod2",
                creation_date="2025-03-25",
                assigned_to="csprod2",
                due_date="2025-03-25",
                is_completed=True,
                completion_date="2025-03-24",
            )
        ]
        # Ensure that get_tasks() executed and returned proper values
        assert response

        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"files/{test_data['file_id']}/tasks",
        )


def test_get_tasks_with_less_data() -> None:
    """Test that the tasks of a file can be retrieved successfully."""

    # Define test data:
    test_data = {
        "file_id": "1837050913782",
        "task_id": "33912549534",
        "action": "review",
        "message": "Task For test",
        "created_by": "csprod2",
        "creation_date": "2025-04-17",
        "assigned_to": "",
        "due_date": "",
        "is_completed": False,
        "completion_date": "",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.get_tasks.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "entries": [
                {
                    "id": test_data["task_id"],
                    "action": test_data["action"],
                    "message": test_data["message"],
                    "created_by": {"name": test_data["created_by"]},
                    "created_at": test_data["creation_date"],
                    "task_assignment_collection": {
                        "entries": [
                            {
                                "assigned_to": {"name": test_data["assigned_to"]},
                                "completed_at": test_data["completion_date"],
                            }
                        ]
                    },
                    "due_at": test_data["due_date"],
                    "is_completed": test_data["is_completed"],
                }
            ]
        }

        # Get tasks of a file
        response = get_tasks(test_data["file_id"]).box_file_tasks[:1]

        expected_response = [
            BoxFileTasks(
                task_id="33912549534",
                action="review",
                message="Task For test",
                created_by="csprod2",
                creation_date="2025-04-17",
                assigned_to="",
                due_date="",
                is_completed=False,
                completion_date="",
            )
        ]
        # Ensure that get_tasks() executed and returned proper values
        assert response

        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"files/{test_data['file_id']}/tasks",
        )
