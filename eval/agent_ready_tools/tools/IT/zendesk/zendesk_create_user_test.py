from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.zendesk_create_user import (
    CreateUserResponse,
    zendesk_create_user,
)


def test_create_user_success() -> None:
    """Tests successful creation of a user in Zendesk."""

    # Test input
    name = "John Doe"
    email = "john.doe@example.com"
    role = "end-user"

    # Mocked response from Zendesk API
    mock_user_id = 123456789
    mock_response = {"user": {"id": mock_user_id, "name": name, "email": email, "role": role}}

    with patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_create_user.get_zendesk_client"
    ) as mock_get_client, patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_create_user.validate_role_enum_value"
    ) as mock_validate_role:
        # Setup mock client and role validator
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = mock_response
        mock_validate_role.return_value = role

        # Call the function
        result = zendesk_create_user(name=name, email=email, role=role)

        # Expected result
        expected = CreateUserResponse(
            user_id=str(mock_user_id), name=name, email=email, role=role, error_message=None
        )

        # Assertions
        assert result == expected

        # Assert correct API call
        mock_client.post_request.assert_called_once_with(
            entity="users", payload={"user": {"name": name, "email": email, "role": role}}
        )


def test_create_user_invalid_role() -> None:
    """Tests user creation with an invalid role value not in the enum."""

    # Test input
    name = "Jane Doe"
    email = "jane.doe@example.com"
    role = "super-admin"  # Invalid role not in enum

    # Simulated error message from role validation
    error_message = f"Invalid role: {role}"

    with patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_create_user.get_zendesk_client"
    ) as mock_get_client, patch(
        "agent_ready_tools.tools.IT.zendesk.zendesk_create_user.validate_role_enum_value"
    ) as mock_validate_role:
        # Setup mock to raise ValueError for invalid role
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_validate_role.side_effect = ValueError(error_message)

        # Call the function
        result = zendesk_create_user(name=name, email=email, role=role)

        # Expected result
        expected = CreateUserResponse(
            user_id="", name=name, email=email, role=role, error_message=error_message
        )

        # Assertions
        assert result == expected
