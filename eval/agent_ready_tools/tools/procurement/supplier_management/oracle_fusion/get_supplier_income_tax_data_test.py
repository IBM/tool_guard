from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_income_tax_data import (
    oracle_fusion_get_supplier_income_tax_data,
)


def test_oracle_fusion_get_supplier_income_tax_data() -> None:
    """Test the getting supplier income tax data from Oracle Fusion using a mock client."""
    test_supplier = {
        "supplier_id": "300000010011003",
        "supplier": "United Parcel Service",
        "tax_organization_type": "Corporation",
        "registry_id": "10078",
        "tax_registration_country": "United States",
        "tax_registration_number": "192837465",
        "tax_payer_country": "Angola",
        "tax_payer_id": "1234",
        "federal_income_tax_type_code": "DAU/AR",
        "federal_income_tax_type": "Miscellaneous - Other",
        "tax_reporting_name": "abctest",
        "withholding_tax_group": "MRBTAXRATE",
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_income_tax_data.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_supplier

        response = oracle_fusion_get_supplier_income_tax_data(
            supplier_id=test_supplier["supplier_id"]
        )

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name=f"suppliers/{test_supplier['supplier_id']}"
        )
