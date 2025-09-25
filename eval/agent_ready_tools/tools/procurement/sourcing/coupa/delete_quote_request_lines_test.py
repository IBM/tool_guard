from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.sourcing.coupa.delete_quote_request_lines import (
    coupa_delete_quote_request_lines,
)


def test_delete_line_success() -> None:
    """delete quote request line."""
    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.delete_quote_request_lines.get_coupa_client"
    ) as mock_get_client:

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        quote_request_id = 1234
        line_id = 5678

        mock_client.get_request.return_value = {
            "id": quote_request_id,
            "state": "draft",
            "lines": [{"id": line_id}, {"id": 9999}],
        }

        mock_client.put_request.return_value = {"id": quote_request_id}

        result = coupa_delete_quote_request_lines(quote_request_id, line_id).content

        assert result is True
        mock_client.put_request.assert_called_once()


def test_delete_line_not_draft() -> None:
    """delete lines when rfp quote request is not in draft."""
    with patch(
        "agent_ready_tools.tools.procurement.sourcing.coupa.delete_quote_request_lines.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "id": 1234,
            "state": "complete",
            "lines": [{"id": 5678}],
        }

        result = coupa_delete_quote_request_lines(1234, 5678).content

        assert result is False
        mock_client.put_request.assert_not_called()
