from decimal import Decimal
import typing
from typing import List, Optional, Tuple

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from xsdata.models.datatype import XmlDate

from agent_ready_tools.apis.workday_soap_services.hr import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class Holiday:
    """Represents a Holiday in Workday."""

    name: str
    start_date: str
    end_date: str


@dataclass
class WorkdayHolidayCalendarResponse:
    """Represents the response from getting a country's holiday calendar for a given year in
    Workday."""

    calendar_name: str
    holidays: List[Holiday]
    total: int


def _get_holiday_calendar_payload(
    next_page: int,
) -> api.GetHolidayCalendarsInput:
    """
    Returns a payload object of type GetHolidayCalendarsInput filled.

    Args:
        next_page: Calendar pagination - define page number.

    Returns:
        The GetHolidayCalendarsInput object.
    """
    return api.GetHolidayCalendarsInput(
        body=api.GetHolidayCalendarsInput.Body(
            get_holiday_calendars_request=api.GetHolidayCalendarsRequest(
                response_filter=api.ResponseFilterType(page=Decimal(next_page))
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_holiday_calendar(country_code: str, year: str) -> WorkdayHolidayCalendarResponse:
    """
    Gets a country's holiday calendar for a given year in Workday.

    Args:
        country_code: The ISO 3166-1 alpha-3 country code representing the country the holiday
            calendar pertains to.
        year: The year of the holiday calendar.

    Returns:
        The holiday calendar for the given year and country.
    """
    client = get_workday_soap_client()

    @typing.no_type_check
    def get_page_info_from_xml(output: api.GetHolidayCalendarsOutput) -> Tuple[int, int]:
        """
        Parses SOAP XML output and returns pagination info.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            current and total response pages.
        """
        try:
            response_results = output.body.get_holiday_calendars_response.response_results
            assert response_results and response_results.page and response_results.total_pages
        except (AttributeError, AssertionError) as e:
            raise ValueError(
                f"unable to get pagination info from GetHolidayCalendarsOutput: {e}\nraw output:\n{output}"
            )
        return int(response_results.page), int(response_results.total_pages)

    @typing.no_type_check
    def search_for_country_calendar(
        country_code: str, output: api.GetHolidayCalendarsOutput
    ) -> Optional[api.HolidayCalendarType]:
        """
        Parses SOAP XML output and searches for a calendar matching the given country code.

        Args:
            country_code: The ISO 3166-1 alpha-3 country code to search for.
            output: SOAP XML output from endpoint.

        Returns:
            Holiday calendar for country (if found).
        """
        found_calendar: Optional[api.HolidayCalendarType] = None
        try:
            calendars: List[api.HolidayCalendarType] = (
                output.body.get_holiday_calendars_response.response_data.holiday_calendar
            )
            for calendar in calendars:
                hids: List[api.HolidayCalendarObjectIdtype] = calendar.holiday_calendar_reference.id
                for hid in hids:
                    if hid.type_value == "Holiday_Calendar_ID":
                        if hid.value.startswith(country_code):
                            found_calendar = calendar
        except AttributeError as e:
            raise ValueError(
                f"unable to get calendar info from GetHolidayCalendarsOutput: {e}\nraw output:\n{output}"
            )

        return found_calendar

    @typing.no_type_check
    def get_holiday_info_from_calendar(
        year: str, calendar: api.HolidayCalendarType
    ) -> WorkdayHolidayCalendarResponse:
        """
        Parses Calendar object from SOAP XML output and extracts relevant holiday info.

        Args:
            year: The year for which to extract holidays from the calendar.
            calendar: SOAP XML calendar response object from endpoint.

        Returns:
            Holidays info from calendar.
        """
        calendar_name: str
        holidays: List[Holiday] = []
        try:
            calendar_name = calendar.holiday_calendar_data.name
            assert calendar_name
            holiday_events: List[api.HolidayCalendarEventDataType] = (
                calendar.holiday_calendar_data.holiday_calendar_event_data
            )
            for event in holiday_events:
                event_name: str = event.name
                event_start_date: XmlDate = event.start_end_data.start_date
                event_end_date: XmlDate = event.start_end_data.end_date
                assert event_name and event_start_date and event_end_date
                if year in (str(event_start_date.year), str(event_end_date.year)):
                    holidays.append(
                        Holiday(
                            name=event_name,
                            start_date=str(event_start_date),
                            end_date=str(event_end_date),
                        )
                    )
        except (AttributeError, AssertionError) as e:
            raise ValueError(
                f"unable to get holiday info from GetHolidayCalendarsOutput: {e}\ncalendar:\n{calendar}"
            )
        return WorkdayHolidayCalendarResponse(
            calendar_name=calendar_name, holidays=holidays, total=len(holidays)
        )

    # loop through paginated results until country's holiday calendar is found
    next_page: int = 1
    total_pages: int = 2
    while next_page < total_pages:
        payload = _get_holiday_calendar_payload(next_page=next_page)

        xml_response = client.get_holiday_calendar(payload)
        found_calendar = search_for_country_calendar(country_code=country_code, output=xml_response)
        if found_calendar:
            return get_holiday_info_from_calendar(year=year, calendar=found_calendar)

        current_page, total_pages = get_page_info_from_xml(xml_response)
        next_page = current_page + 1

    raise ValueError(f"Holiday Calendar not found for country_code {country_code}")
