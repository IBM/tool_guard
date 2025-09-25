from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionSupplierIncomeTaxData,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_supplier_income_tax_data(
    supplier_id: str,
) -> ToolResponse[OracleFusionSupplierIncomeTaxData]:
    """
    Get a supplier's income tax data by their id.

    Args:
        supplier_id: The id of the supplier, returned by the oracle_fusion_get_all_suppliers tool. This ID is obtained by applying filters such as the supplier's name, number, or other relevant criteria.

    Returns:
        A supplier's income tax data
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        resource_name=f"suppliers/{supplier_id}",
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    supplier_income_tax_data = OracleFusionSupplierIncomeTaxData(
        supplier=response.get("Supplier", ""),
        tax_organization_type=response.get("TaxOrganizationType", ""),
        registry_id=response.get("RegistryId", ""),
        tax_registration_country=response.get("TaxRegistrationCountry", ""),
        tax_registration_number=response.get("TaxRegistrationNumber", ""),
        tax_payer_country=response.get("TaxpayerCountry", ""),
        tax_payer_id=response.get("TaxpayerId", ""),
        federal_income_tax_type_code=response.get("FederalIncomeTaxTypeCode", ""),
        federal_income_tax_type=response.get("FederalIncomeTaxType", ""),
        tax_reporting_name=response.get("TaxReportingName", ""),
        withholding_tax_group=response.get("WithholdingTaxGroup", ""),
    )

    return ToolResponse(
        success=True,
        message="Retrieved supplier's income tax data from Oracle Fusion successfully.",
        content=supplier_income_tax_data,
    )
