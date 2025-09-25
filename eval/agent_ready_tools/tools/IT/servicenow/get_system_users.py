from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class SystemUsers:
    """Represents a single system user object in ServiceNow."""

    is_active: str
    system_id: str
    name: str
    user_name: str
    country: Optional[str]
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    mobile_phone: Optional[str] = None
    cost_center: Optional[str] = None
    manager: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None


@dataclass
class SystemUsersResponse:
    """A list of system users details in the ServiceNow."""

    system_users: list[SystemUsers]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_system_users(
    is_active: Optional[str] = None,
    title: Optional[str] = None,
    name: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    user_name: Optional[str] = None,
    email: Optional[str] = None,
    country: Optional[str] = None,
    phone: Optional[str] = None,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> SystemUsersResponse:
    """
    Retrieves a list of system users details in the ServiceNow.

    Args:
        is_active: The status of the system user.
        title: The title of the system user.
        name: The name of the system user.
        first_name: The first name of the system user.
        last_name: The last name of the system user.
        user_name: The user name of the system user.
        email: The email of the system user.
        country: The country code of the user.
        phone: The business phone number of the user.
        limit: The maximum number of system users to retrieve in a single API call. Defaults to 10.
            Use this to control the size of the result set.
        skip: The number of system users to skip for pagination

    Returns:
        A list of system users.
    """

    client = get_servicenow_client()
    params = {
        "active": is_active,
        "title": title,
        "name": name,
        "first_name": first_name,
        "last_name": last_name,
        "user_name": user_name,
        "email": email,
        "country": country,
        "phone": phone,
        "sysparm_limit": limit,
        "sysparm_offset": skip,
        "sysparm_display_value": True,
    }

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(entity="sys_user", params=params)

    system_users: List[SystemUsers] = [
        SystemUsers(
            is_active=user.get("active", ""),
            system_id=user.get("sys_id", ""),
            title=user.get("title", ""),
            name=user.get("name", ""),
            first_name=user.get("first_name", ""),
            last_name=user.get("last_name", ""),
            middle_name=user.get("middle_name", ""),
            user_name=user.get("user_name", ""),
            email=user.get("email", ""),
            phone=user.get("phone", ""),
            mobile_phone=user.get("mobile_phone", ""),
            gender=user.get("gender", ""),
            cost_center=(
                user.get("cost_center", {}).get("display_value", "")
                if isinstance(user.get("cost_center", ""), dict)
                else user.get("cost_center", "")
            ),
            country=user.get("country"),
            manager=(
                user.get("manager", {}).get("display_value")
                if isinstance(user.get("manager", ""), dict)
                else user.get("manager", "")
            ),
            company=(
                user.get("company", {}).get("display_value")
                if isinstance(user.get("company", ""), dict)
                else user.get("company", "")
            ),
            department=(
                user.get("department", {}).get("display_value")
                if isinstance(user.get("department", ""), dict)
                else user.get("department", "")
            ),
        )
        for user in response["result"]
    ]

    return SystemUsersResponse(system_users=system_users)
