from datetime import datetime
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_holiday_calendar_sap import (
    get_holiday_calendar_sap,
)


def test_get_holiday_calendar_sap_india_range() -> None:
    """Test that the `get_holiday_calendar_sap` function returns the expected response."""
    # Define test data:
    test_data = {
        "country": "IND",
        "nye_return_date": "2016-01-01",
        "date_range_start": "2014-01-01",
        "date_range_end": "2025-01-01",
        "holiday": "INDIA_NEWYEAR",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_holiday_calendar_sap.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "holidayAssignments": {
                            "results": [
                                {
                                    "date": test_data["nye_return_date"],
                                    "holiday": test_data["holiday"],
                                }
                            ]
                        }
                    }
                ]
            }
        }

        # Get country of employment
        response = get_holiday_calendar_sap(
            country=test_data["country"],
            date_range_start=test_data["date_range_start"],
            date_range_end=test_data["date_range_end"],
        )

        # Ensure that get_holiday_calendar_sap() executed and returned proper values
        assert response
        assert len(response.holiday_list)
        assert response.holiday_list[0].date == test_data["nye_return_date"]
        assert response.holiday_list[0].holiday == test_data["holiday"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="HolidayCalendar",
            filter_expr=f"country eq '{test_data['country']}'",
            expand_expr="holidayAssignments",
        )


def test_get_holiday_calendar_sap_india_current_year() -> None:
    """Test that the `get_holiday_calendar_sap` function returns the expected response."""
    # Define test data:
    test_data = {
        "country": "IND",
        "nye_return_date": "2016-01-01",
        "holiday": "INDIA_NEWYEAR",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_holiday_calendar_sap.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "holidayAssignments": {
                            "results": [
                                {
                                    "date": test_data["nye_return_date"],
                                    "holiday": test_data["holiday"],
                                }
                            ]
                        }
                    }
                ]
            }
        }

        # Get country of employment
        response = get_holiday_calendar_sap(
            country=test_data["country"],
        )

        # Ensure that get_holiday_calendar_sap() executed and returned proper values
        assert response
        assert len(response.holiday_list) == 0

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="HolidayCalendar",
            filter_expr=f"country eq '{test_data['country']}'",
            expand_expr="holidayAssignments",
        )


def test_get_holiday_calendar_sap_usa_current_year() -> None:
    """Test that the `get_holiday_calendar_sap` function returns the expected response."""
    # Define test data:
    test_data = {
        "country": "USA",
        "nye_return_date": datetime.today().date().replace(month=1, day=1).isoformat(),
        "holiday": "New Year's Day",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_holiday_calendar_sap.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "holidayAssignments": {
                            "results": [
                                {
                                    "date": test_data["nye_return_date"],
                                    "holiday": test_data["holiday"],
                                }
                            ]
                        }
                    }
                ]
            }
        }

        # Get country of employment
        response = get_holiday_calendar_sap(test_data["country"])

        # Ensure that get_holiday_calendar_sap() executed and returned proper values
        assert response
        assert len(response.holiday_list)
        assert response.holiday_list[0].date == test_data["nye_return_date"]
        assert response.holiday_list[0].holiday == test_data["holiday"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="HolidayCalendar",
            filter_expr=f"country eq '{test_data['country']}'",
            expand_expr="holidayAssignments",
        )


def test_get_holiday_calendar_sap_usa_date_range() -> None:
    """Test that the `get_holiday_calendar_sap` function returns the expected response."""
    # Define test data:
    test_data = {
        "country": "USA",
        "nye_return_date": "2015-01-01",
        "date_range_start": "2014-01-01",
        "date_range_end": "2017-12-31",
        "holiday": "NEW_YEARS",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_holiday_calendar_sap.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "holidayAssignments": {
                            "results": [
                                {
                                    "date": test_data["nye_return_date"],
                                    "holiday": test_data["holiday"],
                                }
                            ]
                        }
                    }
                ]
            }
        }

        # Get country of employment
        response = get_holiday_calendar_sap(
            country=test_data["country"],
            date_range_start=test_data["date_range_start"],
            date_range_end=test_data["date_range_end"],
        )

        # Ensure that get_holiday_calendar_sap() executed and returned proper values
        assert response
        assert len(response.holiday_list)
        assert response.holiday_list[0].date == test_data["nye_return_date"]
        assert response.holiday_list[0].holiday == test_data["holiday"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="HolidayCalendar",
            filter_expr=f"country eq '{test_data['country']}'",
            expand_expr="holidayAssignments",
        )
