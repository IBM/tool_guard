from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_tax_registrations import (
    oracle_fusion_get_supplier_tax_registrations,
)


def test_oracle_fusion_get_supplier_tax_registrations() -> None:
    """Test the retrieval of tax registrations of a supplier from Oracle Fusion using a mock
    client."""
    test_tax_reg = {
        "items": [
            {
                "RegistrationNumber": "1892039",
                "TaxRegimeCode": "ABC TAX CODE",
                "Tax": "ABC GST INPUT TAX",
                "TaxJurisdictionCode": "ABC CA JURISDICTION",
                "TaxPointBasis": "ACCOUNTING",
                "RegistrationTypeCode": "CPF",
                "RegistrationStatusCode": "REGISTERED",
                "RegistrationReasonCode": "REVENUE_THRESHOLD",
                "EffectiveFrom": "2025-07-30",
                "RegistrationId": "300000025229353",
            }
        ],
    }

    test_data = {"party_number": "46196"}

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_tax_registrations.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_tax_reg

        response = oracle_fusion_get_supplier_tax_registrations(
            party_number=test_data["party_number"]
        )

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name="taxRegistrations",
            params={"limit": 10, "offset": 0, "q": f"PartyNumber={test_data["party_number"]}"},
        )
