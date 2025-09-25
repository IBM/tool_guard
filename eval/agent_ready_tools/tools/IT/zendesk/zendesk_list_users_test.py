from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.zendesk_list_users import (
    ZendeskUserListResponse,
    zendesk_list_users,
)


def test_zendesk_list_users_with_name_filter() -> None:
    """Verifies that a user is listed correctly when filtering by name."""

    # Test data for a single user
    test_data = {
        "id": 12345,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "role": "admin",
        "alias": "JD",
        "notes": "Test user note",
        "active": True,
        "phone": "123-456-7890",
        "user_fields": {"department": "IT"},
    }

    # Mock response for the 'search' endpoint
    mock_search_response = {"results": [test_data]}

    with patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_list_users.get_zendesk_client"
    ) as mock_get_client:
        # Create a mock client
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_search_response

        # Call the function with a name filter
        result = zendesk_list_users(name="John Doe")

        # Assertions
        assert isinstance(result, ZendeskUserListResponse)
        assert isinstance(result.users, list)
        assert len(result.users) == 1

        user = result.users[0]
        assert user.user_id == str(test_data["id"])
        assert user.name == "John Doe"
        assert user.email == "john.doe@example.com"
        assert user.alias == "JD"
        assert user.notes == "Test user note"
        assert user.role == "admin"
        assert user.active is True
        assert user.phone == "123-456-7890"
        assert user.custom_fields == {"department": "IT"}

        # Ensure the API call was made with the expected query
        expected_params = {
            "per_page": 10,
            "page": 1,
            "query": 'type:user name:"John Doe"',
        }
        mock_client.get_request.assert_called_once_with(entity="search", params=expected_params)


def test_zendesk_list_all_users() -> None:
    """Verifies that all users are listed correctly when no filter is provided."""

    # User payload for the mock response
    user_payload = {
        "id": 12345,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "role": "admin",
        "alias": "JD",
        "notes": "Test user note",
        "active": True,
        "phone": "123-456-7890",
        "user_fields": {"department": "IT"},
    }

    # Mock response for the 'users' endpoint
    mock_users_response = {"users": [user_payload]}

    with patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_list_users.get_zendesk_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_users_response

        # Call the function without filters
        result = zendesk_list_users()

        # Assertions
        assert len(result.users) == 1
        user = result.users[0]
        assert user.user_id == str(user_payload["id"])
        assert user.name == user_payload["name"]
        assert user.email == user_payload["email"]
        assert user.alias == user_payload["alias"]
        assert user.notes == user_payload["notes"]
        assert user.role == user_payload["role"]
        assert user.active is user_payload["active"]
        assert user.phone == user_payload["phone"]
        assert user.custom_fields == user_payload["user_fields"]

        # Ensure the API call was made to the correct endpoint
        mock_client.get_request.assert_called_once_with(
            entity="users", params={"per_page": 10, "page": 1}
        )


def test_zendesk_list_users_no_match() -> None:
    """Verifies the tool's behavior when no users match the filter."""

    # Mock response for no results
    mock_users_response: Dict[str, List[Any]] = {"results": []}

    with patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_list_users.get_zendesk_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = mock_users_response

        # Call the function with a filter that yields no results
        result = zendesk_list_users(name="Non Existent User")

        # Assertions
        assert len(result.users) == 0
        assert result.message == "No data or no match found."

        # Ensure the API call was made correctly
        expected_params = {
            "per_page": 10,
            "page": 1,
            "query": 'type:user name:"Non Existent User"',
        }
        mock_client.get_request.assert_called_once_with(entity="search", params=expected_params)
