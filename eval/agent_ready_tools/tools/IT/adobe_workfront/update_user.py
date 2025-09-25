from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class UpdateUserResponse:
    """Represents the response for updating a user in Adobe Workfront."""

    user_id: str
    title: Optional[str]
    my_info: Optional[str]


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=ADOBE_WORKFRONT_CONNECTIONS,
)
def adobe_update_user(
    user_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    title: Optional[str] = None,
    my_info: Optional[str] = None,
    phone_number: Optional[str] = None,
    work_hours_per_day: Optional[int] = None,
    address: Optional[str] = None,
    postal_code: Optional[str] = None,
    city_name: Optional[str] = None,
    state_name: Optional[str] = None,
    country_name: Optional[int] = None,
) -> UpdateUserResponse:
    """
    Updates a user in Adobe Workfront.

    Args:
        user_id: The id of the user in Adobe Workfront returned by the tool `list_users`.
        first_name: The first name of the user in Adobe Workfront.
        last_name: The last name of the user in Adobe Workfront.
        title: The title of the user in Adobe Workfront.
        my_info: The information of the user in Adobe Workfront.
        phone_number: The phone number of the user in Adobe Workfront.
        work_hours_per_day: The number of hours the user works in a day in Adobe Workfront.
        address: The address of the user in Adobe Workfront.
        postal_code: The postal_code of the user in Adobe Workfront.
        city_name: The city name of the user in Adobe Workfront.
        state_name: The state name of the user in Adobe Workfront.
        country_name: The country name of the user in Adobe Workfront.

    Returns:
        The result of performing an update operation on a user.
    """

    client = get_adobe_workfront_client()

    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "title": title,
        "myInfo": my_info,
        "phoneNumber": phone_number,
        "workHoursPerDay": work_hours_per_day,
        "address": address,
        "postalCode": postal_code,
        "city": city_name,
        "state": state_name,
        "country": country_name,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.put_request(entity=f"user/{user_id}", payload=payload)

    data = response.get("data", {})

    return UpdateUserResponse(
        user_id=data.get("ID", ""),
        title=data.get("title", ""),
        my_info=data.get("myInfo", ""),
    )
