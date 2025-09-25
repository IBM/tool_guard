from enum import StrEnum
from typing import Optional

from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse


class FunctionOfPartner(StrEnum):
    """Enum specifying the contact person functions in SAP S4 HANA."""

    EXECUTIVE_BOARD = "0001"
    PURCHASING_MANAGER = "0002"
    SALES_MANAGER = "0003"
    HEAD_OF_PERSONNEL = "0004"
    QUALITY_OFFICER = "0005"
    PRODUCTION_MANAGER = "0006"
    PERSONAL_ASSISTANT = "0007"
    IT_MANAGER = "0008"
    FINANCIAL_ACCOUNTING_MANAGER = "0009"
    MARKETING_MANAGER = "0010"


class Department(StrEnum):
    """Enum specifying the contact person departments in SAP S4 HANA."""

    MANAGING_DIRECTOR = "0001"
    PURCHASING = "0002"
    SALES = "0003"
    ORGANIZATION = "0004"
    ADMINISTRATION = "0005"
    PRODUCTION = "0006"
    QUALITY_ASSURANCE = "0007"
    SECRETARY_OFFICE = "0008"
    FINANCIAL_DEPARTMENT = "0009"
    LEGAL_DEPARTMENT = "0010"


class SAPS4HANASupplierCategory(StrEnum):
    """Represents the category of the supplier in Coupa."""

    PERSON = "1"
    ORGANIZATION = "2"
    GROUP = "3"


@dataclass
class S4HanaBusinessPartner:
    """Represents a business partner in SAP S4 HANA."""

    business_partner_id: str


def get_business_partner_id_of_supplier(supplier_id: str) -> ToolResponse[S4HanaBusinessPartner]:
    """
    Gets the business partner id of a supplier.

    Args:
        supplier_id: The id of the supplier.

    Returns:
        The business partner id of the supplier.
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    response = client.get_request(
        entity="API_BUSINESS_PARTNER/A_BusinessPartner", filter_expr=f"Supplier eq '{supplier_id}'"
    )

    if isinstance(response, dict):
        if "error" in response:
            status_code = response.get("error", {}).get("message", {}).get("status_code", "Unknown")
            content = (
                f"{status_code} : {response.get("error", {}).get("message", {}).get("value", "")}"
            )
            return ToolResponse(success=False, message=f"Request unsuccessful {content}")
        if "fault" in response:
            return ToolResponse(
                success=False,
                message="Request unsuccessful",
                content=response.get("fault", {}).get("faultstring", ""),
            )

    results = response.get("response", {}).get("d", {}).get("results", [])
    for item in results:
        business_partner_id = item.get("BusinessPartner", "")
        if business_partner_id:
            bp_data = S4HanaBusinessPartner(business_partner_id=business_partner_id)
            return ToolResponse(success=True, message="Success", content=bp_data)

    return ToolResponse(success=False, message="Supplier not found")


@dataclass
class S4HanaSupplierAddress:
    """Represents a supplier address in SAP S4 HANA."""

    address_id: Optional[str] = None
    street_name: Optional[str] = None
    house_number: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    time_zone: Optional[str] = None
