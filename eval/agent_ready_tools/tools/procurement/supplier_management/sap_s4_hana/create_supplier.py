from enum import StrEnum
from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


class SAPS4HANASupplierCategory(StrEnum):
    """The category of the supplier."""

    PERSON = "1"
    ORGANIZATION = "2"
    GROUP = "3"


@dataclass
class SAPS4HANACreateSupplierResult:
    """Represents the result of creating a business partner in SAP Hana."""

    supplier_id: str


BUSINESS_PARTNER_ROLE = "FLVN01"  # Defaulting role to supplier to satisfy the use case.


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_create_supplier(
    supplier_name: str, supplier_category: SAPS4HANASupplierCategory, supplier_country: str
) -> ToolResponse[SAPS4HANACreateSupplierResult]:
    """
    Creates a supplier in SAP S4 Hana.

    Args:
        supplier_name: The name of supplier.
        supplier_category: The category of the supplier.
        supplier_country: Country of the supplier in ISO 3166-1 alpha-2 standard.

    Returns:
        Result from creating a supplier
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    supplier_category = SAPS4HANASupplierCategory[supplier_category.upper()]

    payload: dict[str, Any] = {
        "BusinessPartnerCategory": str(supplier_category.value),
        "to_BusinessPartnerRole": [
            {
                "BusinessPartnerRole": BUSINESS_PARTNER_ROLE,
            }
        ],
        "to_BusinessPartnerAddress": [{"Country": supplier_country}],
    }

    if str(supplier_category.value) == SAPS4HANASupplierCategory.PERSON:
        payload["LastName"] = supplier_name
    elif str(supplier_category.value) == SAPS4HANASupplierCategory.ORGANIZATION:
        payload["OrganizationBPName1"] = supplier_name
    elif str(supplier_category.value) == SAPS4HANASupplierCategory.GROUP:
        payload["GroupBusinessPartnerName1"] = supplier_name

    response = client.post_request(entity="API_BUSINESS_PARTNER/A_BusinessPartner", payload=payload)

    if "error" in response:
        content = response.get("error", {}).get("message", {}).get("value", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    supplier_id = response["d"]["BusinessPartner"]

    return ToolResponse(
        success=True,
        message="The supplier was successfully created.",
        content=SAPS4HANACreateSupplierResult(supplier_id=supplier_id),
    )
