from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier_item import (
    coupa_create_supplier_item,
)


def test_coupa_create_supplier_item() -> None:
    """Test create supplier item using a mock client."""
    test_supplier_id = 123
    test_item_id = 345
    test_supplier_item_id = 1

    test_data: Dict[str, Any] = {
        "price": 100.0,
        "supplier-part-num": "CARBONROD",
        "preferred": False,
        "currency": {"code": "USD"},
        "supplier": {"id": test_supplier_id},
        "item": {"id": test_item_id},
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.coupa.create_supplier_item.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": 1,
            "supplier": {"id": test_supplier_id},
            "item": {"id": test_item_id},
        }

        response = coupa_create_supplier_item(
            item_id=test_data["item"]["id"],
            supplier_id=test_data["supplier"]["id"],
            supplier_part_num=test_data["supplier-part-num"],
            price=test_data["price"],
            preferred=test_data["preferred"],
            currency_code=test_data["currency"]["code"],
        ).content

        assert response
        assert response.supplier_item_id == test_supplier_item_id
        assert response.supplier_id == test_supplier_id
        assert response.item_id == test_item_id

        mock_client.post_request.assert_called_once_with(
            resource_name="supplier_items",
            params={"fields": '["id",{"supplier":["id"]},{"item":["id"]}]'},
            payload=test_data,
        )
