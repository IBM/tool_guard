from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_approval_processes import (
    ApprovalProcess,
    list_approval_processes,
)


def test_list_approval_processes() -> None:
    """Verify that the `list_approval_processes` tool can successfully retrieve Adobe Workfront
    approval processes."""

    # Define test data
    test_data: dict[str, Any] = {
        "approval_process_id": "679d5124000299113f4d8fd048014df5",
        "approval_process_name": "Private Approval Process: Short name approval needed",
        "created_date": "2025-01-31T17:39:32:465-0500",
        "is_active": True,
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_approval_processes.get_adobe_workfront_client"
    ) as mock_adobe_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["approval_process_id"],
                    "name": test_data["approval_process_name"],
                    "entryDate": test_data["created_date"],
                    "isActive": test_data["is_active"],
                }
            ]
        }

        # Call the tool
        response = list_approval_processes(
            approval_process_name="Private Approval Process: Short name approval needed"
        )

        # Expected result
        expected_data = ApprovalProcess(
            approval_process_id=test_data["approval_process_id"],
            approval_process_name=test_data["approval_process_name"],
            created_date=test_data["created_date"],
            is_active=test_data["is_active"],
        )

        # Assertions
        assert response
        assert response.approval_processes[0] == expected_data

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="arvprc/search",
            params={
                "name": "Private Approval Process: Short name approval needed",
                "$$LIMIT": 50,
                "isActive": True,
            },
        )
