from unittest.mock import MagicMock, patch

from xsdata.models.datatype import XmlDate

from agent_ready_tools.tools.hr.employee_support.workday.get_holiday_calendar import (
    _get_holiday_calendar_payload,
    get_holiday_calendar,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_holiday_calendar() -> None:
    """Test that the `get_holiday_calendar` function returns the expected response."""

    # Define test data:
    test_data = {
        "country_code": "USA",
        "year": "2020",
        "calendar_name": "Holidays for the United States of America",
        "holiday_name": "New Year's Day",
        "start_date": "2020-01-01",
        "end_date": "2020-01-01",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_holiday_calendar.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_holiday_calendar.return_value = Obj(
            {
                "body": {
                    "get_holiday_calendars_response": {
                        "response_results": {
                            "page": 1,
                            "total_pages": 1,
                        },
                        "response_data": {
                            "holiday_calendar": [
                                Obj(
                                    {
                                        "holiday_calendar_reference": {
                                            "id": [
                                                Obj(
                                                    {
                                                        "type_value": "Holiday_Calendar_ID",
                                                        "value": test_data["country_code"],
                                                    }
                                                )
                                            ]
                                        },
                                        "holiday_calendar_data": {
                                            "name": test_data["calendar_name"],
                                            "holiday_calendar_event_data": [
                                                Obj(
                                                    {
                                                        "name": test_data["holiday_name"],
                                                        "start_end_data": {
                                                            "start_date": XmlDate(2020, 1, 1),
                                                            "end_date": XmlDate(2020, 1, 1),
                                                        },
                                                    }
                                                )
                                            ],
                                        },
                                    }
                                )
                            ],
                        },
                    },
                },
            }
        )

        # Get Holiday Calendar
        response = get_holiday_calendar(
            country_code=test_data["country_code"], year=test_data["year"]
        )

        # Ensure that get_holiday_calendar() executed and returned proper values
        assert response
        assert response.calendar_name == test_data["calendar_name"]
        assert len(response.holidays)
        assert response.holidays[0].name == test_data["holiday_name"]
        assert response.holidays[0].start_date == test_data["start_date"]
        assert response.holidays[0].end_date == test_data["end_date"]

        # Ensure the API call was made with expected parameters
        mock_client.get_holiday_calendar.assert_called_once_with(
            _get_holiday_calendar_payload(next_page=1)
        )
