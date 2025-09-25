from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.coupa.link_item_to_supplier import (
    CoupaItemAvailabilityStatus,
    coupa_link_item_to_supplier,
)


def test_link_item_to_supplier() -> None:
    """test the coupa_link_item_to_supplier tool using mock client."""

    test_data = {
        "supplier_id": "4",
        "item_id": "2743",
        "price": "670",
        "currency_code": "USD",
        "saving_percentage": "10",
        "availability": CoupaItemAvailabilityStatus.IN_STOCK,
        "availability_date": "2025-06-12",
        "manufacturer": "AMAZON AWS",
        "minimum_order_quantity": "500",
        "part_number": "AAWS678",
        "auxiliary_part_number": "AAWS786",
        "id": "4432",
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.coupa.link_item_to_supplier.get_coupa_client"
    ) as mock_coupa_client:

        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {"id": test_data["id"]}

        response = coupa_link_item_to_supplier(
            supplier_id=test_data["supplier_id"],
            item_id=test_data["item_id"],
            price=test_data["price"],
            currency_code=test_data["currency_code"],
            saving_percentage=test_data["saving_percentage"],
            availability=test_data["availability"],
            availability_date=test_data["availability_date"],
            manufacturer=test_data["manufacturer"],
            minimum_order_quantity=test_data["minimum_order_quantity"],
            part_number=test_data["part_number"],
            auxiliary_part_number=test_data["auxiliary_part_number"],
        ).content

        assert response
        assert response == test_data["id"]

        mock_client.post_request.assert_called_once_with(
            resource_name="supplier_items",
            payload={
                "item": {"id": test_data["item_id"]},
                "price": test_data["price"],
                "currency": {"code": test_data["currency_code"]},
                "supplier": {"id": test_data["supplier_id"]},
                "savings-pct": test_data["saving_percentage"],
                "availability": test_data["availability"],
                "availability-date": test_data["availability_date"],
                "manufacturer": test_data["manufacturer"],
                "supplier-part-num": test_data["part_number"],
                "supplier-aux-part-num": test_data["auxiliary_part_number"],
                "minimum-order-quantity": test_data["minimum_order_quantity"],
            },
        )
