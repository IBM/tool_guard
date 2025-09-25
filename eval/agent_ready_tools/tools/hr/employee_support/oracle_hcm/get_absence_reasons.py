from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class AbsenceReason:
    """Represents a reason associated with an absence type in Oracle HCM."""

    reason: str


@dataclass
class AbsenceReasonResponse:
    """Response containing all absence reasons for a given absence type."""

    absence_reasons: List[AbsenceReason]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_absence_reasons(absence_type_id: str) -> AbsenceReasonResponse:
    """
    Gets a list of absence reasons associated with a specific absence type in Oracle HCM.

    Only some absence types support reasons. If none exist, the returned list will be empty.

    Args:
        absence_type_id: The ID of the absence type, returned by the `get_absence_types` tool.

    Returns:
        A list of absence reasons related to the absence type.
    """
    client = get_oracle_hcm_client()
    response = client.get_request(
        "absenceTypeReasonsLOV",
        q_expr=f"AbsenceTypeId={absence_type_id}",
    )

    absence_reasons: List[AbsenceReason] = [
        AbsenceReason(
            reason=item.get("Name", ""),
        )
        for item in response.get("items", [])
    ]

    return AbsenceReasonResponse(absence_reasons=absence_reasons)
