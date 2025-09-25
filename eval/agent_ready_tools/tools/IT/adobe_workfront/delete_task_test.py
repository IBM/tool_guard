from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.delete_task import adobe_delete_task


def test_adobe_delete_task() -> None:
    """Tests that an task can be deleted successfully by the `adobe_delete_task` tool."""
    # Define test data:
    test_data = {"task_id": "682af48500080ccd3e2afe8e406c0b59", "http_code": 200}

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.delete_task.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Delete a Task
        response = adobe_delete_task(task_id=test_data["task_id"])

        # Ensure that the adobe_delete_task() has been executed and returned the expected response
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(entity=f"task/{test_data["task_id"]}")
