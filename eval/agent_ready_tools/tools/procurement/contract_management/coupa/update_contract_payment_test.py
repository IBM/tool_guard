from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.contract_management.coupa.update_contract_payment import (
    coupa_update_contract_payment_details,
)


def test_coupa_update_contract_payment_details() -> None:
    """Test update contract payment details using a mock client."""
    test_contract_id = 1047
    test_data: Dict[str, Any] = {
        "payment-term": {"code": "Net 30"},
        "currency": {"code": "USD"},
        "savings-pct": 0.3,
        "stop-spend-based-on-max-value": "yes",
        "shipping-term": {"code": "UPS"},
        "min-commit": "999.99",
        "max-commit": "9999.99",
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.coupa.update_contract_payment.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": test_contract_id,
            "status": "draft",
        }

        response = coupa_update_contract_payment_details(
            contract_id=test_contract_id,
            payment_term=test_data["payment-term"]["code"],
            currency=test_data["currency"]["code"],
            savings_pct=test_data["savings-pct"],
            stop_spend_based_on_max_value=test_data["stop-spend-based-on-max-value"],
            shipping_term=test_data["shipping-term"]["code"],
            min_commit=test_data["min-commit"],
            max_commit=test_data["max-commit"],
        ).content

        assert response

        mock_client.put_request.assert_called_once_with(
            resource_name=f"contracts/{test_contract_id}",
            params={"fields": '["id","status"]'},
            payload=test_data,
        )
