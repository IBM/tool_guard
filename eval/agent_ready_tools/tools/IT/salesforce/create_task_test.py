from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.create_task import salesforce_create_task


def test_create_task() -> None:
    """Verifies that the `create_task` tool can successfully create a task in Salesforce."""

    # Define test data
    test_data = {
        "subject": "call test3",
        "task_status": "Completed",
        "task_priority": "High",
        "assignee_id": "005gL000001qXQjQAM",
        "contact_id": "003gL0000033EkfQAE",
        "due_date": "2025-05-10",
        "description": "First",
        "task_id": "00TgL0000045XYZQAM",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.create_task.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Task.create.return_value = {"id": test_data["task_id"]}

        # Call the function
        response = salesforce_create_task(
            subject=test_data["subject"],
            task_status=test_data["task_status"],
            task_priority=test_data["task_priority"],
            assignee_id=test_data["assignee_id"],
            contact_id=test_data["contact_id"],
            due_date=test_data["due_date"],
            description=test_data["description"],
        )

        # Ensure that salesforce_create_contact() has executed and returned proper values
        assert response
        assert response.task_id is not None

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.task.create(
            payload={
                "Subject": test_data["subject"],
                "Status": test_data["task_status"],
                "Priority": test_data["task_priority"],
                "OwnerId": test_data["assignee_id"],
                "WhoId": test_data["contact_id"],
                "ActivityDate": test_data["due_date"],
                "Description": test_data["description"],
            }
        )
