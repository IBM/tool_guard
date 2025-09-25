from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_sites import (
    oracle_fusion_get_supplier_sites,
)


def test_oracle_fusion_get_supplier_sites() -> None:
    """Test the getting of supplier's sites from Oracle Fusion using a mock client."""

    test_site_result = {
        "items": [
            {
                "SupplierSiteId": 123,
                "SupplierSite": "Site 1",
                "ProcurementBU": "BU 1",
                "SupplierAddressName": "address 1",
            }
        ]
    }

    test_data = {"supplier_id": "434334"}

    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.get_supplier_sites.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = test_site_result

        response = oracle_fusion_get_supplier_sites(supplier_id=test_data["supplier_id"])

        assert response
        assert response.content is not None
        assert response.content[0].site_name == test_site_result["items"][0]["SupplierSite"]
        assert (
            response.content[0].address_name == test_site_result["items"][0]["SupplierAddressName"]
        )

        mock_client.get_request.assert_called_once_with(
            resource_name=f"suppliers/{test_data['supplier_id']}/child/sites",
            params={"limit": 20, "offset": 0},
        )
