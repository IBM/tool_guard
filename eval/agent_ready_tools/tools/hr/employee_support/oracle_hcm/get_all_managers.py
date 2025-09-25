from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class Manager:
    """Represents manager's assignment number in Oracle HCM."""

    manager_assignment_number: str
    manager_display_name: str
    manager_email_address: str


@dataclass
class ManagerResponse:
    """Represents the response from getting a manager's assignment number in Oracle HCM."""

    managers: List[Manager]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_all_managers(
    person_number: Optional[str] = None, email_address: Optional[str] = None
) -> ManagerResponse:
    """
    Gets manager's assignment number in Oracle HCM.

    Args:
        person_number: The person_number uniquely identifying manager within the Oracle HCM.
        email_address: The email_address of the new manager in Oracle HCM.

    Returns:
        The manager's assignment number.
    """
    client = get_oracle_hcm_client()

    q_expr = None

    if email_address:
        q_expr = f"EmailAddress={email_address}"
    elif person_number:
        q_expr = f"PersonNumber={person_number}"

    response = client.get_request(
        "talentReviewManagersLOV",
        q_expr=q_expr,
    )

    managers: list[Manager] = []
    for result in response["items"]:
        managers.append(
            Manager(
                manager_assignment_number=result.get("AssignmentNumber", ""),
                manager_display_name=result.get("DisplayName", ""),
                manager_email_address=result.get("EmailAddress", ""),
            )
        )
    return ManagerResponse(managers=managers)
