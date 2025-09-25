from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class LearningCommunityDetails:
    """Represents learning community details of a worker in Oracle HCM."""

    learning_item_id: int
    learning_item_status: str
    learning_item_title: str
    learning_community_id: str


@dataclass
class ViewLearningCommunitiesResponse:
    """Represents the response from getting a worker's learning community in Oracle HCM."""

    communities: List[LearningCommunityDetails]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def view_learnings_communities(
    person_id: Optional[str] = None,
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
) -> ViewLearningCommunitiesResponse:
    """
    Gets a worker's learnings in Oracle HCM.

    Args:
        person_id: The person_id uniquely identifies them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        limit: The maximum number of learnings to retrieve in a single API call. Defaults to 50. Use
            this to control the size of the result set.
        offset: The starting point to handle pagination.

    Returns:
        The learnings of a worker.
    """
    client = get_oracle_hcm_client()

    q_expr = None
    if person_id:
        q_expr = f"userAccess.userAccessPersonId={person_id}"

    params = {"limit": limit, "offset": offset}

    response = client.get_request(
        "learningCommunities", q_expr=q_expr, params=params, headers={"REST-Framework-Version": "4"}
    )

    communities: list[LearningCommunityDetails] = []

    for result in response["items"]:
        communities.append(
            LearningCommunityDetails(
                learning_item_id=result.get("learningItemId", ""),
                learning_item_status=result.get("learningItemStatus", ""),
                learning_item_title=result.get("learningItemTitle", ""),
                learning_community_id=get_id_from_links(result["links"][0]["href"]),
            )
        )
    return ViewLearningCommunitiesResponse(communities=communities)
