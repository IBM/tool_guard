from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANASupplier:
    """Represents a supplier in SAP S4 HANA."""

    supplier_id: str
    supplier_name: Optional[str] = None
    supplier_company_name: Optional[str] = None
    creation_date: Optional[str] = None
    created_by: Optional[str] = None
    currency: Optional[str] = None


@dataclass
class S4HANASuppliersResponse:
    """A response containing the list of suppliers from SAP S4 HANA."""

    suppliers: List[S4HANASupplier]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_suppliers(
    supplier_id: Optional[str] = None,
    supplier_name: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANASuppliersResponse]:
    """
    Gets a list of suppliers from SAP S4 HANA.

    Args:
        supplier_id: The supplier's id uniquely identifying them within the SAP S4 HANA.
        supplier_name: The name of the supplier in SAP S4 HANA.
        limit: The number of suppliers returned.
        skip: The number of suppliers to skip for pagination.

    Returns:
        A list of suppliers.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    filter_expr = None
    if supplier_id and supplier_name:
        filter_expr = f"Supplier eq '{supplier_id}' and SupplierName eq '{supplier_name}'"
    elif supplier_id:
        filter_expr = f"Supplier eq '{supplier_id}'"
    elif supplier_name:
        filter_expr = f"SupplierName eq '{supplier_name}'"

    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity="API_BUSINESS_PARTNER/A_Supplier",
        filter_expr=filter_expr,
        expand_expr=f"to_SupplierPurchasingOrg",
        params=params,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    suppliers = [
        S4HANASupplier(
            supplier_name=item.get("SupplierName", ""),
            supplier_id=item.get("Supplier", ""),
            supplier_company_name=item.get("SupplierFullName", ""),
            creation_date=sap_date_to_iso_8601(item.get("CreationDate", "")),
            created_by=item.get("CreatedByUser", ""),
            currency=(
                item.get("to_SupplierPurchasingOrg", {})
                .get("results", [{}])[0]
                .get("PurchaseOrderCurrency", "")
                if isinstance(item.get("to_SupplierPurchasingOrg", {}).get("results"), list)
                and item.get("to_SupplierPurchasingOrg", {}).get("results")
                else ""
            ),
        )
        for item in response["response"]["d"]["results"]
    ]

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=S4HANASuppliersResponse(suppliers=suppliers),
    )
