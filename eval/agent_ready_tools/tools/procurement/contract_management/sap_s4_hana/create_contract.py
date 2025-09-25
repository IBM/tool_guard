from typing import Any, Dict, List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.common_classes_contract_management import (
    SAPS4HANAContractTypes,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaCreateContractResponse:
    """Represents the response of creating a contract in SAP S4 Hana."""

    contract_id: str
    supplier_id: str


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_create_contract(
    supplier_id: str,
    contract_type: SAPS4HANAContractTypes,
    company_code: str,
    purchasing_organization: str,
    purchasing_group: str,
    validity_end_date: str,
    material_id: str,
    plant: str,
    quantity: str,
    net_price: str,
) -> ToolResponse[S4HanaCreateContractResponse]:
    """
    Creates a purchasing contract in SAP S4 HANA.

    Args:
        supplier_id: The unique identifier of the supplier, returned by the `sap_s4_hana_get_suppliers` tool.
        contract_type: The type of contract.
        company_code: The company code of the supplier.
        purchasing_organization: The purchasing organization of the supplier.
        purchasing_group: The purchasing group of the supplier.
        validity_end_date: The validity end date for the contract in ISO 8601 format (e.g., YYYY-MM-DD).
        material_id: The unique identifier of the material, returned by the `sap_s4_hana_get_materials` tool.
        plant: The plant ID associated with the material.
        quantity: The required quantity.
        net_price: The net price of the quantity.

    Returns:
        The result of creating a contract, including the contract ID and supplier ID.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    item_details: List[Dict[str, Any]] = [
        {
            "Material": material_id,
            "Plant": plant,
            "TargetQuantity": quantity,
            "ContractNetPriceAmount": net_price,
        }
    ]

    validity_end_date = iso_8601_to_sap_date(validity_end_date)

    payload: Dict[str, Any] = {
        "PurchaseContractType": SAPS4HANAContractTypes[contract_type.upper()].value,
        "Supplier": supplier_id,
        "CompanyCode": company_code,
        "PurchasingOrganization": purchasing_organization,
        "PurchasingGroup": purchasing_group,
        "ValidityEndDate": validity_end_date,
        "to_PurchaseContractItem": {"results": item_details},
    }

    response = client.post_request(
        entity="100/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract",
        payload=payload,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {}).get("value", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    contract_id = response.get("d", {}).get("PurchaseContract", "")
    supplier_id = response.get("d", {}).get("Supplier", "")
    result = S4HanaCreateContractResponse(contract_id=contract_id, supplier_id=supplier_id)

    return ToolResponse(
        success=True,
        message="The record was successfully created.",
        content=result,
    )
