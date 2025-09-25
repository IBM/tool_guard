from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_purchase_order_by_req_id import (
    coupa_get_purchase_order_by_req_id,
)


def test_coupa_get_purchase_order_by_req_id() -> None:
    """Test that the `get_purchase_order_by_req_id` function returns the expected response."""

    # Define test data:
    test_data = {
        "purchase_order_id": 4152,
        "requisition_id": 5194,
        "requested_by": "Sargam Singh",
        "requested_by_login": "ssingh",
        "total_with_estimated_tax": "2950.00",
        "postal_code": "appconxfxyb",
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_purchase_order_by_req_id.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "id": test_data["purchase_order_id"],
                "po-number": f'{test_data["purchase_order_id"]}',
                "created-by": {"login": "mjordan"},
                "updated-by": {"login": "mjordan"},
                "created-at": "2025-02-10T22:59:02-08:00",
                "updated-at": "2025-03-21T12:48:17-07:00",
                "status": "issued",
                "transmission-status": "sent_via_email",
                "exported": 0,
                "ship-to-attention": test_data["requested_by"],
                "requisition-header": {
                    "id": 5194,
                    "created-by": {"login": "mjordan"},
                    "updated-by": {"login": "mjordan"},
                    "created-at": "2025-02-10T22:59:02-08:00",
                    "updated-at": "2025-03-21T12:48:17-07:00",
                    "requested-by": {
                        "fullname": test_data["requested_by"],
                        "login": test_data["requested_by_login"],
                    },
                    "status": "pending_approval",
                    "currency": {"code": "USD"},
                    "line-count": 1,
                    "total-with-estimated-tax": "10000",
                    "department": {"name": "IT"},
                    "justification": "Need chargers for new hires",
                    "ship-to-address": {
                        "street1": "123 Coupa St",
                        "city": "San Jose",
                        "postal-code": "95141",
                        "state": "CA",
                        "country": {"name": "United States"},
                    },
                    "current-approval": None,
                    "approvals": [{"id": 1001}, {"id": 1002}],
                    "requisition-lines": [
                        {
                            "id": 9991,
                            "description": "Multi-Charger",
                            "unit-price": "50.0",
                            "currency": {"code": "USD"},
                            "line-type": "RequisitionAmountLine",
                            "line-num": "1",
                            "quantity": "50.0",
                            "supplier": {"id": 1234},
                            "account": {"id": 5678},
                            "total-with-estimated-tax": "950.0",
                        }
                    ],
                },
                "payment-method": "invoice",
                "currency": {"code": "USD"},
                "total-with-estimated-tax": test_data["total_with_estimated_tax"],
                "supplier": {"name": "WxO_Coupa_Supplier1"},
                "ship-to-address": {
                    "street1": "appcongz520w",
                    "city": "appconkhpvd",
                    "postal-code": "appconxfxyb",
                    "state": "",
                    "country": {"name": "India"},
                },
                "order-lines": [
                    {
                        "id": 6048,
                        "description": "Multi-Charger",
                        "item": {
                            "description": "IBTX 9900 Xtreme",
                            "uom": {"name": "Each"},
                        },
                        "quantity": "50.0",
                        "price": "50.0",
                        "total": "2500.00",
                        "received": "0.00",
                        "receipt-approval-required": False,
                    }
                ],
            }
        ]

        # Get purchase by ID
        response = coupa_get_purchase_order_by_req_id(requisition_id=5194).content

        # Ensure that add_a_comment_to_invoice_coupa() executed and returned proper values
        assert response
        assert response.purchase_order_id == test_data["purchase_order_id"]
        assert response.requested_by == test_data["requested_by"]
        assert response.total_with_estimated_tax == test_data["total_with_estimated_tax"]
        assert len(response.order_lines.order_lines)
        assert response.shipping_address.postal_code == test_data["postal_code"]

        requisition = response.requisition
        assert requisition.id == 5194
        assert requisition.requested_by == test_data["requested_by_login"]
        assert requisition.status == "pending_approval"
        assert requisition.business_unit == "IT"
        assert requisition.business_purpose == "Need chargers for new hires"
        assert requisition.ship_to_address.city == "San Jose"
        assert requisition.current_approval is None
        assert requisition.approval_id_list == [1001, 1002]
        assert len(requisition.requisition_lines) == 1

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="purchase_orders",
            params={"requisition-header[id]": test_data["requisition_id"]},
        )
