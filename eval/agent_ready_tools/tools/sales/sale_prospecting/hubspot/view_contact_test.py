from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.hubspot.dataclasses import HubspotContact
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.view_contact import hubspot_view_contact


def test_hubspot_view_contact() -> None:
    """Test Hubspot view contact tool."""

    test_id = "123"

    test_contact_response = {
        "createdate": "2025-08-05T17:56:41.453Z",
        "email": "lorelai@thedragonfly.com",
        "firstname": "Lorelai",
        "hs_object_id": "197093183168",
        "lastmodifieddate": "2025-08-05T20:55:06.398Z",
        "lastname": "Gilmore",
    }

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.hubspot.view_contact.get_hubspot_client"
    ) as mock_hubspot_client:
        mock_client = MagicMock()
        mock_hubspot_client.return_value = mock_client

        mock_client.get_request.return_value = {"properties": test_contact_response}

        response: HubspotContact = hubspot_view_contact(test_id)

        assert response
        assert response.first_name == "Lorelai"
        assert response.last_name == "Gilmore"

        mock_client.get_request.assert_called_once_with(
            service="crm",
            version="v3",
            entity=f"objects/contacts/{test_id}",
        )
