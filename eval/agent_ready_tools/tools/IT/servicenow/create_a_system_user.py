from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class CreateSystemUserResult:
    """Represents the result of create a system user in ServiceNow."""

    system_id: str
    user_name: str
    email: str
    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def create_a_system_user(
    user_name: str,
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    gender: Optional[str] = None,
    mobile_phone: Optional[str] = None,
    phone: Optional[str] = None,
    title: Optional[str] = None,
    company_system_id: Optional[str] = None,
    department_system_id: Optional[str] = None,
    time_zone: Optional[str] = None,
    user_password: Optional[str] = None,
) -> CreateSystemUserResult:
    """
    Creates a system user in ServiceNow.

    Args:
        user_name: The user name of the system user.
        email: The email of the system user.
        first_name: The first name of the system user.
        last_name: The last name of the system user.
        gender: The gender of the system user returned from `get_genders` tool.
        mobile_phone: The mobile phone of the system user.
        phone: The phone of the system user.
        title: The title of the system user.
        company_system_id: The system_id of system user's company, returned by the tool
            `get_companies` tool.
        department_system_id: The system_id of system user's department, returned by the tool
            `get_departments` tool.
        time_zone: The time zone of the system user returned from `get_time_zones` tool.
        user_password: The password of the system user.

    Returns:
        The result of creating the system user.
    """
    client = get_servicenow_client()

    payload: dict[str, Any] = {
        "user_name": user_name,
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "email": email,
        "mobile_phone": mobile_phone,
        "phone": phone,
        "title": title,
        "company": company_system_id,
        "department": department_system_id,
        "time_zone": time_zone,
        "user_password": user_password,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="sys_user", payload=payload)

    result = response.get("result", None)
    return CreateSystemUserResult(
        system_id=result.get("sys_id", ""),
        user_name=result and result.get("user_name", ""),
        email=result and result.get("email", ""),
        http_code=response.get("status_code", ""),
    )
