from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class MaritalStatus:
    """Represents a category of marital status."""

    martial_status_id: str
    description: Optional[str] = None


@dataclass
class MaritalStatusResponse:
    """Represents the response of employee's marital statuses in Oracle HCM."""

    lookups: List[MaritalStatus]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_marital_statuses() -> MaritalStatusResponse:
    """
    Gets lookup code from Oracle HCM.

    Returns:
        The marital status martial_status_ids.
    """
    client = get_oracle_hcm_client()

    response = client.get_request(
        "commonLookupsLOV", q_expr="LookupType='MAR_STATUS'", path="fscmRestApi"
    )

    common_lookups: list[MaritalStatus] = []

    for result in response["items"]:
        common_lookups.append(
            MaritalStatus(
                description=result.get("Meaning", ""),
                martial_status_id=result.get("LookupCode", ""),
            )
        )

    return MaritalStatusResponse(lookups=common_lookups)
