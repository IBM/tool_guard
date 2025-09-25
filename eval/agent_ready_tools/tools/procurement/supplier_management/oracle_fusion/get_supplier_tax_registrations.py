from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionSupplierTaxRegistrations,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_supplier_tax_registrations(
    party_number: str,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionSupplierTaxRegistrations]]:
    """
    Get a list of tax registrations of a supplier from Oracle Fusion.

    Args:
        party_number: The registry ID of a supplier, returned by the tool `oracle_fusion_get_supplier_income_tax_data`.
        limit: The maximum number of tax registrations to return.
        offset: The number of tax registrations to skip for pagination.

    Returns:
        A list of tax registrations of a supplier
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {"limit": limit, "offset": offset}

    if party_number:
        params["q"] = f"PartyNumber={party_number}"

    response = client.get_request(
        resource_name="taxRegistrations",
        params=params,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No tax registrations returned")

    tax_registrations = []
    for tax_reg in response["items"]:
        tax_registrations.append(
            OracleFusionSupplierTaxRegistrations(
                registration_number=tax_reg["RegistrationNumber"],
                tax_regime_code=tax_reg["TaxRegimeCode"],
                tax=tax_reg["Tax"],
                tax_jurisdiction_code=tax_reg["TaxJurisdictionCode"],
                tax_point_basis=tax_reg["TaxPointBasis"],
                registration_type=tax_reg["RegistrationTypeCode"],
                status=tax_reg["RegistrationStatusCode"],
                reason=tax_reg["RegistrationReasonCode"],
                effective_from=tax_reg["EffectiveFrom"],
                registration_id=tax_reg["RegistrationId"],
            )
        )

    return ToolResponse(
        success=True,
        message="Retrieved list of tax registrations of supplier from Oracle Fusion successfully.",
        content=tax_registrations,
    )
