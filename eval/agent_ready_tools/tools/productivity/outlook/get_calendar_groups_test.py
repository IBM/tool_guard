from unittest.mock import MagicMock, patch

from requests import Response
from requests.exceptions import HTTPError

from agent_ready_tools.tools.productivity.outlook.get_calendar_groups import (
    CalendarGroup,
    get_calendar_groups,
)


def test_get_calendar_groups_with_filter() -> None:
    """Tests retrieval of calendar groups using a filter."""

    test_data = {
        "calendar_group_name": "gurrrrrrrrrrrrrrrrrrrrr",
        "calendar_group_class_id": "0006f0b7-0000-0000-c000-000000000046",
        "calendar_group_change_key": "/8mpclnBWUu5NxcDfUb/WwACS2G3Fw==",
        "calendar_group_id": "AQMkADYyODVkMjM5LTFlZQA3LTRmMWYtYThjOC1hYmY2Mjc5ZDE5ODYARgAAA5zjV7sSmoBNlqiW3HRRFSgHAP-JqXJZwVlLuTcXA31G-1sAAAIBBgAAAP-JqXJZwVlLuTcXA31G-1sAAAI7ZQAAAA==",
        "user_name": "user@example.com",
    }

    limit = 10
    skip = 0

    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_calendar_groups.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "name": test_data["calendar_group_name"],
                    "classId": test_data["calendar_group_class_id"],
                    "changeKey": test_data["calendar_group_change_key"],
                    "id": test_data["calendar_group_id"],
                }
            ],
            "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/calendarGroups?$top=10&$skip=10",
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data['user_name']}"

        response = get_calendar_groups(calendar_group_name=test_data["calendar_group_name"])

        expected_group = CalendarGroup(
            calendar_group_name=test_data["calendar_group_name"],
            calendar_group_class_id=test_data["calendar_group_class_id"],
            calendar_group_change_key=test_data["calendar_group_change_key"],
            calendar_group_id=test_data["calendar_group_id"],
        )

        assert response.calendar_groups[0] == expected_group
        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data['user_name']}/calendarGroups",
            params={
                "$filter": f"name eq '{test_data['calendar_group_name']}'",
                "$top": limit,
                "$skip": skip,
            },
        )


def test_get_calendar_groups_without_filter() -> None:
    """Tests retrieval of calendar groups without any filter."""

    test_data = {
        "calendar_group_name": "gurrrrrrrrrrrrrrrrrrrrr",
        "calendar_group_class_id": "0006f0b7-0000-0000-c000-000000000046",
        "calendar_group_change_key": "/8mpclnBWUu5NxcDfUb/WwACS2G3Fw==",
        "calendar_group_id": "AQMkADYyODVkMjM5LTFlZQA3LTRmMWYtYThjOC1hYmY2Mjc5ZDE5ODYARgAAA5zjV7sSmoBNlqiW3HRRFSgHAP-JqXJZwVlLuTcXA31G-1sAAAIBBgAAAP-JqXJZwVlLuTcXA31G-1sAAAI7ZQAAAA==",
        "user_name": "user@example.com",
    }

    limit = 10
    skip = 0
    output_limit = 10
    output_skip = 10

    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_calendar_groups.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "name": test_data["calendar_group_name"],
                    "classId": test_data["calendar_group_class_id"],
                    "changeKey": test_data["calendar_group_change_key"],
                    "id": test_data["calendar_group_id"],
                }
            ],
            "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/calendarGroups?$top=10&$skip=10",
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data['user_name']}"

        response = get_calendar_groups()

        expected_group = CalendarGroup(
            calendar_group_name=test_data["calendar_group_name"],
            calendar_group_class_id=test_data["calendar_group_class_id"],
            calendar_group_change_key=test_data["calendar_group_change_key"],
            calendar_group_id=test_data["calendar_group_id"],
        )

        assert response.calendar_groups[0] == expected_group
        assert response.limit == output_limit
        assert response.skip == output_skip

        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data['user_name']}/calendarGroups",
            params={"$top": limit, "$skip": skip},
        )


def test_get_calendar_groups_http_error_json() -> None:
    """Tests handling of HTTPError with JSON error response."""

    test_data = {
        "calendar_group_name": "Work",
        "error_http_code": 403,
        "error_message": "Access denied.",
    }

    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_calendar_groups.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_user_resource_path.return_value = "me"

        mock_response = MagicMock(spec=Response)
        mock_response.status_code = test_data["error_http_code"]
        mock_response.json.return_value = {"error": {"message": test_data["error_message"]}}

        http_error = HTTPError(response=mock_response)
        mock_client.get_request.side_effect = http_error

        response = get_calendar_groups(calendar_group_name=test_data["calendar_group_name"])

        assert response.http_code == test_data["error_http_code"]
        assert response.error_message == test_data["error_message"]
        assert response.calendar_groups is None
