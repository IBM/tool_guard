from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.sourcing.coupa.create_quote_request_event import (
    coupa_create_quote_request_event,
)


def test_coupa_create_quote_request_event() -> None:
    """Test that rfp was created successfully by the `create_quote_request_event` tool."""

    # Define test data:
    test_data = {
        "event_name": "Agent-6",
        "quantity": "2",
        "price_amount": "100",
        "line_type": "item",
        "item": "Agent - 2",
        "supplier_name": "WxO_Coupa_Supplier1",
        "supplier_email": "manepalli.pavan.santosh@partner.ibm.com",
        "commodity_name": "food",
        "state": "new",
        "event_id": "1",
    }

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.create_quote_request_event.get_coupa_client"
    ) as mock_coupa_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "description": test_data["event_name"],
            "state": test_data["state"],
            "id": test_data["event_id"],
        }

        # Call the function under test
        response = coupa_create_quote_request_event(
            event_name=test_data["event_name"],
            quantity=test_data["quantity"],
            price_amount=test_data["price_amount"],
            line_type=test_data["line_type"],
            item=test_data["item"],
            supplier_name=test_data["supplier_name"],
            supplier_email=test_data["supplier_email"],
            commodity_name=test_data["commodity_name"],
        ).content

        # Ensure that create_an_rfp() executed and returned proper values
        assert response
        print(response.event_name)
        print(response)
        assert response.event_name == test_data["event_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            resource_name="quote_requests",
            payload={
                "event-type": "rfp",
                "description": test_data["event_name"],
                "lines": [
                    {
                        "type": "QuoteRequestQuantityLine",
                        "quantity": test_data["quantity"],
                        "price-amount": test_data["price_amount"],
                        "description": test_data["item"],
                    }
                ],
                "quote-suppliers": [
                    {
                        "name": test_data["supplier_name"],
                        "email": test_data["supplier_email"],
                    }
                ],
                "commodity": {"name": test_data["commodity_name"]},
            },
        )


def test_create_rfp_event_mul_suppliers() -> None:
    """Test that rfp with multiple suppliers was created successfully by the `create_rfp_event`
    tool."""

    # Define test data:
    test_data = {
        "event_name": "Agent-6",
        "quantity": "2",
        "price_amount": "100",
        "line_type": "item",
        "item": "Agent - 2",
        "commodity_name": "food",
        "state": "new",
        "event_id": "1",
    }
    # List of supplier names and supplier emails
    suppliers_names = (["Supplier1", "Suppliers2"],)
    suppliers_emails = (["supplier1@ibm.com", "supplier2@ibm.com"],)

    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.create_quote_request_event.get_coupa_client"
    ) as mock_coupa_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "description": test_data["event_name"],
            "state": test_data["state"],
            "id": test_data["event_id"],
        }

        # Call the function under test
        response = coupa_create_quote_request_event(
            event_name=test_data["event_name"],
            quantity=test_data["quantity"],
            price_amount=test_data["price_amount"],
            line_type=test_data["line_type"],
            item=test_data["item"],
            supplier_name=suppliers_names,
            supplier_email=suppliers_emails,
            commodity_name=test_data["commodity_name"],
        ).content

        assert response
        assert response.event_name == test_data["event_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            resource_name="quote_requests",
            payload={
                "event-type": "rfp",
                "description": test_data["event_name"],
                "lines": [
                    {
                        "type": "QuoteRequestQuantityLine",
                        "quantity": test_data["quantity"],
                        "price-amount": test_data["price_amount"],
                        "description": test_data["item"],
                    }
                ],
                "quote-suppliers": [
                    {"name": name, "email": email}
                    for name, email in zip(suppliers_names, suppliers_emails)
                ],
                "commodity": {"name": test_data["commodity_name"]},
            },
        )
