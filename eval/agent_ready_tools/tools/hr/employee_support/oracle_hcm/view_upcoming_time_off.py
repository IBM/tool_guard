from datetime import date
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleUpcomingTimeOff:
    """Represents an upcoming time off entry in Oracle HCM."""

    employer: str
    absence_type: str
    start_date: str
    end_date: str
    duration: str
    absence_status: str
    approval_status: str


@dataclass
class OracleUpcomingTimeOffResponse:
    """Represents the response from getting a user's upcoming time off in Oracle HCM."""

    upcoming_absences: List[OracleUpcomingTimeOff]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def view_upcoming_time_off(
    person_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
) -> OracleUpcomingTimeOffResponse:
    """
    Gets a user's upcoming time off entries from Oracle HCM.

    Args:
        person_id: The person_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        start_date: The start of the date range in ISO 8601 format (e.g., YYYY-MM-DD). Defaults to
            today's date if not provided.
        end_date: The end of the date range in ISO 8601 format (e.g., YYYY-MM-DD).
        limit: The maximum number of records to return. Default is 50.
        offset: The starting point in the record set. Default is 0.

    Returns:
        A worker's upcoming time off entries.
    """
    client = get_oracle_hcm_client()

    if not start_date:
        start_date = date.today().isoformat()  # Default to current date

    finder_expr = f"findByPersonAbsenceTypeIdAndAbsDate;personId={person_id},startDate={start_date}"

    if end_date:
        finder_expr += f",endDate={end_date}"

    params = {"limit": limit, "offset": offset}

    response = client.get_request("absences", finder_expr=finder_expr, params=params)

    upcoming_absences: List[OracleUpcomingTimeOff] = []

    for item in response.get("items", []):
        upcoming_absences.append(
            OracleUpcomingTimeOff(
                employer=item.get("employer", ""),
                absence_type=item.get("absenceType", ""),
                start_date=item.get("startDate", ""),
                end_date=item.get("endDate", ""),
                duration=item.get("formattedDuration", ""),
                absence_status=item.get("absenceDispStatusMeaning", ""),
                approval_status=item.get("approvalStatusCd", ""),
            )
        )

    return OracleUpcomingTimeOffResponse(upcoming_absences=upcoming_absences)
