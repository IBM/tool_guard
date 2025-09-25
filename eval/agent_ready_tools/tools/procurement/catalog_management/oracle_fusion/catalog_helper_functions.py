from typing import Any, Dict

from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.catalog_dataclasses import (
    OracleFusionApprovedSupplierListEntry,
)
from agent_ready_tools.utils.date_conversion import iso_8601_datetime_convert_to_date


def oracle_fusion_build_approved_supplier_list_entry_from_response(
    response: Dict[str, Any],
) -> OracleFusionApprovedSupplierListEntry:
    """
    Utility function to build approved supplier list entry given an individual entry response in the
    list.

    Args:
        response: The response of an approved supplier list entry

    Returns:
        The constructed approved supplier list entry.
    """
    return OracleFusionApprovedSupplierListEntry(
        asl_id=response["AslId"],
        procurement_business_unit_id=response.get("ProcurementBUId", -1),
        procurement_business_unit=response.get("ProcurementBU", ""),
        scope=response["Scope"],
        ship_to_organization=response.get("ShipToOrganization"),
        item=response["Item"],
        item_id=response["ItemId"],
        supplier=response["Supplier"],
        supplier_id=response["SupplierId"],
        supplier_site=response.get("SupplierSite"),
        supplier_site_id=response.get("SupplierSiteId"),
        supplier_primary_vendor_item=response.get("PrimaryVendorItem"),
        status=response["Status"],
        review_due_date=response.get("ReviewDueDate"),
        comments=response.get("Comments"),
        created_at=iso_8601_datetime_convert_to_date(response["AslCreationDate"]),
        purchasing_uom=response.get("PurchasingUOM"),
        country_name=response.get("CountryOfOrigin"),
        minimum_order_quantity=response.get("MinimumOrderQuantity"),
        fixed_lot_multiple=response.get("FixedLotMultiple"),
    )
