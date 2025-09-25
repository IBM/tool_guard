from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionBusinessRelationship,
    OracleFusionSupplierDetails,
    OracleFusionTaxOrganizationType,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_create_supplier(
    supplier: str,
    tax_organization_type: OracleFusionTaxOrganizationType = OracleFusionTaxOrganizationType.CORPORATION,
    business_relationship: OracleFusionBusinessRelationship = OracleFusionBusinessRelationship.PROSPECTIVE,
    supplier_number: Optional[str] = None,
    duns_number: Optional[str] = None,
    taxpayer_country: Optional[str] = None,
) -> ToolResponse[OracleFusionSupplierDetails]:
    """
    Creates or updates a single supplier in Oracle Fusion.

    Args:
        supplier: The legal name of the supplier.
        tax_organization_type: The type of Supplier's Tax Organization in Oracle Fusion.
        business_relationship: The nature of the business relationship in Oracle Fusion.
        supplier_number: The unique identification number for the supplier.
        duns_number: The Dun & Bradstreet D-U-N-S number for the supplier.
        taxpayer_country: The country for tax purposes, typically a two-letter country code.

    Returns:
        A ToolResponse object containing the API response or an error message.
    """
    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError) as e:
        return ToolResponse(success=False, message=f"Failure to retrieve credentials: {e}")

    payload: Dict[str, Any] = {
        key: value
        for key, value in {
            "Supplier": supplier,
            "TaxOrganizationType": tax_organization_type,
            "BusinessRelationship": business_relationship,
            "SupplierNumber": supplier_number,
            "DUNSNumber": duns_number,
            "TaxpayerCountry": taxpayer_country,
        }.items()
        if value not in (None, "", "null", "None")
    }

    response = client.post_request(
        resource_name="suppliers",
        payload=payload,
    )

    if "errors" in response or "error" in response:
        error_message = response.get("errors", response.get("error", "Unknown API error"))
        return ToolResponse(success=False, message=str(error_message))

    supplier_id_from_response = response.get("SupplierId")
    if supplier_id_from_response is None:
        return ToolResponse(
            success=False, message="API did not return a 'SupplierId' in the response."
        )

    output_details = OracleFusionSupplierDetails(
        supplier_id=supplier_id_from_response,
        supplier_name=response.get("Supplier"),
        supplier_status=response.get("Status"),
        supplier_type_code=response.get("SupplierTypeCode"),
        supplier_creation_date=response.get("CreationDate"),
    )

    return ToolResponse(
        success=True,
        message=f"A new Oracle Fusion Supplier was created successfully with ID: {supplier_id_from_response}.",
        content=output_details,
    )
