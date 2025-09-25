from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_approval_by_id import (
    coupa_get_approval_by_id,
)


def test_coupa_get_approval_by_id() -> None:
    """Test that the `get_approval_by_id` function returns the expected response."""

    # Define test data:
    test_data = {
        "approval_id": 85263,
        "approver_id": 3,
        "approved_id": 9464,
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_approval_by_id.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "approver": {
                "id": test_data["approver_id"],
                "login": "vpierren",
                "fullname": "Victor (CFO) Pierre",
            },
            "approved-by": {
                "id": test_data["approved_id"],
                "login": "IBMFunctionalUser",
                "fullname": "IBM AppConnect Function User",
            },
            "id": test_data["approval_id"],
            "created-at": "2025-03-24T10:14:00-07:00",
            "updated-at": "2025-03-24T16:36:49-07:00",
            "approval-date": "2025-03-24T16:36:48-07:00",
            "approvable-type": "RequisitionHeader",
            "approver-type": "User",
            "approvable-id": 5197,
        }

        # Get approval by ID
        response = coupa_get_approval_by_id(approval_id=test_data["approval_id"]).content

        # Ensure that get_approval_by_id() executed and returned proper values
        assert response
        assert response.approver.approver_id == test_data["approver_id"]
        assert response.approved_by.approver_id == test_data["approved_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            resource_name=f"approvals/{test_data['approval_id']}"
        )
