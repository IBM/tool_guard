from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.contract_management.coupa.update_contract_department import (
    coupa_update_contract_department,
)


def test_coupa_update_contract_department() -> None:
    """Test updating the department of a contract."""
    test_contract_id = 1082
    test_department_id = 20
    expected_payload = {"department": {"id": test_department_id}}
    mock_api_success_response = {
        "id": test_contract_id,
        "status": "draft",
        "department": {"id": test_department_id, "name": "Canada"},
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.coupa.update_contract_department.get_coupa_client"
    ) as mock_get_coupa_client:
        mock_client = MagicMock()
        mock_get_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = mock_api_success_response

        response = coupa_update_contract_department(
            test_contract_id,
            test_department_id,
        ).content

        assert response

        mock_client.put_request.assert_called_once_with(
            resource_name=f"contracts/{test_contract_id}",
            params={"fields": '["id","status"]'},
            payload=expected_payload,
        )
