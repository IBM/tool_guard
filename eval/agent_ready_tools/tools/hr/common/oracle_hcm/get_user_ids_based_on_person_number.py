from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleUserIDs:
    """Represents the response from getting a worker's unique identifiers from Oracle HCM."""

    person_id: Optional[int]
    worker_id: Optional[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_user_ids_based_on_person_number(person_number: str) -> OracleUserIDs:
    """
    Gets a worker's `worker_id` and `person_id` from Oracle HCM.

    Args:
        person_number: The person_number of the worker in Oracle HCM.

    Returns:
        The worker's unique identifiers within Oracle HCM.
    """
    client = get_oracle_hcm_client()

    q_expr = f"PersonNumber='{person_number}'"

    response = client.get_request("workers", q_expr=q_expr, headers={"REST-Framework-Version": "4"})

    if len(response["items"]) == 0:
        return OracleUserIDs(person_id=None, worker_id=None)

    result = response.get("items", [])[0]
    return OracleUserIDs(
        person_id=result.get("PersonId"),
        worker_id=get_id_from_links(result.get("links", [{}])[0].get("href")),
    )
