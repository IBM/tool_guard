from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.update_a_department import update_a_department


def test_update_a_department() -> None:
    """Test that the department can be updated successfully by the `update_a_department` tool."""

    # Define test data:
    test_data = {
        "department_name_system_id": "2f06e8cb83842610e73115a6feaad30f",
        "description": "Testing through Agent",
        "head_count": "3",
        "business_unit_name": "Legal",
        "department_head_system_id": "John21 Doe",
        "cost_center_name": "Sales",
        "primary_contact_system_id": "John21 Doe",
        "http_code": 200,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.update_a_department.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.patch_request.return_value = {"status_code": test_data["http_code"]}

        # Update a department
        response = update_a_department(
            department_name_system_id=test_data["department_name_system_id"],
            description=test_data["description"],
            head_count=test_data["head_count"],
            business_unit_name=test_data["business_unit_name"],
            department_head_system_id=test_data["department_head_system_id"],
            cost_center_name=test_data["cost_center_name"],
            primary_contact_system_id=test_data["primary_contact_system_id"],
        )

        # Ensure that update_a_department() executed and returned proper values
        assert response
        assert response.http_code == 200

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity="cmn_department",
            entity_id=test_data["department_name_system_id"],
            payload={
                "description": test_data["description"],
                "head_count": test_data["head_count"],
                "business_unit": test_data["business_unit_name"],
                "dept_head": test_data["department_head_system_id"],
                "cost_center": test_data["cost_center_name"],
                "primary_contact": test_data["primary_contact_system_id"],
            },
        )
