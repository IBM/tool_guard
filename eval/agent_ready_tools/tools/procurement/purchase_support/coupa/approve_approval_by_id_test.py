from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.approve_approval_by_id import (
    coupa_approve_approval_by_id,
)


def test_coupa_approve_approval_by_id() -> None:
    """Test that the `approve_approval_by_id` function returns the expected response."""
    test_approval_id = 85365
    test_data_approval = {
        "status": "pending_approval",
        "approvable-type": "RequisitionHeader",
        "approvable-id": 5277,
    }
    test_data_approval_response = {
        "id": test_approval_id,
        "created-at": "2025-03-26T11:10:10-07:00",
        "updated-at": "2025-03-26T11:17:20-07:00",
        "status": "approved",
        "approval-date": "2025-03-26T11:17:17-07:00",
        "approvable-type": "RequisitionHeader",
        "approver-type": "User",
        "approvable-id": 5277,
        "approver-id": 3,
        "approver": {"id": 3, "login": "vpierren", "fullname": "Victor (CFO) Pierre"},
        "approved-by": {
            "id": 9464,
            "login": "IBMFunctionalUser",
            "fullname": "IBM AppConnect Function User",
        },
    }
    test_data_requisition = {
        "id": 5277,
        "status": "pending_approval",
        "current-approval": {"id": test_approval_id},
    }

    # Patch `get_coupa_client` to return a mock client
    with (
        patch(
            "agent_ready_tools.tools.procurement.purchase_support.coupa.approve_approval_by_id.get_coupa_client"
        ) as mock_coupa_client,
    ):
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = test_data_approval_response
        mock_client.get_request.side_effect = [test_data_approval, test_data_requisition]

        # Approve the requisition
        response = coupa_approve_approval_by_id(test_approval_id).content

        # Ensure that approve_approval_by_id() executed and returned proper values
        assert response
        assert response.status == "approved"

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            resource_name=f"approvals/{test_approval_id}/approve"
        )

        mock_client.get_request.assert_called_with(
            resource_name=f"requisitions/{test_data_requisition["id"]}"
        )
