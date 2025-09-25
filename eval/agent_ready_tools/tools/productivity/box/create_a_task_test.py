from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.create_a_task import create_a_task


def test_create_a_task() -> None:
    """Verify that the `create_a_task` tool can successfully create a task in Box."""

    # Define test data:
    test_data = {
        "file_id": "1811944714882",
        "task_message": "Task creation for a file",
        "task_id": "1234",
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.create_a_task.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": test_data["task_id"],
            "message": test_data["task_message"],
            "item": {"name": test_data["file_id"]},
        }

        # Create a task for a file
        response = create_a_task(file_id=test_data["file_id"], message=test_data["task_message"])

        # Ensure that create_a_task() executed and returned proper values
        assert response
        assert response.task_id == test_data["task_id"]
        assert response.message == test_data["task_message"]
        assert response.file_id == test_data["file_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="tasks",
            data={
                "item": {"id": test_data["file_id"], "type": "file"},
                "message": test_data["task_message"],
            },
        )
