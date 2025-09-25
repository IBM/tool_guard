from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.hubspot.create_deal import hubspot_create_deal


def test_hubspot_create_deal() -> None:
    """Test Hubspot create deal tool."""

    test_deal = {
        "deal_name": "The New Deal",
        "deal_type": "newbusiness",
        "description": "A brand new, beautiful deal",
        "deal_stage": "initiated",
        "amount": 250.5,
        "pipeline": None,
        "close_date": "2025-12-25",
    }

    correct_properties = {
        "dealname": test_deal["deal_name"],
        "dealtype": test_deal["deal_type"],
        "description": test_deal["description"],
        "dealstage": test_deal["deal_stage"],
        "amount": test_deal["amount"],
        "closedate": test_deal["close_date"],
    }

    test_id = "123456"

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.hubspot.create_deal.get_hubspot_client"
    ) as mock_hubspot_client:
        mock_client = MagicMock()
        mock_hubspot_client.return_value = mock_client

        mock_client.post_request.return_value = {"id": test_id}

        response = hubspot_create_deal(**test_deal)

        assert response
        assert response.deal_id == test_id

        mock_client.post_request.assert_called_once_with(
            service="crm",
            version="v3",
            entity="objects/deals",
            payload={"properties": correct_properties},
        )
