from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class AbsenceType:
    """Represents an absence type in Oracle HCM."""

    absence_type_id: int
    employer_id: int
    absence_type_name: str
    description: Optional[str] = None
    unit_of_measure: Optional[str] = None


@dataclass
class AbsenceTypeResponse:
    """Represents the response from getting a user's absence types in Oracle HCM."""

    absence_types: List[AbsenceType]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_absence_types(person_id: str) -> AbsenceTypeResponse:
    """
    Gets a user's absence types in Oracle HCM.

    Args:
        person_id: The person_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.

    Returns:
        The user's absence types.
    """
    client = get_oracle_hcm_client()
    response = client.get_request(
        "absenceTypesLOV",
        finder_expr=f"findByWord;PersonId={person_id}",
    )

    absence_types: List[AbsenceType] = []
    for item in response.get("items", []):
        absence_types.append(
            AbsenceType(
                absence_type_id=item.get("AbsenceTypeId", ""),
                employer_id=item.get("EmployerId", ""),
                absence_type_name=item.get("AbsenceTypeName", ""),
                description=item.get("Description") or "",
                unit_of_measure=item.get("DurationUOMCodeMeaning", ""),
            )
        )

    return AbsenceTypeResponse(absence_types=absence_types)
