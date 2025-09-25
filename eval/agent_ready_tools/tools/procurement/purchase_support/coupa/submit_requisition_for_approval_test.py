from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_requisition_by_id_test import (
    mock_requisition_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.submit_requisition_for_approval import (
    coupa_submit_requisition_for_approval,
)


def test_coupa_submit_requisition_for_approval() -> None:
    """Test that the `submit_requisition_for_approval_coupa` function returns the expected
    response."""

    # Define test data:
    test_data = {
        "requisition_line_id": 123131222,
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.submit_requisition_for_approval.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = mock_requisition_response()
        mock_client.put_request.return_value = mock_requisition_response() | {
            "id": test_data["requisition_line_id"],
            "status": "pending_approval",
        }

        # Submit a requisition approval
        response = coupa_submit_requisition_for_approval(
            requisition_id=test_data["requisition_line_id"]
        ).content

        # Ensure that submit_requisition_for_approval_coupa() executed and returned proper values
        assert response.status == "pending_approval"

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            resource_name=f"requisitions/{test_data['requisition_line_id']}/update_and_submit_for_approval"
        )
