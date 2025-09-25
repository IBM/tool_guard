from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_all_suppliers import (
    oracle_fusion_get_all_suppliers,
)


def test_oracle_fusion_get_all_suppliers() -> None:
    """Test the getting of all suppliers from Oracle Fusion using a mock client."""
    test_supplier = {
        "items": [
            {
                "SupplierId": 8675309,
                "Supplier": "I Got It Inc.",
                "SupplierTypeCode": "TAX AUTHORITY",
                "Status": "Active",
                "CreationDate": "2025-07-28T010:30:00.666+00:00",
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_all_suppliers.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_supplier

        response = oracle_fusion_get_all_suppliers()

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name="suppliers",
            params={"limit": 10, "offset": 0},
        )


def test_oracle_fusion_get_specific_suppliers() -> None:
    """Test the getting of all suppliers from Oracle Fusion using a mock client."""
    test_supplier = {
        "items": [
            {
                "SupplierId": 300000025349107,
                "Supplier": "Baur",
                "SupplierTypeCode": "TAX AUTHORITY",
                "Status": "Active",
                "CreationDate": "2025-07-30T22:37:48.002+00:00",
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_all_suppliers.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_supplier

        response = oracle_fusion_get_all_suppliers(supplier_name="Baur")

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name="suppliers",
            params={"limit": 10, "q": "Supplier=Baur", "offset": 0},
        )
