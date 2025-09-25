from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.date_conversion import iso_8601_datetime_convert_to_date
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class LearningDetails:
    """Represents learning details of a worker in Oracle HCM."""

    learning_name: str
    learning_status: str
    assigned_by: str
    assigned_date: str
    learning_record_id: str
    assigner: Optional[str] = None
    withdrawn_date: Optional[str] = None
    completion_date: Optional[str] = None


@dataclass
class ViewLearningResponse:
    """Represents the response from getting a worker's learnings in Oracle HCM."""

    learnings: List[LearningDetails]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def view_learnings(
    person_id: int,
    learning_status_code: Optional[str] = None,
    learning_title: Optional[str] = None,
    limit: Optional[int] = 50,
) -> ViewLearningResponse:
    """
    Gets a worker's learnings in Oracle HCM.

    Args:
        person_id: The person_id uniquely identifies them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        learning_status_code: The status code of the learning in Oracle HCM returned by the
            `get_learning_statuses` tool.
        learning_title: The title of the learning in Oracle HCM.
        limit: The maximum number of learnings to retrieve in a single API call. Defaults to 50. Use
            this to control the size of the result set.

    Returns:
        The learnings of a worker.
    """
    client = get_oracle_hcm_client()
    q_expr = f"assignedToId={person_id}"

    if learning_status_code:
        q_expr += f" and assignmentSubStatus='{learning_status_code}'"
    elif learning_title:
        q_expr += f" and learningItemTitle='{learning_title}'"

    params = {"limit": limit}
    response = client.get_request(
        "learnerLearningRecords",
        q_expr=q_expr,
        params=params,
        headers={"REST-Framework-Version": "4"},
    )

    learnings: list[LearningDetails] = []

    for result in response["items"]:
        learnings.append(
            LearningDetails(
                learning_name=result.get("learningItemTitle", ""),
                learning_status=result.get("assignmentSubStatusMeaning", ""),
                assigned_by=result.get("assignerDisplayName", ""),
                assigned_date=iso_8601_datetime_convert_to_date(result.get("assignedDate", "")),
                withdrawn_date=(
                    iso_8601_datetime_convert_to_date(result.get("withdrawnDate", ""))
                    if result.get("withdrawnDate", "")
                    else ""
                ),
                completion_date=(
                    iso_8601_datetime_convert_to_date(result.get("completedDate", ""))
                    if result.get("completedDate", "")
                    else ""
                ),
                assigner=(
                    "Self-enrolled"
                    if result.get("assignerId", 0) == person_id
                    else "Assigned by a manager"
                ),
                learning_record_id=get_id_from_links(result.get("links", [{}])[0].get("href")),
            )
        )
    return ViewLearningResponse(learnings=learnings)
