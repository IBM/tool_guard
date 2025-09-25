from typing import List
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_task_statuses import list_task_statuses
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import TaskStatus


def test_list_task_statuses_with_conditions() -> None:
    """Test that `list_task_statuses` function returns the expected response with specific
    conditions."""

    # Define test data
    test_data = [
        TaskStatus(
            task_status="Completed",
        )
    ]

    # Expected output
    expected: List[TaskStatus] = test_data

    # Patch the Salesforce client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_task_statuses.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "MasterLabel": test_data[0].task_status,
            }
        ]

        # Call the function
        response = list_task_statuses("Completed")

        # Assertion
        assert response == expected
