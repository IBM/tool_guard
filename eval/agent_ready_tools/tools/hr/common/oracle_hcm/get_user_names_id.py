from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UserNameID:
    """Represents the response from getting a user's unique identifiers from Oracle HCM."""

    names_id: Optional[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_user_names_id(
    email: str,
) -> UserNameID:
    """
    Gets a user's `names_id` from Oracle HCM.

    Args:
        email: The logged in user's email address.

    Returns:
        The user's unique identifiers within Oracle HCM.
    """
    client = get_oracle_hcm_client()

    q_expr = f"emails.EmailAddress='{email}'"

    response = client.get_request(
        "workers", q_expr=q_expr, expand_expr="names", headers={"REST-Framework-Version": "4"}
    )
    if len(response["items"]) == 0:
        return UserNameID(names_id=None)
    result = response["items"][0]
    names_id_href = (
        get_id_from_links(
            result.get("names", {}).get("items", [])[0].get("links", [])[0].get("href")
        )
        if result.get("names", {}).get("items", [])
        else None
    )
    return UserNameID(
        names_id=names_id_href,
    )
