from enum import StrEnum

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UserAccessType(StrEnum):
    """Represents the user access type of learning community in Oracle HCM."""

    MEMBER = "ORA_CMNTY_REGULAR_MEMBER"
    COMMUNITY_MANAGER = "ORA_CMNTY_MANAGER"
    REQUIRED_MEMBER = "ORA_CMNTY_REQUIRED_MEMBER"


@dataclass
class AssignLearningCommunityResponse:
    """Represents the results of assigning learning community to worker in Oracle HCM."""

    http_code: int


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def assign_learning_community(
    learning_community_id: str, person_id: str, user_access_type: str
) -> AssignLearningCommunityResponse:
    """
    Assign a worker to a learning community in Oracle HCM.

    Args:
        learning_community_id: The unique identifier of the learning community returned by the
            view_learnings_communities tool.
        person_id: The person id of the worker returned by the get_user_oracle_ids tool.
        user_access_type: The user access type for the learning community. Accepted values are
            MEMBER, COMMUNITY_MANAGER, REQUIRED_MEMBER.

    Returns:
        The result from performing the assign learning community to a worker.
    """

    client = get_oracle_hcm_client()

    user_access_types = [user_access_type.name for user_access_type in UserAccessType]
    if user_access_type and user_access_type.upper() not in user_access_types:
        raise ValueError(
            f"User access type '{user_access_type}' is not a valid value. Accepted values are {user_access_types}"
        )

    payload = {
        "userAccessPersonId": person_id,
        "userAccessType": UserAccessType[user_access_type.upper()].value,
    }

    response = client.post_request(
        entity=f"/learningCommunities/{learning_community_id}/child/userAccess", payload=payload
    )

    return AssignLearningCommunityResponse(http_code=response.get("status_code", ""))
