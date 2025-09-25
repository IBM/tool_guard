from unittest.mock import MagicMock, patch

from requests import Response
from requests.exceptions import HTTPError

from agent_ready_tools.tools.productivity.outlook.get_calendars import CalendarInfo, get_calendars


def test_get_calendars_success() -> None:
    """Verifies successful retrieval of calendars in Microsoft Outlook."""

    test_data = {
        "calendar_id": "AQMkADYyODVkMjM5LTFlZQA3LTRmMWYtYThjOC1hYmY2Mjc5ZDE5ODYARgAAA5zjV7sSmoBNlqiW3HRRFSgHAP-JqXJZwVlLuTcXA31G-1sAAAIBBgAAAP-JqXJZwVlLuTcXA31G-1sAAAI7ZgAAAA==",
        "calendar_name": "Calendar",
        "owner_name": "cstest",
        "user_name": "user@example.com",
    }
    limit = 3
    skip = 1
    output_limit = 3
    output_skip = 4

    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_calendars.get_microsoft_client"
    ) as mock_outlook_client:
        mock_client = MagicMock()
        mock_outlook_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["calendar_id"],
                    "name": test_data["calendar_name"],
                    "owner": {"name": test_data["owner_name"]},
                }
            ],
            "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/calendars?$top=3&$skip=4",
        }
        mock_client.get_user_resource_path.return_value = f"users/{test_data['user_name']}"

        response = get_calendars(limit=limit, skip=skip)

        expected_response = CalendarInfo(
            calendar_id=test_data["calendar_id"],
            calendar_name=test_data["calendar_name"],
            owner_name=test_data["owner_name"],
        )

        assert response.calendars[0] == expected_response
        assert response.limit == output_limit
        assert response.skip == output_skip

        mock_client.get_request.assert_called_once_with(
            endpoint=f"users/{test_data['user_name']}/calendars",
            params={"$top": limit, "$skip": skip},
        )


def test_get_calendars_http_error_json() -> None:
    """Tests handling of HTTPError with JSON error response."""

    test_data = {
        "calendar_name": "Work",
        "error_http_code": 403,
        "error_message": "Access denied.",
    }

    with patch(
        "agent_ready_tools.tools.productivity.outlook.get_calendars.get_microsoft_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_user_resource_path.return_value = "me"

        mock_response = MagicMock(spec=Response)
        mock_response.status_code = test_data["error_http_code"]
        mock_response.json.return_value = {"error": {"message": test_data["error_message"]}}

        http_error = HTTPError(response=mock_response)
        mock_client.get_request.side_effect = http_error

        response = get_calendars(calendar_name=test_data["calendar_name"])

        assert response.http_code == test_data["error_http_code"]
        assert response.error_message == test_data["error_message"]
        assert response.calendars is None
