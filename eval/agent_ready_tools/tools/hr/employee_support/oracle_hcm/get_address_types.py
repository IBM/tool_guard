from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass(frozen=True)
class AddressTypes:
    """Represents a address type in Oracle HCM."""

    address_type_code: str
    address_type_name: str


@dataclass
class AddressTypeResponse:
    """A list of address types configured for a Oracle HCM deployment."""

    address_types: list[AddressTypes]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_address_types_oracle() -> AddressTypeResponse:
    """
    Gets a list of address types configured for a Oracle HCM deployment.

    Returns:
        A list of address types.
    """

    client = get_oracle_hcm_client()
    response = client.get_request(
        entity="commonLookupsLOV", q_expr="LookupType='ADDRESS_TYPE'", path="fscmRestApi"
    )

    address_types_list: list[AddressTypes] = [
        AddressTypes(
            address_type_code=address.get("LookupCode", ""),
            address_type_name=address.get("Meaning", ""),
        )
        for address in response.get("items", [])
    ]

    return AddressTypeResponse(address_types=address_types_list)
