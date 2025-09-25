from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class AddressTypesResponse:
    """A list of address types configured for a SuccessFactors deployment."""

    address_types: list[str]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_address_types_sap() -> AddressTypesResponse:
    """
    Gets a list of address types configured for this SuccessFactors deployment.

    Returns:
        A list of address types.
    """
    client = get_sap_successfactors_client()
    response = client.get_picklist_options(picklist_field="addressType")

    address_types = [
        address_type["externalCode"] for address_type in response["d"]["picklistOptions"]["results"]
    ]
    return AddressTypesResponse(address_types=address_types)
