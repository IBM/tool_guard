from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.tools.hr.employee_support.sap_successfactors.sap_utility import user_exists
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class SFDirectReport:
    """Represents a single direct report of a user in SAP SuccessFactors."""

    user_id: str
    name: str
    email: Optional[str] = None
    home_phone: Optional[str] = None
    title: Optional[str] = None
    division: Optional[str] = None
    department: Optional[str] = None


@dataclass
class SFDirectReportsResponse:
    """Represents all direct reports of a user in SAP SuccessFactors."""

    direct_reports: List[SFDirectReport]
    error_message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_direct_reports_sap(user_id: str) -> SFDirectReportsResponse:
    """
    Gets a user's direct reports in SAP SuccessFactors.

    Args:
        user_id: The user's user_id uniquely identifying them within the SuccessFactors API.

    Returns:
        The user's direct reports.
    """

    if not user_exists(user_id):
        return SFDirectReportsResponse(direct_reports=[], error_message="User does not exist.")
    client = get_sap_successfactors_client()

    response = client.get_request(entity="User", filter_expr=f"manager/userId eq '{user_id}'")
    results = response.get("d", {}).get("results", [])

    direct_reports_list = [
        SFDirectReport(
            user_id=record.get("userId"),
            name=record.get("displayName"),
            email=record.get("email"),
            home_phone=record.get("homePhone", None),
            title=record.get("title"),
            division=record.get("division"),
            department=record.get("department"),
        )
        for record in results
    ]
    return SFDirectReportsResponse(direct_reports=direct_reports_list)
