from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_accounts import (
    coupa_get_accounts,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAccount,
    CoupaGetAccountsResponse,
)


def test_coupa_get_accounts() -> None:
    """test the get_accounts tool."""

    test_account_type_id = 1

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_accounts.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "id": 13,
                "name": "San Francisco - Marketing, Indirect",
                "code": "SF-Marketing-Indirect",
                "active": True,
                "account-type-id": 1,
            },
            {
                "id": 14,
                "name": "San Francisco - Marketing, Assets",
                "code": "SF-Marketing-Assets",
                "active": True,
                "account-type-id": 1,
            },
            {
                "id": 15,
                "name": "San Francisco - Finance, Indirect",
                "code": "SF-Finance-Indirect",
                "active": True,
                "account-type-id": 1,
            },
        ]

        response = coupa_get_accounts(test_account_type_id).content

        assert response
        assert response.total_count == 3
        assert isinstance(response, CoupaGetAccountsResponse)
        assert len(response.accounts) == 3
        assert isinstance(response.accounts[0], CoupaAccount)

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="accounts",
            params={
                "active": True,
                "account-type-id": test_account_type_id,
                "fields": '["id", "name", "code", "active", "account-type-id"]',
                "limit": 10,
                "offset": 0,
            },
        )
