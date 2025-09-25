from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_roles import list_roles
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Role


def test_fetch_user_roles_with_filter() -> None:
    """Tests that the user roles from Salesforce can be retrieved successfully (with filter)."""

    # Define test data:
    test_data = {
        "role_id": "00EgL000001MnKrUAK",
        "role_name": "AI developer",
        "parent_role_id": None,
        "developer_name": "AI_developer",
        "forecast_user_id": None,
    }
    expected = Role(**test_data)  # type: ignore[arg-type]
    # Define limit and offset for the query
    limit = 100
    offset = 0
    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_roles.get_salesforce_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["role_id"],
                "Name": test_data["role_name"],
                "ParentRoleId": test_data["parent_role_id"],
                "DeveloperName": test_data["developer_name"],
                "ForecastUserId": test_data["forecast_user_id"],
            }
        ]
        # Get user roles
        response = list_roles(search="DeveloperName = 'AI_developer'")

        assert response
        assert len(response)
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            f"SELECT Id, Name, ParentRoleId, DeveloperName, ForecastUserId FROM UserRole WHERE DeveloperName = 'AI_developer' LIMIT {limit} OFFSET {offset}"
        )


def test_fetch_user_roles_without_filter() -> None:
    """Tests that the user roles from Salesforce can be retrieved successfully (without filter)."""

    # Define test data:
    test_data = {
        "role_id": "00EgL000001MnKrUAK",
        "role_name": "AI developer",
        "parent_role_id": None,
        "developer_name": "AI_developer",
        "forecast_user_id": None,
    }
    expected = Role(**test_data)  # type: ignore[arg-type]
    # Define limit and offset for the query
    limit = 100
    offset = 0

    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_roles.get_salesforce_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["role_id"],
                "Name": test_data["role_name"],
                "ParentRoleId": test_data["parent_role_id"],
                "DeveloperName": test_data["developer_name"],
                "ForecastUserId": test_data["forecast_user_id"],
            }
        ]
        # Get user roles
        response = list_roles()

        assert response
        assert len(response)
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            f"SELECT Id, Name, ParentRoleId, DeveloperName, ForecastUserId FROM UserRole  LIMIT {limit} OFFSET {offset}"
        )
