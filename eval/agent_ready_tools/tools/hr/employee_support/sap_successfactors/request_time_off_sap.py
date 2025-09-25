from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class SFRequestTimeOffResponse:
    """Represents the response from creating a time off request in SAP SuccessFactors."""

    request_id: str


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def request_time_off_sap(
    user_id: str,
    time_type: str,
    start_date: str,
    end_date: str,
) -> SFRequestTimeOffResponse:
    """
    Creates a time off request for the user in SuccessFactors.

    Args:
        user_id: The user's user_id uniquely identifying them within the SuccessFactors API.
        time_type: The time type for the request, as specified by the `get_time_types` tool.
        start_date: The start date for the time off request in ISO 8601 format (e.g., YYYY-MM-DD).
        end_date: The end date for the time off request in ISO 8601 format (e.g., YYYY-MM-DD).

    Returns:
        The result from submitting the time off request.
    """
    client = get_sap_successfactors_client()

    payload = {
        "__metadata": {"uri": "EmployeeTime", "type": "SFOData.EmployeeTime"},
        "startDate": iso_8601_to_sap_date(start_date),
        "endDate": iso_8601_to_sap_date(end_date),
        "userIdNav": {"__metadata": {"uri": f"User('{user_id}')", "type": "SFOData.User"}},
        "timeTypeNav": {
            "__metadata": {"uri": f"TimeType('{time_type}')", "type": "SFOData.TimeType"}
        },
    }
    try:
        response = client.upsert_request(payload=payload)

        status_code = response.get("d", {})[0].get("httpCode", "")
        if status_code == 200:
            key_value = response.get("d", {})[0].get("key", "")
        else:
            key_value = response.get("d", {})[0].get("message", "")

    except AttributeError as e:
        raise ValueError(f"unexpected Output:", e)

    return SFRequestTimeOffResponse(request_id=key_value)
