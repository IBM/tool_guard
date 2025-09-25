from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.contract_management.coupa.contract_dataclasses import (
    CoupaContract,
)
from agent_ready_tools.tools.procurement.contract_management.coupa.get_all_contracts import (
    coupa_get_all_contracts,
)


def test_coupa_get_all_contracts() -> None:
    """test the get_all_contracts tool."""

    test_filter_name = "test"
    test_supplier = {"id": 20, "name": "test supplier display name 1", "number": "Test Number"}
    test_contract = {
        "id": 123456,
        "name": "test contract 1",
        "supplier": test_supplier,
        "number": "test contract number 1",
        "status": None,  # Status is provided
        "start-date": "2023-01-01",
        "end-date": "2023-12-31",
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.coupa.get_all_contracts.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client

        # Configure the return value for the method called *by* get_all_contracts
        mock_client.get_request_list.return_value = [test_contract]

        supplier_name_filter = None
        status_filter = None

        response = coupa_get_all_contracts(
            name=test_filter_name,
            supplier_name=supplier_name_filter,
            status=status_filter,
        ).content

        assert response
        assert len(response) == 1
        assert isinstance(response[0], CoupaContract)
        assert response[0].contract_id == test_contract["id"]
        assert response[0].name == test_contract["name"]
        assert response[0].number == test_contract["number"]
        assert response[0].supplier is not None
        assert response[0].supplier.id == test_supplier["id"]
        assert response[0].status == test_contract["status"]
        assert response[0].start_date == test_contract["start-date"]
        assert response[0].end_date == test_contract["end-date"]

        expected_params = {
            "fields": '["id","name","no-of-renewals","number","reason-insight-events","renewal-length-unit","renewal-length-value","status","start-date","end-date",{"supplier": ["name","number","id","status"]},{"department": ["name","id","active"]}]',
            "name[contains]": test_filter_name,
            "limit": 10,
            "offset": 0,
        }

        mock_client.get_request_list.assert_called_once_with(
            resource_name="contracts",
            params=expected_params,
        )


def test_coupa_get_all_contracts_date_filters() -> None:
    """test the get_all_contracts tool."""

    test_supplier = {"name": "test supplier display name 1", "number": "Test Number", "id": 20}
    test_contract = {
        "id": 123456,
        "name": "test contract 1",
        "supplier": test_supplier,
        "number": "test contract number 1",
        "start-date": "2025-07-03",
        "end-date": "2025-10-18",
        "department": None,
    }
    start_date_start_filter = "2025-01-01"
    start_date_end_filter = "2025-12-31"

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.coupa.get_all_contracts.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client

        # Configure the return value for the method called *by* get_all_contracts
        mock_client.get_request_list.return_value = [test_contract]

        response = coupa_get_all_contracts(
            start_date_start=start_date_start_filter,
            start_date_end=start_date_end_filter,
        ).content

        assert response
        assert len(response) == 1
        assert isinstance(response[0], CoupaContract)
        assert response[0].contract_id == test_contract["id"]
        assert response[0].name == test_contract["name"]
        assert response[0].number == test_contract["number"]
        assert response[0].supplier is not None
        assert response[0].supplier.id == test_supplier["id"]
        assert response[0].start_date == test_contract["start-date"]
        assert response[0].end_date == test_contract["end-date"]

        expected_params = {
            "fields": '["id","name","no-of-renewals","number","reason-insight-events","renewal-length-unit","renewal-length-value","status","start-date","end-date",{"supplier": ["name","number","id","status"]},{"department": ["name","id","active"]}]',
            "start-date[gt_or_eq]": start_date_start_filter,
            "start-date[lt_or_eq]": start_date_end_filter,
            "limit": 10,
            "offset": 0,
        }

        mock_client.get_request_list.assert_called_once_with(
            resource_name="contracts",
            params=expected_params,
        )
