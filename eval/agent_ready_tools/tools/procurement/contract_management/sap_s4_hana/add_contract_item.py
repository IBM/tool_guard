from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaAddContractItemResponse:
    """Represents the response of adding a contract item in SAP S4 Hana."""

    contract_id: str


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_add_contract_item(
    contract_id: str,
    material_id: str,
    plant: str,
    quantity: str,
    net_price: str,
) -> ToolResponse[S4HanaAddContractItemResponse]:
    """
    Adds item to a contract in SAP S4 Hana.

    Args:
        contract_id: The ID of the contract, returned by the `sap_s4_hana_get_contracts` tool.
        material_id: The ID of the material, returned by the `sap_s4_hana_get_materials` tool.
        plant: The plant ID associated with the material.
        quantity: The required quantity.
        net_price: The net price of the quantity.

    Returns:
        The result of adding a contract item.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload = {
        "PurchaseContract": contract_id,
        "Material": material_id,
        "Plant": plant,
        "TargetQuantity": quantity,
        "ContractNetPriceAmount": net_price,
    }

    response = client.post_request(
        entity=f"100/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract('{contract_id}')/to_PurchaseContractItem",
        payload=payload,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {}).get("value", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    contract_id = response.get("d", {}).get("PurchaseContract", "")
    result = S4HanaAddContractItemResponse(contract_id=contract_id)

    return ToolResponse(
        success=True,
        message="The record was successfully created.",
        content=result,
    )
