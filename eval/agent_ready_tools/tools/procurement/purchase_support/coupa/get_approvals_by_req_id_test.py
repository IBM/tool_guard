from unittest.mock import MagicMock, call, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_approvals_by_req_id import (
    coupa_get_approvals_by_req_id,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.get_requisition_by_id_test import (
    mock_requisition_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaApproval,
    CoupaApprover,
)


def test_coupa_get_approvals_by_req_id() -> None:
    """Test that the `get_approvals_by_req_id` function returns the expected response."""

    # Define test data: ids are keys just for ease of accessing test data, Approval is the real data
    test_approval_id = 85487
    test_request_id = 5315
    test_data = {
        "approvals": {
            test_approval_id: CoupaApproval(
                approval_id=test_approval_id,
                created_at="2025-04-02T15:10:00-07:00",
                updated_at="2025-04-02T15:19:16-07:00",
                status="approved",
                approval_date="2025-04-02T15:19:15-07:00",
                approvable_type="RequisitionHeader",
                approver_type="User",
                approvable_id=test_request_id,
                approver=CoupaApprover(
                    approver_id=3,
                    approver_login="vpierren",
                    approver_fullname="Victor (CFO) Pierre",
                ),
                approved_by=CoupaApprover(
                    approver_id=9464,
                    approver_login="IBMFunctionalUser",
                    approver_fullname="IBM AppConnect Function User",
                ),
            )
        }
    }
    mock_requisition = mock_requisition_response()

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_approvals_by_req_id.get_coupa_client"
    ) as mock_coupa_client:
        # mock client
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client

        mock_client.get_request.side_effect = [
            mock_requisition | {"approval_id_list": [test_approval_id]},
            {
                "id": test_approval_id,
                "status": "approved",
                "approval_date": "2025-04-02T15:19:15-07:00",
                "approvable_type": "RequisitionHeader",
                "approver_type": "User",
                "approvable_id": test_request_id,
                "approver": {"id": 3, "login": "vpierren", "fullname": "Victor (CFO) Pierre"},
                "approved_by": {
                    "id": 9464,
                    "login": "IBMFunctionalUser",
                    "fullname": "IBM AppConnect Function User",
                },
            },
        ]

        response = coupa_get_approvals_by_req_id(test_request_id).content

        # Ensure that get_approvals_by_req_id() executed and returned proper values
        assert response
        assert len(response.approval_list) == len(test_data["approvals"])
        for approval in response.approval_list:
            assert approval.approval_id in test_data["approvals"]

        # Ensure the API calls were made with expected parameters
        mock_client.get_request.assert_has_calls(
            [
                call(resource_name=f"requisitions/{test_request_id}"),
                call(resource_name=f"approvals/{test_approval_id}"),
            ],
            any_order=False,
        )
