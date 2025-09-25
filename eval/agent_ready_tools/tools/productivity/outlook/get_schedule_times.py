from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class ScheduleTime:
    """Represents the result of time window schedules for a given user."""

    statuses: List[str]
    start_date_time: List[str]
    end_date_time: List[str]


@dataclass
class ScheduleTimeResponse:
    """Represents the result of time window schedules for a given user."""

    schedule_times: List[ScheduleTime]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_schedule_times(
    email_address: str,
    start_date_time: str,
    time_zone: str,
    end_date_time: str,
) -> ScheduleTimeResponse:
    """
    Gets the schedule time of the user in Microsoft Outlook.

    Args:
        email_address: The email address of the user whose schedule is being retrieved.
        start_date_time: The start date and time for the period to retrieve the schedule, in ISO
            8601 format.
        time_zone: The time zone in which the schedule times are specified returned by
            `get_timezones` tool.
        end_date_time: The end date and time for the period to retrieve the schedule, in ISO 8601
            format.

    Returns:
        The schedule time of the user
    """
    client = get_microsoft_client()

    payload = {
        "schedules": [email_address],
        "startTime": {"dateTime": start_date_time, "timeZone": time_zone},
        "endTime": {"dateTime": end_date_time, "timeZone": time_zone},
    }

    headers = {"Prefer": f'outlook.timezone ="{time_zone}"'}

    response = client.post_request(
        endpoint=f"{client.get_user_resource_path()}/calendar/getSchedule",
        data=payload,
        headers=headers,
    )

    value = response.get("value", [])
    status = [
        status.get("status", "") for schedule in value for status in schedule.get("scheduleItems")
    ]
    start_date_time_list = [
        start_time.get("start", {}).get("dateTime", "")
        for schedule in value
        for start_time in schedule.get("scheduleItems", [])
    ]
    end_date_time_list = [
        end_time.get("end", {}).get("dateTime", "")
        for schedule in value
        for end_time in schedule.get("scheduleItems", [])
    ]

    # Check if the status is present in the value
    schedule_times_list = []
    if status:
        schedule_times_list = [
            ScheduleTime(
                statuses=status,
                start_date_time=start_date_time_list,
                end_date_time=end_date_time_list,
            )
        ]
    else:
        schedule_times_list = [
            ScheduleTime(
                statuses=[],
                start_date_time=[],
                end_date_time=[],
            )
        ]
    return ScheduleTimeResponse(schedule_times=schedule_times_list)
