from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS

# As per Oracle HCM requirements, it is necessary to provide an action code for updates. Since we are updating the assignment name, we have defaulted the action code to ASG_CHANGE, with the corresponding action name being 'Assignment Change'.
ACTION_CODE = "ASG_CHANGE"


@dataclass
class OracleUpdateBusinessTitleResponse:
    """Represents the response from updating a user's business title in Oracle HCM."""

    assignment_id: str
    business_title: str
    action_code: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def update_business_title_oracle(
    worker_id: str,
    assignment_uniq_id: str,
    period_of_service_id: str,
    business_title: str,
) -> OracleUpdateBusinessTitleResponse:
    """
    Updates user's business title in Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        assignment_uniq_id: The assignment_uniq_id of the worker's assignment as returned by
            `get_assignment_details` tool.
        period_of_service_id: The period_of_service_id of the worker's assignment as returned by
            `get_assignment_details` tool.
        business_title: The new assignment name within the Oracle HCM

    Returns:
        The worker's updated info.
    """
    client = get_oracle_hcm_client()

    response = client.update_request(
        entity=f"workers/{worker_id}/child/workRelationships/{period_of_service_id}/child/assignments/{assignment_uniq_id}",
        payload={"AssignmentName": business_title, "ActionCode": ACTION_CODE},
    )

    return OracleUpdateBusinessTitleResponse(
        assignment_id=response.get("AssignmentId", ""),
        business_title=response.get("AssignmentName", ""),
        action_code=response.get("ActionCode", ""),
    )
