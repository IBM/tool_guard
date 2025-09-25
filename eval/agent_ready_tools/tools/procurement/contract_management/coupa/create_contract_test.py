from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.contract_management.coupa.contract_dataclasses import (
    CoupaContractRenewalLengthUnit,
)
from agent_ready_tools.tools.procurement.contract_management.coupa.create_contract import (
    coupa_create_contract,
)


def test_create_contract_mock() -> None:
    """Test create contract using a mock client."""
    test_data: Dict[str, Any] = {
        "name": "test-contract",
        "number": "testemail@email.com",
        "no-of-renewals": 1,
        "reason-insight-events": [],
        "renewal-length-unit": CoupaContractRenewalLengthUnit.YEARS,
        "renewal-length-value": 1,
        "status": "draft",
        "start-date": "2025-01-01",
        "supplier": {"id": "20"},
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.coupa.create_contract.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.post_request.return_value = {"id": "1234", "status": "draft"}

        response = coupa_create_contract(
            name=test_data["name"],
            number=test_data["number"],
            no_of_renewals=test_data["no-of-renewals"],
            reason_insight_events=test_data["reason-insight-events"],
            renewal_length_unit=test_data["renewal-length-unit"],
            renewal_length_value=test_data["renewal-length-value"],
            status=test_data["status"],
            start_date=test_data["start-date"],
            supplier_id=test_data["supplier"]["id"],
        ).content

        assert response
        assert isinstance(response.id, int)
        assert response.status == test_data["status"]

        mock_client.post_request.assert_called_once_with(
            resource_name="contracts",
            params={"fields": '["id","status"]'},
            payload=test_data,
        )
