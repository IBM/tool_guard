from datetime import datetime
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class HolidayCalendar:
    """Represents a holiday calendar by country in SAP SuccessFactors."""

    date: str
    holiday: str


@dataclass
class SFHolidayCalendarResponse:
    """A list of holiday calendar configured for a country in SAP SuccessFactors."""

    holiday_list: List[HolidayCalendar]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_holiday_calendar_sap(
    country: str,
    date_range_start: Optional[str] = None,
    date_range_end: Optional[str] = None,
) -> SFHolidayCalendarResponse:
    """
    Gets a holiday calendar of a country in SAP SuccessFactors. If a date range start and end is
    provided, the SAP api results will be filtered accordingly. If a date range start and end is not
    provided, this method will only return the calendar for the current year.

    Args:
        country: The 3-letter ISO code of the country.
        date_range_start: Date range start to filter results in YYYY-MM-DD format
        date_range_end: Date range end to filter results in YYYY-MM-DD format

    Returns:
        The holiday calendar of the country.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(
        entity="HolidayCalendar",
        filter_expr=f"country eq '{country}'",
        expand_expr="holidayAssignments",
    )

    holiday_list: List[HolidayCalendar] = []
    for result in response["d"]["results"]:
        if date_range_start is None:
            date_range_start = datetime.today().date().replace(month=1, day=1).isoformat()

        if date_range_end is None:
            date_range_end = datetime.today().date().replace(month=12, day=31).isoformat()

        items = result["holidayAssignments"]["results"]
        for item in items:
            item_iso_date = sap_date_to_iso_8601(item.get("date", ""))

            if date_range_start <= item_iso_date <= date_range_end:
                holiday_list.append(
                    HolidayCalendar(date=(item_iso_date), holiday=item.get("holiday"))
                )
    return SFHolidayCalendarResponse(holiday_list=holiday_list)
