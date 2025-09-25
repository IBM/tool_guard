from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleGetBusinessTitleResponse:
    """Represents the response from getting a user's business title in Oracle HCM."""

    assignment_id: str
    business_title: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_business_title_oracle(
    worker_id: str,
    service_id: str,
    assignment_id: Optional[str],
) -> OracleGetBusinessTitleResponse:
    """
    Gets user's business title in Oracle HCM.

    Args:
        worker_id: The worker_id is the internal unique identifier hash string for a person in HCM
            returned by the `get_user_oracle_ids` tool.
        service_id: The service_id is an id number that refers to a person's Work
            Relationship/Arrangement.
        assignment_id: The assignment_id number is an optional unique identifier for a specific assignment or job position.
            It is not used for the API call, but instead to filter reults from the API call since each assignment id has a different business title.

    Returns:
        The worker's business title info.
    """
    client = get_oracle_hcm_client()

    business_title_found = ""
    business_title_list = []
    assignment_id_found = ""

    # Assignment id is optional because it is not needed for the API call
    result = client.get_request(
        entity=f"workers/{worker_id}/child/workRelationships/{service_id}/child/assignments"
    )

    all_assignments = result.get("items", [])

    for this_assignment in all_assignments:
        business_title_list.append(this_assignment.get("AssignmentName", ""))

        # If we have an asssignment id number, we use it to return whatever assignment the user asked for
        if assignment_id:
            this_assignment_id = this_assignment.get("AssignmentId")

            if this_assignment_id == assignment_id:
                assignment_id_found = this_assignment_id
                business_title_found = this_assignment.get("AssignmentName", "")
                break

        # When no assignment id number is passed in, we return the user's primary assignment
        else:
            is_primary_assignment = this_assignment.get("PrimaryAssignmentFlag", False)

            if is_primary_assignment:
                assignment_id_found = this_assignment.get("AssignmentId")
                business_title_found = this_assignment.get("AssignmentName", "")
                break

    return OracleGetBusinessTitleResponse(
        assignment_id=assignment_id_found,
        business_title=business_title_found,
    )
