from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.coupa.create_item import (
    coupa_create_item,
)


def test_coupa_create_item() -> None:
    """test the create_item tool."""

    # Define test data:
    item_name = "Full Item"
    item_uom = "EA"
    item_desc = "Full description"
    item_active = True

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.coupa.create_item.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "id": 2700,
            "description": item_desc,
            "name": item_name,
            "active": item_active,
            "uom": {"code": item_uom, "name": "Each"},
        }

        # Create item
        result = coupa_create_item(
            name=item_name, uom_code=item_uom, description=item_desc, active=item_active
        ).content

        # Ensure that get_item_suppliers() executed and returned proper values
        assert result

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            resource_name="items",
            payload={
                "name": item_name,
                "active": item_active,
                "uom": {"code": item_uom},
                "description": item_desc,
                "item-type": "Item",
            },
        )
