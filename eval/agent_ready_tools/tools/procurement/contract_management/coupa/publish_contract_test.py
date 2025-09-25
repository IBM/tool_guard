from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.contract_management.coupa.publish_contract import (
    coupa_publish_contract,
)


def test_coupa_publish_contract() -> None:
    """Test publish contract using a mock client."""
    test_contract_id = 1234

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.coupa.publish_contract.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": test_contract_id,
            "status": "approved",
        }

        response = coupa_publish_contract(
            contract_id=test_contract_id,
        ).content

        assert response

        mock_client.put_request.assert_called_once_with(
            resource_name=f"contracts/{test_contract_id}",
            params={"fields": '["id","status"]'},
            payload={"status": "published"},
        )
