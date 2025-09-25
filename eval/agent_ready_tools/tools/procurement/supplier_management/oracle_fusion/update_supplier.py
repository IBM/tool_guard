from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionUpdateSupplierResponse,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_update_supplier(
    supplier_id: int,
    supplier_name: Optional[str] = None,
    supplier_tax_country: Optional[str] = None,
    corporate_website: Optional[str] = None,
    year_established: Optional[str] = None,
    mission_statement: Optional[str] = None,
    alternate_name: Optional[str] = None,
    status: Optional[str] = None,
    duns_number: Optional[str] = None,
    taxpayer_id: Optional[str] = None,
    tax_registration_country: Optional[str] = None,
    tax_registration_number: Optional[str] = None,
    federal_income_tax_type: Optional[str] = None,
) -> ToolResponse[OracleFusionUpdateSupplierResponse]:
    """
    Updates the supplier in Oracle Fusion.

    Args:
        supplier_id: The id of the supplier.
        supplier_name: The name of the supplier.
        supplier_tax_country: Tax country.
        corporate_website: Company website.
        year_established: Year Established.
        mission_statement: Mission statement.
        alternate_name: Alternate Name.
        status: Status.
        duns_number: Duns Number.
        taxpayer_id: Tax Payer ID.
        tax_registration_country: Tax Registration.
        tax_registration_number: Tax Reg Number.
        federal_income_tax_type: Federal Income Tax Type.

    Returns:
        The supplier id of the update response.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: dict[str, Any] = {}
    optional_fields = {
        "Supplier": supplier_name,
        "SupplierTaxCountry": supplier_tax_country,
        "CorporateWebsite": corporate_website,
        "YearEstablished": year_established,
        "MissionStatement": mission_statement,
        "AlternateName": alternate_name,
        "Status": status,
        "DUNSNumber": duns_number,
        "TaxpayerId": taxpayer_id,
        "TaxRegistrationCountry": tax_registration_country,
        "TaxRegistrationNumber": tax_registration_number,
        "FederalIncomeTaxType": federal_income_tax_type,
    }

    for key, value in optional_fields.items():
        if value is not None:
            payload[key] = value

    response = client.patch_request(
        resource_name=f"suppliers/{supplier_id}",
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["errors"]
        )

    if "fault" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=response["fault"]["faultstring"]
        )

    return ToolResponse(
        success=True, message="The data was successfully updated", content=response["SupplierId"]
    )
