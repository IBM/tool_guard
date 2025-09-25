from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class WithdrawLearningResponse:
    """Represents the learning withdrawal result in Oracle HCM."""

    learning_status: str
    assignment_record_id: int


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def withdraw_learning(
    learning_record_id: str, comment: Optional[str] = None
) -> WithdrawLearningResponse:
    """
    Withdraw from a learning enrollment in Oracle HCM.

    Args:
        learning_record_id: The learning_record_id of learning returned by `view_learnings` tool.
        comment: A comment from the user

    Returns:
        The result from learning enrollment.
    """

    client = get_oracle_hcm_client()

    payload = {"assignmentStatus": "ORA_ASSN_REC_WITHDRAWN"}

    if comment is not None:
        payload["statusChangeComment"] = comment

    result = client.update_request(
        payload=payload,
        entity=f"learnerLearningRecords/{learning_record_id}",
    )

    return WithdrawLearningResponse(
        learning_status=result.get("assignmentStatus", ""),
        assignment_record_id=result.get("assignmentRecordId", ""),
    )
