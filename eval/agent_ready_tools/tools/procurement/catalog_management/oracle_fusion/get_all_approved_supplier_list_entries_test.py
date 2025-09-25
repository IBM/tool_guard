from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.get_all_approved_supplier_list_entries import (
    oracle_fusion_get_all_approved_supplier_list_entries,
)


def test_oracle_fusion_get_all_approved_supplier_list_entries() -> None:
    """Test that the `get_all_approved_supplier_list_entries` function returns the expected
    response."""

    # Define test data
    test_data: dict[str, Any] = {
        "items": [
            {
                "AslId": 300000025672053,
                "ProcurementBUId": 300000002168484,
                "ProcurementBU": "US1 Business Unit",
                "AslScopeCode": "SHIP_TO_ORG",
                "Scope": "Ship-to Organization",
                "ShipToOrganizationId": 300000002210990,
                "ShipToOrganization": "Seattle",
                "Item": "SCH-01",
                "ItemId": 300000023455123,
                "Supplier": "Bank of IBM",
                "SupplierId": 300000023455796,
                "SupplierSite": "P-Card",
                "SupplierSiteId": 300000023455815,
                "PrimaryVendorItem": "testt",
                "Status": "Approved",
                "AslStatusId": 2,
                "ReviewDueDate": None,
                "DisableFlag": False,
                "Comments": None,
                "AslCreationDate": "2025-08-04T21:49:21.059+00:00",
                "PurchasingUOMCode": "zzu",
                "PurchasingUOM": "Ea",
                "CountryOfOriginCode": "US",
                "CountryOfOrigin": "United States",
                "MinimumOrderQuantity": None,
                "FixedLotMultiple": None,
            },
            {
                "AslId": 300000025672050,
                "ProcurementBUId": 300000002168484,
                "ProcurementBU": "US1 Business Unit",
                "AslScopeCode": "GLOBAL",
                "Scope": "Global",
                "ShipToOrganizationId": -1,
                "ShipToOrganization": None,
                "Item": "SCH-01",
                "ItemId": 300000023455123,
                "Supplier": "United Parcel Service",
                "SupplierId": 300000010011003,
                "SupplierSite": None,
                "SupplierSiteId": None,
                "PrimaryVendorItem": None,
                "Status": "Approved",
                "AslStatusId": 2,
                "ReviewDueDate": "2025-08-30",
                "DisableFlag": False,
                "Comments": None,
                "AslCreationDate": "2025-08-04T21:45:11.001+00:00",
                "PurchasingUOMCode": "zzu",
                "PurchasingUOM": "Ea",
                "CountryOfOriginCode": "US",
                "CountryOfOrigin": "United States",
                "MinimumOrderQuantity": 1,
                "FixedLotMultiple": None,
            },
            {
                "AslId": 300000025672047,
                "ProcurementBUId": 300000002168484,
                "ProcurementBU": "US1 Business Unit",
                "AslScopeCode": "GLOBAL",
                "Scope": "Global",
                "ShipToOrganizationId": -1,
                "ShipToOrganization": None,
                "Item": "PK101",
                "ItemId": 300000016236804,
                "Supplier": "Bank of IBM",
                "SupplierId": 300000023455796,
                "SupplierSite": None,
                "SupplierSiteId": None,
                "PrimaryVendorItem": None,
                "Status": "Approved",
                "AslStatusId": 2,
                "ReviewDueDate": None,
                "DisableFlag": False,
                "Comments": None,
                "AslCreationDate": "2025-08-04T21:33:02.001+00:00",
                "PurchasingUOMCode": None,
                "PurchasingUOM": None,
                "CountryOfOriginCode": None,
                "CountryOfOrigin": None,
                "MinimumOrderQuantity": None,
                "FixedLotMultiple": None,
            },
            {
                "AslId": 300000025229297,
                "ProcurementBUId": 300000002168484,
                "ProcurementBU": "US1 Business Unit",
                "AslScopeCode": "GLOBAL",
                "Scope": "Global",
                "ShipToOrganizationId": -1,
                "ShipToOrganization": None,
                "Item": "PK101",
                "ItemId": 300000016236804,
                "Supplier": "United Parcel Service",
                "SupplierId": 300000010011003,
                "SupplierSite": "UPS US1",
                "SupplierSiteId": 300000010011025,
                "PrimaryVendorItem": None,
                "Status": "Approved",
                "AslStatusId": 2,
                "ReviewDueDate": "2025-07-30",
                "DisableFlag": False,
                "Comments": None,
                "AslCreationDate": "2025-07-29T22:57:34.001+00:00",
                "PurchasingUOMCode": "zzu",
                "PurchasingUOM": "Ea",
                "CountryOfOriginCode": "US",
                "CountryOfOrigin": "United States",
                "MinimumOrderQuantity": None,
                "FixedLotMultiple": None,
            },
        ],
        "count": 4,
        "hasMore": False,
        "limit": 10,
        "offset": 0,
        "links": [
            {
                "rel": "self",
                "href": "https://iavnqy-dev1.fa.ocs.oraclecloud.com:443/fscmRestApi/resources/11.13.18.05/procurementApprovedSupplierListEntries",
                "name": "procurementApprovedSupplierListEntries",
                "kind": "collection",
            }
        ],
    }

    # Patch `get_oracle_fusion_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.get_all_approved_supplier_list_entries.get_oracle_fusion_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = test_data

        # Get all approved supplier list entries
        response = oracle_fusion_get_all_approved_supplier_list_entries().content

        # Ensure that get_all_supplier_list_entries() executed and returned proper values
        assert len(response.supplier_list_entry_list) == 4

        assert response.supplier_list_entry_list[0].asl_id == 300000025672053
        assert response.supplier_list_entry_list[0].item == "SCH-01"
        assert response.supplier_list_entry_list[0].supplier == "Bank of IBM"

        assert response.supplier_list_entry_list[1].asl_id == 300000025672050
        assert response.supplier_list_entry_list[1].item_id == 300000023455123
        assert response.supplier_list_entry_list[1].supplier_id == 300000010011003

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            resource_name="procurementApprovedSupplierListEntries",
            params={"limit": 10, "offset": 0, "orderBy": "AslCreationDate:desc"},
        )
