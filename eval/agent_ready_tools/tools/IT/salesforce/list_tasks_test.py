from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_tasks import list_tasks
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Task


def test_get_all_tasks() -> None:
    """Test that the `list_tasks` function returns the expected response."""
    # Define test data:
    test_data = {
        "task_subject": "Call",
        "task_status": "Not Started",
        "task_priority": "Normal",
        "task_description": "Test",
        "task_id": "00TgL000000QMGDUA4",
    }

    expected = Task(**test_data)  # type: ignore[arg-type]

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_tasks.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Subject": test_data["task_subject"],
                "Id": test_data["task_id"],
                "Status": test_data["task_status"],
                "Priority": test_data["task_priority"],
                "Description": test_data["task_description"],
            }
        ]

        # Find tasks by subject
        response = list_tasks("Subject=Call AND Priority=Normal")

        # Ensure that list_tasks executed and returned proper values
        assert response[0] == expected
