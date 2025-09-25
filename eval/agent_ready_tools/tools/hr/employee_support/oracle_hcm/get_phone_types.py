from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass(frozen=True)
class PhoneTypes:
    """Represents a phone type in Oracle HCM."""

    phone_type_code: str
    phone_type_name: str


@dataclass
class PhoneTypeResponse:
    """A list of phone types configured for a Oracle HCM deployment."""

    phone_types: List[PhoneTypes]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_phone_types_oracle() -> PhoneTypeResponse:
    """
    Gets a list of phone types configured for a Oracle HCM deployment.

    Returns:
        A list of phone types.
    """

    client = get_oracle_hcm_client()
    response = client.get_request(
        entity="commonLookupsLOV", q_expr="LookupType='PHONE_TYPE'", path="fscmRestApi"
    )

    phone_types_list = [
        PhoneTypes(
            phone_type_code=phone.get("LookupCode", ""),
            phone_type_name=phone.get("Meaning", ""),
        )
        for phone in response.get("items", [])
    ]

    return PhoneTypeResponse(phone_types=phone_types_list)
