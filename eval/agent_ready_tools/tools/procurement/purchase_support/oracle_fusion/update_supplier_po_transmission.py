from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.purchase_dataclasses import (
    OracleFusionSupplierPOTransmission,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_update_supplier_po_transmission(
    purchase_order_id: str,
    supplier_id: Optional[str] = None,
    supplier_site_id: Optional[str] = None,
    communication_method: Optional[str] = None,
    supplier_fax: Optional[str] = None,
    supplier_email: Optional[str] = None,
    supplier_cc_email: Optional[str] = None,
    supplier_bcc_email: Optional[str] = None,
) -> ToolResponse[OracleFusionSupplierPOTransmission]:
    """
    Update supplier purchase order transmission in Oracle Fusion.

    Args:
        purchase_order_id: The id of the purchase order, returned by the tool `oracle_fusion_get_all_purchase_orders`.
        supplier_id: The id of the supplier, returned by the `oracle_fusion_get_all_suppliers` tool. This ID is obtained by
            applying filters such as the supplier's name, number, or other relevant criteria.
        supplier_site_id: The id of a supplier site, obtained by calling the `oracle_fusion_get_supplier_sites` tool using the supplier_id.
        communication_method: The communication method of the supplier purchase order transmission, possible values are NONE, FAX, EMAIL, PRINT.
        supplier_fax: The fax number of the supplier, mandatory if the chosen communication method is FAX.
        supplier_email: The email address of the supplier, mandatory if the chosen communication method is EMAIL.
        supplier_cc_email: The CC email address of the supplier, can only be updated if the chosen communication method is EMAIL.
        supplier_bcc_email: The BCC email address of the supplier, can only be updated if the chosen communication method is EMAIL.

    Returns:
        Updated supplier purchase order transmission details.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {
        "SupplierId": supplier_id,
        "SupplierSiteId": supplier_site_id,
        "SupplierCommunicationMethod": communication_method,
        "SupplierCCEmailAddress": supplier_cc_email,
        "SupplierBCCEmailAddress": supplier_bcc_email,
    }

    payload = {key: value for key, value in payload.items() if value}

    if communication_method == "EMAIL":
        payload["SupplierEmailAddress"] = supplier_email
    elif communication_method == "FAX":
        payload["SupplierFax"] = supplier_fax

    if not payload:
        return ToolResponse(
            success=False,
            message="No fields provided for update. Please specify at least one field.",
        )

    response = client.patch_request(
        resource_name=f"draftPurchaseOrders/{purchase_order_id}",
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    supplier_po_transmission = OracleFusionSupplierPOTransmission(
        supplier_id=response.get("SupplierId", -1),
        supplier_site_id=response.get("SupplierSiteId", -1),
        communication_method=response.get("SupplierCommunicationMethod", ""),
        supplier_fax=response.get("SupplierFax", ""),
        supplier_email=response.get("SupplierEmailAddress", ""),
        supplier_cc_email=response.get("SupplierCCEmailAddress", ""),
        supplier_bcc_email=response.get("SupplierBCCEmailAddress", ""),
    )

    return ToolResponse(
        success=True,
        message="Updated the supplier purchase order transmission in Oracle Fusion.",
        content=supplier_po_transmission,
    )
