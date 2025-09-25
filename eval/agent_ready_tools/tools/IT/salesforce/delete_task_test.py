from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.delete_task import delete_task


def test_delete_task() -> None:
    """Tests that the `delete_task` function returns the expected response."""

    # Define test data:
    task_id = "00TgL000000TSqYUAW"
    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.delete_task.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Task.delete.return_value = test_response

        # Delete a task
        response = delete_task(task_id)

        # Ensure that delete_task() executed and returned proper values
        assert response
        assert response.http_code == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Task.delete.assert_called_once_with(task_id)
