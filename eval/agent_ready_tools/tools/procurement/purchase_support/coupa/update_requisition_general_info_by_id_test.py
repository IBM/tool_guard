from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_requisition_by_id_test import (
    mock_requisition_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.update_requisition_general_info_by_id import (
    coupa_update_requisition_general_info_by_id,
)


def test_coupa_update_requisition_general_info_by_id() -> None:
    """Test that `update_requisition_general_info_by_id` function returns the expected response."""

    # Define test data:
    test_data = {
        "requisition_id": 98765,
        "requested_by": "jdoe",
        "business_unit": "Engineering",
        "business_purpose": "New equipment for development team",
    }

    expected_payload: dict[str, Any] = {
        "justification": test_data["business_purpose"],
        "department": {"name": test_data["business_unit"]},
        "requested_by": {"login": test_data["requested_by"]},
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.update_requisition_general_info_by_id.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.put_request.return_value = mock_requisition_response() | expected_payload

        # Update requisition's general info
        result = coupa_update_requisition_general_info_by_id(
            requisition_id=test_data["requisition_id"],
            requested_by=test_data["requested_by"],
            business_unit=test_data["business_unit"],
            business_purpose=test_data["business_purpose"],
        ).content

        # Ensure that update_requisition_general_info_by_id() executed and returned True to condition
        assert result.business_unit == expected_payload["department"]["name"]
        assert result.business_purpose == expected_payload["justification"]

        # Ensure the API call was made with expected parameters and payload
        mock_client.put_request.assert_called_once_with(
            resource_name=f"requisitions/{test_data['requisition_id']}",
            payload=expected_payload,
        )
