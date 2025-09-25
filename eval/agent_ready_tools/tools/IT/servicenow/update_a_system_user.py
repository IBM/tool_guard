from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class UpdateASystemUserResponse:
    """Represents the response of updating a system user in ServiceNow."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def update_a_system_user(
    user_name_system_id: str,
    user_password: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    gender: Optional[str] = None,
    title: Optional[str] = None,
    mobile_phone: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    middle_name: Optional[str] = None,
    time_zone: Optional[str] = None,
    manager_username_system_id: Optional[str] = None,
    department_system_id: Optional[str] = None,
    country: Optional[str] = None,
) -> UpdateASystemUserResponse:
    """
    Updates a system user in ServiceNow.

    Args:
        user_name_system_id: The system_id of the user name returned by the `get_system_users` tool.
        user_password: The password of the system user.
        email: The email address of the system user.
        phone: The business phone number of the system user.
        gender: The gender of the system user, returned by the tool `get_genders`.
        title: The job title of the system user (e.g., Director, Chief Financial Officer).
        mobile_phone: The mobile phone number of the system user.
        first_name: The first name of the system user.
        last_name: The last name of the system user.
        middle_name: The middle name of the system user.
        time_zone: The time zone of the system user, returned by the tool `get_time_zones`.
        manager_username_system_id: The system_id of the manager username, returned by the tool
            `get_system_users`.
        department_system_id: The system_id of system user's department, returned by the tool
            `get_departments`.
        country: The value of system user's country, returned by the tool `get_countries`.

    Returns:
        Confirmation of the system user update.
    """

    client = get_servicenow_client()
    payload = {
        "email": email,
        "user_password": user_password,
        "phone": phone,
        "gender": gender,
        "title": title,
        "mobile_phone": mobile_phone,
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "time_zone": time_zone,
        "manager": manager_username_system_id,
        "department": department_system_id,
        "country": country,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.patch_request(
        entity="sys_user",
        entity_id=user_name_system_id,
        payload=payload,
    )

    return UpdateASystemUserResponse(http_code=response["status_code"])
