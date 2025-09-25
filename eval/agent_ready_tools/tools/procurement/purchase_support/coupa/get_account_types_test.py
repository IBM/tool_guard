from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_account_types import (
    coupa_get_account_types,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAccountType,
    CoupaGetAccountTypesResponse,
)


def test_coupa_get_account_types() -> None:
    """test the get_billing_accounts tool."""

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_account_types.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {"id": 2, "name": "CHART100", "active": True, "currency": {"code": "USD"}},
            {"id": 9, "name": "CHART200", "active": True, "currency": {"code": "USD"}},
            {"id": 18, "name": "CHART900", "active": True, "currency": {"code": "USD"}},
        ]

        response = coupa_get_account_types().content

        assert response
        assert response.total_count == 3
        assert isinstance(response, CoupaGetAccountTypesResponse)
        assert len(response.account_types) == 3
        assert isinstance(response.account_types[0], CoupaAccountType)

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="account_types",
            params={
                "active": True,
                "fields": '["id","name","active",{"currency": ["code"]}]',
            },
        )
