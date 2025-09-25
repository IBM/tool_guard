from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.contract_management.coupa.contract_dataclasses import (
    CoupaContract,
)
from agent_ready_tools.tools.procurement.contract_management.coupa.get_contract_details import (
    coupa_get_contract_details,
)
from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaInvoicePaymentTerm,
)
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaSupplierDetails,
)


def test_coupa_get_contract_details() -> None:
    """Test the get_contract_details tool with a mocked Coupa client."""

    test_contract_number = 1065
    test_supplier = {
        "name": "Test WO",
        "number": "1234563",
        "id": 20,
        "status": "active",
    }
    test_payment_term = {"id": 3, "code": "2/10 Net 30"}
    test_contract = {
        "id": 1065,
        "name": "Baur Tool Test #4",
        "no-of-renewals": 1,
        "number": "BaurToolTest4",
        "reason-insight-events": ["Testing reasons"],
        "renewal-length-unit": "months",
        "renewal-length-value": 12,
        "status": "draft",
        "start-date": "2025-04-17T00:00:00-07:00",
        "end-date": None,
        "supplier": test_supplier,
        "payment-term": test_payment_term,
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.coupa.get_contract_details.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Set the return value for get_request to our test contract
        mock_client.get_request.return_value = test_contract

        # Call the tool with the test contract ID
        response = coupa_get_contract_details(contract_id=test_contract_number).content

        # Assertions
        assert len(response) == 1
        contract = response[0]
        assert isinstance(contract, CoupaContract)
        assert contract.contract_id == test_contract["id"]
        assert contract.name == test_contract["name"]
        assert contract.no_of_renewals == test_contract["no-of-renewals"]
        assert contract.number == test_contract["number"]
        assert contract.reason_insight_events == test_contract["reason-insight-events"]
        assert contract.renewal_length_unit == test_contract["renewal-length-unit"]
        assert contract.renewal_length_value == test_contract["renewal-length-value"]
        assert contract.status == test_contract["status"]
        assert contract.start_date == test_contract["start-date"]
        assert contract.end_date == test_contract["end-date"]

        assert isinstance(contract.supplier, CoupaSupplierDetails)
        assert contract.supplier.name == test_supplier["name"]
        assert contract.supplier.number == test_supplier["number"]
        assert contract.supplier.id == test_supplier["id"]
        assert contract.supplier.status == test_supplier["status"]

        assert isinstance(contract.payment_term, CoupaInvoicePaymentTerm)
        assert contract.payment_term.id == test_payment_term["id"]
        assert contract.payment_term.code == test_payment_term["code"]

        # Verify the call to get_request was correct
        mock_client.get_request.assert_called_once_with(
            resource_name=f"contracts/{test_contract_number}"
        )
