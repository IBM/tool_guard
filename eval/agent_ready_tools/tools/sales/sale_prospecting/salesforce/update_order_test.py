from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_order import update_order


def test_update_order() -> None:
    """Test that the `update_order` function returns the expected response."""

    expected = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_order.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Order.update.return_value = 204

        # Update Order
        response = update_order(order_id="801gL000005hhmoQAA", owner_id="005gL000001aT2vQAE")

        # Ensure that update_order() executed and returned proper values
        assert response
        assert response == expected
