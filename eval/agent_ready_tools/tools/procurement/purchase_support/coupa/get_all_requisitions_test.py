from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_all_requisitions import (
    coupa_get_all_requisitions,
)


def test_coupa_get_all_requisitions() -> None:
    """Test that the `get_all_requisitions` function returns the expected response."""

    # Define test data:
    test_data: dict[str, Any] = {
        "requisitions": [
            {
                "id": 5335,
                "created-at": "2025-04-01T12:00:00Z",
                "updated-at": "2025-04-10T12:00:00Z",
                "created-by": {"login": "mjordan"},
                "updated-by": {"login": "mjordan"},
                "requested-by": {"login": "mjordan"},
                "status": "partially_received",
                "currency": {"code": "USD"},
                "line-count": 2,
                "total-with-estimated-tax": "10000",
                "department": {"name": "Operations"},
                "justification": None,
                "ship-to-address": {"street1": "wocfioqaqkcl"},
                "ship-to-attention": "Meg(CEO) Jordan",
                "current-approval": {"id": 85691},
                "approvals": [{"id": 85691}],
                "requisition-lines": [
                    {
                        "id": 9948,
                        "description": "laptop",
                        "unit-price": 1000.0,
                        "currency": {"code": "USD"},
                        "line-type": "RequisitionAmountLine",
                        "line-num": 1,
                        "quantity": None,
                        "supplier": {"id": 9},
                        "account": {"id": 1426},
                        "total-with-estimated-tax": "950.0",
                    },
                    {
                        "id": 9949,
                        "description": "9070xt",
                        "unit-price": 850.0,
                        "currency": {"code": "USD"},
                        "line-type": "RequisitionAmountLine",
                        "line-num": 2,
                        "quantity": None,
                        "supplier": {"id": 9},
                        "account": {"id": 1426},
                        "total-with-estimated-tax": "950.0",
                    },
                ],
            },
            {
                "id": 5334,
                "created-at": "2025-04-01T12:00:00Z",
                "updated-at": "2025-04-10T12:00:00Z",
                "created-by": {"login": "mjordan"},
                "updated-by": {"login": "mjordan"},
                "requested-by": {"login": "mjordan"},
                "status": "draft",
                "currency": {"code": "USD"},
                "line-count": 1,
                "total-with-estimated-tax": "10000",
                "department": {"name": "Operations"},
                "justification": None,
                "ship-to-address": {"street1": "wocfioqaqkcl"},
                "ship-to-attention": "Meg(CEO) Jordan",
                "current-approval": {"id": 85686},
                "approvals": [{"id": 85686}],
                "requisition-lines": [
                    {
                        "id": 9947,
                        "description": "MacBook Pro Retina - 15-inch",
                        "unit-price": 2000.0,
                        "currency": {"code": "USD"},
                        "line-type": "RequisitionQuantityLine",
                        "line-num": 1,
                        "quantity": "10.0",
                        "supplier": {"id": 38},
                        "account": {"id": 1540},
                        "total-with-estimated-tax": "950.0",
                    }
                ],
            },
        ]
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_all_requisitions.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = test_data["requisitions"]

        # Get all requisitions (2 most recent)
        response = coupa_get_all_requisitions(limit=2).content

        # Ensure that get_all_requisitions() executed and returned proper values
        assert response
        assert response.requisition_list and len(response.requisition_list) == 2
        assert response.requisition_list[0].id == 5335
        assert response.requisition_list[1].id == 5334

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="requisitions",
            params={
                "limit": 2,
                "offset": 0,
                "order_by": "created-at",
                "dir": "desc",
            },
        )
