from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_departments import get_departments


def test_get_departments() -> None:
    """Test that departments can be retrieved successfully."""

    # Define test data:
    test_data = {
        "id": "1d995b11935b0210ca7e326efaba10c2",
        "name": "namr",
        "company": "ACME North America",
        "head": "Nelly Jakuboski",
        "contact": "Nelly Jakuboski",
        "limit": 10,
        "skip": 0,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_departments.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "name": test_data["name"],
                    "parent_department": "",
                    "description": "cf",
                    "business_unit": "",
                    "dept_head": {"display_value": test_data["head"]},
                    "company": {"display_value": test_data["company"]},
                    "primary_contact": {"display_value": test_data["contact"]},
                },
            ],
        }

        # Get departments
        response = get_departments()

        # Ensure that get_departments() executed and returned proper values
        assert response
        assert len(response.departments)
        assert response.departments[0].system_id == test_data["id"]
        assert response.departments[0].department_name == test_data["name"]
        assert response.departments[0].department_head == test_data["head"]
        assert response.departments[0].company == test_data["company"]
        assert response.departments[0].primary_contact == test_data["contact"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="cmn_department",
            params={
                "sysparm_limit": test_data["limit"],
                "sysparm_offset": test_data["skip"],
                "sysparm_display_value": True,
            },
        )
