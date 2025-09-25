from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionRegistrationStatus,
    OracleFusionTaxRegistrationType,
    OracleFusionUpdateTaxRegistrationResponse,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_update_supplier_tax_registration(
    registration_id: str,
    tax_point_basis: Optional[str] = None,
    registration_type_code: Optional[OracleFusionTaxRegistrationType] = None,
    registration_status_code: Optional[OracleFusionRegistrationStatus] = None,
    registration_reason_code: Optional[str] = None,
    registration_source_code: Optional[str] = None,
    rounding_rule_code: Optional[str] = None,
    tax_authority_id: Optional[int] = None,
    legal_location_id: Optional[int] = None,
) -> ToolResponse[OracleFusionUpdateTaxRegistrationResponse]:
    """
    Update supplier tax registration details in Oracle Fusion.

    Args:
        registration_id: The id of the supplier tax registration, returned by the oracle_fusion_get_supplier_tax_registrations tool.
        tax_point_basis: The receipt transaction process where taxes are accounted and reported to the tax authorities (e.g., "ACCOUNTING", "DELIVERY", "INVOICE", "PAYMENT").
        registration_type_code: The tax registration type issued to the supplier.
        registration_status_code: The registration status code for tax registrations.
        registration_reason_code: The registration reason code for tax registrations (e.g., "MINIMUM_PRESENCE", "REVENUE_THRESHOLD").
        registration_source_code: The registration source code for tax registrations (e.g., "EXPLICIT", "IMPLICIT").
        rounding_rule_code: The rule that defines how the rounding must be performed on a value involved in a taxable transaction. Possible values range from the next highest value to the next lowest or nearest value (e.g., "NEAREST", "DOWN", "UP").
        tax_authority_id: The unique identifier of the tax authority, obtained by calling the oracle_fusion_get_tax_authorities tool.
        legal_location_id: The unique identifier of the legal location, obtained by calling the oracle_fusion_legal_locations tool.

    Returns:
        Updated tax registration details for the selected supplier.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {
        "TaxPointBasis": tax_point_basis.upper() if tax_point_basis else None,
        "RegistrationTypeCode": registration_type_code,
        "RegistrationStatusCode": registration_status_code,
        "RegistrationReasonCode": (
            registration_reason_code.upper() if registration_reason_code else None
        ),
        "RegistrationSourceCode": (
            registration_source_code.upper() if registration_source_code else None
        ),
        "RoundingRuleCode": rounding_rule_code.upper() if rounding_rule_code else None,
        "TaxAuthorityId": tax_authority_id,
        "LegalLocationId": legal_location_id,
    }

    payload = {key: value for key, value in payload.items() if value is not None}

    if not payload:
        return ToolResponse(
            success=False,
            message="No fields provided for update. Please specify at least one field.",
        )

    response = client.patch_request(
        resource_name=f"taxRegistrations/{registration_id}",
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    tax_registration_details = OracleFusionUpdateTaxRegistrationResponse(
        tax_point_basis=response.get("TaxPointBasis", ""),
        registration_type_code=response.get("RegistrationTypeCode", ""),
        registration_status_code=response.get("RegistrationStatusCode", ""),
        registration_reason_code=response.get("RegistrationReasonCode", ""),
        registration_source_code=response.get("RegistrationSourceCode", ""),
        rounding_rule_code=response.get("RoundingRuleCode", ""),
        tax_authority_id=response.get("TaxAuthorityId", -1),
        legal_location_id=response.get("LegalLocationId", -1),
    )

    return ToolResponse(
        success=True,
        message="Updated the tax registration details of a supplier from Oracle Fusion.",
        content=tax_registration_details,
    )
