from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.hubspot.update_deal import hubspot_update_deal


def test_hubspot_update_deal() -> None:
    """Test Hubspot update deal tool."""

    test_deal_update = {
        "deal_id": "123",
        "deal_name": "The New Deal",
        "deal_type": "newbusiness",
        "description": "A brand new, beautiful deal",
        "deal_stage": "initiated",
    }

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.hubspot.update_deal.get_hubspot_client"
    ) as mock_hubspot_client:
        mock_client = MagicMock()
        mock_hubspot_client.return_value = mock_client

        mock_client.patch_request.return_value = {"id": test_deal_update["deal_id"]}

        response = hubspot_update_deal(**test_deal_update)

        assert response
        assert response.deal_id == test_deal_update["deal_id"]

        deal_id = test_deal_update["deal_id"]
        payload = {
            "dealname": test_deal_update["deal_name"],
            "dealtype": test_deal_update["deal_type"],
            "description": test_deal_update["description"],
            "dealstage": test_deal_update["deal_stage"],
        }
        mock_client.patch_request.assert_called_once_with(
            service="crm",
            version="v3",
            entity=f"objects/deals/{deal_id}",
            payload={"properties": payload},
        )
