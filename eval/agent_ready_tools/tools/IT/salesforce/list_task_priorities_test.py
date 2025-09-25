from typing import List
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_task_priorities import list_task_priorities
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import TaskPriority


def test_list_task_priorities_with_conditions() -> None:
    """Test that `list_task_priorities` function returns the expected response with specific
    conditions."""

    # Define test data
    test_data = [
        TaskPriority(
            task_priority="High",
        )
    ]

    # Expected output
    expected: List[TaskPriority] = test_data

    # Patch the Salesforce client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_task_priorities.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "MasterLabel": test_data[0].task_priority,
            }
        ]

        # Call the function
        response = list_task_priorities("High")

        # Assertion
        assert response == expected
