from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UserSuccessFactorsIDs:
    """Represents the response from getting a user's unique identifiers from SuccessFactors."""

    person_id_external: Optional[str] = None
    user_id: Optional[str] = None
    username: Optional[str] = None
    name: Optional[str] = None
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_user_successfactors_ids(email: str) -> UserSuccessFactorsIDs:
    """
    Gets a user's `person_id_external` and `user_id` from SuccessFactors.

    Args:
        email: The user's email address.

    Returns:
        The user's unique identifiers within SuccessFactors or a message indicating the user does not exist.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(
        "User",
        filter_expr=f"tolower(email) eq '{email.lower()}'",
        select_expr="userId,username,displayName",
    )
    results = response["d"]["results"]

    if len(results) == 0:
        return UserSuccessFactorsIDs(message="The given user does not exist.")

    user_id = response["d"]["results"][0]["userId"]
    username = response["d"]["results"][0]["username"]
    name = response["d"]["results"][0]["displayName"]
    response = client.get_request(
        "EmpEmployment", filter_expr=f"userId eq '{user_id}'", select_expr="personIdExternal"
    )
    return UserSuccessFactorsIDs(
        person_id_external=response["d"]["results"][0]["personIdExternal"],
        user_id=user_id,
        username=username,
        name=name,
    )
