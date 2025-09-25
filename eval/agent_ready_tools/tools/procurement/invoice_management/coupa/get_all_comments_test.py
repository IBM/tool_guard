from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.get_all_comments import (
    coupa_get_all_comments,
)


def test_coupa_get_all_comments() -> None:
    """Test that the `coupa_get_all_comments` function returns the expected response."""

    test_data = {"invoice_id": 1234}
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.get_all_comments.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "id": 1,
                "comments": "test 1",
            },
            {
                "id": 2,
                "comments": "test 2",
            },
        ]

        comments_list_instance = coupa_get_all_comments(test_data["invoice_id"]).content
        assert comments_list_instance
        assert len(comments_list_instance.comments_list) == 2
