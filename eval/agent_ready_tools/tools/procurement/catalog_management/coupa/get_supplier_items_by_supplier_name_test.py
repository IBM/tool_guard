from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.coupa.get_supplier_items_by_supplier_name import (
    QUERY_FIELDS,
    coupa_get_supplier_items_by_supplier_name,
)

TEST_SUPPLIER_ITEM = {
    "id": "1234",
    "supplier": {"id": "1234", "name": "SNPP", "number": "7G"},
    "item": {
        "id": "999",
        "description": "In rod we trust",
        "item-number": "S5E15",
        "name": "Inanimate carbon rod",
        "active": True,
        "storage-quantity": 1,
        "consumption-quantity": 1,
    },
}


def test_coupa_get_supplier_items_by_name() -> None:
    """Test get supplier items by name using a mock client."""

    supplier_name = "SNPP"

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.coupa.get_supplier_items_by_supplier_name.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [TEST_SUPPLIER_ITEM]

        response = coupa_get_supplier_items_by_supplier_name(supplier_name=supplier_name).content

        assert response

        mock_client.get_request_list.assert_called_once_with(
            resource_name="supplier_items",
            params={
                "fields": QUERY_FIELDS,
                "supplier[name][contains]": supplier_name,
            },
        )
