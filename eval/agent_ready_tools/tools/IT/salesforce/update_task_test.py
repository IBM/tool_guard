from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_task import update_task


def test_update_task() -> None:
    """Tests that the `update_task` function returns the expected response."""

    # Define test data:
    test_data = {
        "task_id": "00TgL000000TAjxUAG",
        "task_contact_id": "003gL000002CLU9QAO",
        "assignee_id": "005gL000001qXQjQAM",
        "task_related_to_account": "001gL000004Zin4QAC",
        "task_subject": "Call2",
        "task_activity_date": "2025-05-12",
        "task_status": "In progress",
        "task_priority": "Normal",
        "task_description": "test2",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_task.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Task.update.return_value = test_response

        # Update task
        response = update_task(**test_data)

        # Ensure that update_task() executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Task.update(test_data, test_data["task_id"])
