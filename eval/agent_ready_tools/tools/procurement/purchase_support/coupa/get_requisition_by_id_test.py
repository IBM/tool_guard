from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_requisition_by_id import (
    coupa_get_requisition_by_id,
)


def mock_requisition_response() -> dict:
    """
    Function that returns test data that can be used in other requisition related tests.

    Returns:
        The mock requisition data.
    """

    return {
        "id": 9653,
        "created-at": "2025-04-01T12:00:00Z",
        "updated-at": "2025-04-10T12:00:00Z",
        "created-by": {"login": "mjordan"},
        "updated-by": {"login": "mjordan"},
        "requested-by": {"login": "ssingh"},
        "status": "draft",
        "currency": {"code": "USD"},
        "line-count": 1,
        "total-with-estimated-tax": "10000",
        "department": {"name": "Operations"},
        "justification": "Test",
        "ship-to-address": {
            "street1": "28 Nevada 11",
            "city": "San Jose",
            "postal-code": "95141",
            "state": "CA",
            "country": {"name": "United States"},
        },
        "ship-to-attention": "Meg(CEO) Jordan",
        "current-approval": {"id": 85487},
        "approvals": [{"id": 85487}],
        "requisition-lines": [
            {
                "id": 9658,
                "description": "Lock,Combination",
                "unit-price": 923.12,
                "currency": {"code": "USD"},
                "line-type": "RequisitionQuantityLine",
                "line-num": 1,
                "quantity": "1",
                "uom": {"name": "Each"},
                "item": {
                    "id": 166,
                    "name": "Lenovo ThinkPad",
                    "description": "Lenovo think pad",
                    "item-number": "7650ELUC",
                    "manufacturer-name": None,
                    "manufacturer-part-number": None,
                },
                "supplier": {"id": 8776464},
                "account": {"id": 1538},
                "commodity": {"name": "Security Equipment"},
                "source-part-num": "SP-456",
                "shipping-term": {"code": "FOB"},
                "payment-term": {"code": "Net30"},
                "need-by-date": "2025-05-01",
                "transmission-method-override": "Email",
                "manufacturer-name": "MasterLock",
                "manufacturer-part-number": "ML-1234",
                "total-with-estimated-tax": "950.0",
            }
        ],
    }


def test_coupa_get_requisition_by_id_coupa() -> None:
    """Test that the `get_requisition_by_id_coupa` function returns the expected response."""

    # Define test data:
    test_data: dict[str, Any] = mock_requisition_response()

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_requisition_by_id.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = test_data

        # Get requisition by ID
        response = coupa_get_requisition_by_id(requisition_id=test_data["id"]).content

        # Ensure that get_requisition_by_id_coupa() executed and returned proper values
        assert response.id == test_data["id"]
        assert response.requested_by == test_data["requested-by"]["login"]
        assert response.status == test_data["status"]
        assert response.business_unit == test_data["department"]["name"]
        assert response.business_purpose == test_data["justification"]
        assert response.ship_to_address.street1 == test_data["ship-to-address"]["street1"]
        assert response.ship_to_attention == test_data["ship-to-attention"]
        assert response.current_approval.approval_id == test_data["current-approval"]["id"]
        assert response.approval_id_list == [approval["id"] for approval in test_data["approvals"]]
        assert response.requisition_lines
        line = response.requisition_lines[0]
        assert line.id == 9658

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            resource_name=f"requisitions/{test_data["id"]}"
        )
