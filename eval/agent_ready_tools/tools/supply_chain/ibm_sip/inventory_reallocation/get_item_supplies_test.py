from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.supply_chain.ibm_sip.inventory_reallocation.get_item_supplies import (
    ibm_sip_get_item_supplies,
)

TEST_ITEM_SUPPLIES = [
    {
        "itemId": "FST-3001",
        "unitOfMeasure": "EACH",
        "shipNode": "Woodland_DC",
        "type": "ONHAND",
        "segment": "B2B-Direct",
        "segmentType": "Channel",
        "quantity": 604.0,
        "eta": "1900-01-01T00:00:00.000Z",
        "shipByDate": "2500-01-01T00:00:00.000Z",
    },
    {
        "itemId": "FST-3001",
        "unitOfMeasure": "EACH",
        "shipNode": "Woodland_DC",
        "type": "ONHAND",
        "segment": "B2B-Marketplace",
        "segmentType": "Channel",
        "quantity": 816.0,
        "eta": "1900-01-01T00:00:00.000Z",
        "shipByDate": "2500-01-01T00:00:00.000Z",
    },
]


def test_get_item_supplies() -> None:
    """Test get item supplies using a mock client."""

    test_item_id = "FST-3001"
    test_ship_node = "Woodland_DC"

    with patch(
        "agent_ready_tools.tools.supply_chain.ibm_sip.inventory_reallocation.get_item_supplies.get_watson_commerce_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = TEST_ITEM_SUPPLIES

        response = ibm_sip_get_item_supplies(item_id=test_item_id, ship_node=test_ship_node).content

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name="/v1/supplies",
            params={
                "itemId": test_item_id,
                "shipNode": test_ship_node,
                "unitOfMeasure": "EACH",
            },
        )
