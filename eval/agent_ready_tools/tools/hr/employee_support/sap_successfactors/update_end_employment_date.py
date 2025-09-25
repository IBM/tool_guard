from datetime import datetime, timezone
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UpdateEndEmploymentDateResults:
    """Represents the result of updating a user's end employment date in SAP SuccessFactors."""

    http_code: int
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def update_end_employment_date(
    person_id_external: str, user_id: str, end_date: str, event_reason: str
) -> UpdateEndEmploymentDateResults:
    """
    Updates a user's end employment date in SAP SuccessFactors.

    Args:
        person_id_external: The user's person_id_external uniquely identifying them within the
            SuccessFactors API, returned by the tool `get_all_terminated_employees` and associated
            with the logged-in HR.
        user_id: The user's user_id uniquely identifying them within the SuccessFactors API,
            returned by the tool `get_all_terminated_employees` and associated with the logged-in
            HR.
        end_date: The end date to update, indicating when an employee’s job officially ends, in ISO
            8601 format (e.g., YYYY-MM-DD).
        event_reason: The reason for employment termination (FOEventReason type).

    Returns:
        The result from performing the update to the user's termination.
    """
    client = get_sap_successfactors_client()

    dt = datetime.strptime(end_date, "%Y-%m-%d")
    dt.replace(tzinfo=timezone.utc)
    end_date_milliseconds = int(dt.timestamp() * 1000)

    payload = {
        "__metadata": {
            "uri": "EmpEmploymentTermination",
            "type": "SFOData.EmpEmploymentTermination",
        },
        "personIdExternal": person_id_external,
        "userId": user_id,
        "endDate": f"/Date({end_date_milliseconds})/",
        "eventReason": event_reason,
    }
    response = client.upsert_request(payload=payload)
    return UpdateEndEmploymentDateResults(
        http_code=response["d"][0]["httpCode"], message=response["d"][0]["message"]
    )
