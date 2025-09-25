import json
from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.coupa.get_departments import (
    coupa_get_departments,
)


def test_coupa_get_departments() -> None:
    """Test that the `get_all_departments` function returns the expected response."""

    # Define test data:
    test_data: list[dict[str, Any]] = [
        {"id": 1, "name": "Marketing", "active": True},
        {"id": 2, "name": "Sales", "active": True},
        {"id": 3, "name": "IT", "active": True},
        {"id": 4, "name": "Development", "active": True},
        {"id": 5, "name": "Operations", "active": True},
    ]
    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.coupa.get_departments.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = test_data

        # Get all departments
        response = coupa_get_departments().content

        # Ensure that get_all_departments() executed and returned proper values
        assert response
        assert response.department_list and len(response.department_list) == 5
        assert response.department_list[0].department_name == test_data[0]["name"]
        assert response.department_list[1].department_name == test_data[1]["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="departments", params={"fields": json.dumps(["id", "name", "active"])}
        )
