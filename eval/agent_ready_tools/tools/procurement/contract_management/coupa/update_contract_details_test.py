from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.contract_management.coupa.contract_dataclasses import (
    CoupaContractRenewalLengthUnit,
)
from agent_ready_tools.tools.procurement.contract_management.coupa.update_contract_details import (
    coupa_update_contract_details,
)


def test_coupa_update_contract_details() -> None:
    """Test update contract details using a mock client."""
    test_contract_id = 1234
    test_data: Dict[str, Any] = {
        "no-of-renewals": 1,
        "reason-insight-events": "test",
        "renewal-length-unit": CoupaContractRenewalLengthUnit.YEARS,
        "renewal-length-value": 1,
        "start-date": "2025-01-01",
        "end-date": "2026-01-01",
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.coupa.update_contract_details.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": test_contract_id,
            "status": "draft",
        }

        response = coupa_update_contract_details(
            contract_id=test_contract_id,
            no_of_renewals=test_data["no-of-renewals"],
            reason_insight_events=test_data["reason-insight-events"],
            renewal_length_unit=test_data["renewal-length-unit"],
            renewal_length_value=test_data["renewal-length-value"],
            start_date=test_data["start-date"],
            end_date=test_data["end-date"],
        ).content

        assert response

        mock_client.put_request.assert_called_once_with(
            resource_name=f"contracts/{test_contract_id}",
            params={"fields": '["id","status"]'},
            payload=test_data,
        )


def test_coupa_update_contract_end_date() -> None:
    """Test update contract details using a mock client."""
    test_contract_id = 1132
    test_data: Dict[str, Any] = {
        "start-date": "2025-01-01",
        "end-date": "2026-01-01",
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.coupa.update_contract_details.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": test_contract_id,
            "status": "draft",
        }

        response = coupa_update_contract_details(
            contract_id=test_contract_id,
            start_date=test_data["start-date"],
            end_date=test_data["end-date"],
        ).content

        assert response

        mock_client.put_request.assert_called_once_with(
            resource_name=f"contracts/{test_contract_id}",
            params={"fields": '["id","status"]'},
            payload=test_data,
        )
