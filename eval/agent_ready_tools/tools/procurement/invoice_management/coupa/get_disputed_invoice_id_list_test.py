from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.get_disputed_invoice_id_list import (
    CoupaDisputedInvoiceIdList,
    coupa_get_disputed_invoice_id_list,
)


def test_coupa_get_disputed_invoice_id_list() -> None:
    """Test that the get_disputed_invoice_id_list function returns expected invoice IDs."""
    mock_response = [{"id": 713514}, {"id": 713516}, {"id": 713517}, {"id": 713521}]

    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.get_disputed_invoice_id_list.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_client.get_request.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = coupa_get_disputed_invoice_id_list()

        assert isinstance(result, CoupaDisputedInvoiceIdList)
        assert result.disputed_invoice_ids == [713514, 713516, 713517, 713521]
