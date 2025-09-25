from datetime import datetime, timezone
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UpdateLocationResult:
    """Represents the result of a location update operation in SAP SuccessFactors."""

    http_code: int
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def update_location(user_id: str, location_id: str, start_date: str) -> UpdateLocationResult:
    """
    Updates a user's location in SAP SuccessFactors.

    Args:
        user_id: The user's unique identifier within the SuccessFactors API.
        location_id: The location ID of the new location, as specified by the `get_location_id` tool.
        start_date: The start date for the location change in ISO 8601 format (YYYY-MM-DD).

    Returns:
        The result from updating the user's location.
    """
    client = get_sap_successfactors_client()

    dt = datetime.strptime(start_date, "%Y-%m-%d")
    dt = dt.replace(tzinfo=timezone.utc)
    start_date_uri = dt.strftime("%Y-%m-%dT%H:%M:%S")

    payload = {
        "__metadata": {
            "uri": f"EmpJob(seqNumber=1L,startDate=datetime'{start_date_uri}',userId='{user_id}')",
            "type": "SFOData.EmpJob",
        },
        "location": location_id,
    }

    response = client.upsert_request(payload=payload)

    return UpdateLocationResult(
        http_code=response["d"][0]["httpCode"], message=response["d"][0]["message"]
    )
