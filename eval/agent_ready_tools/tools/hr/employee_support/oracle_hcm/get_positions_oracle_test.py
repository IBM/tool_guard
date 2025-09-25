from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_positions_oracle import (
    get_positions_oracle,
)


def test_get_positions_oracle() -> None:
    """Test that the `get_positions_oracle` function returns the expected response."""

    # Define test data:
    test_data = {
        "position_name": "Academic Advisor",
        "position_code": "PRGCAPOS101",
        "position_id": 300000250515053,
        "job_id": 300000250545331,
        "job_code": "PRGCANJOB250",
        "job_name": "CAN Analyst",
        "hiring_status": "Approved",
        "department_id": 300000250545709,
        "department_name": "Admissions Prg CAN",
        "business_unit_id": 300000250518753,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_positions_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "PositionName": test_data["position_name"],
                    "PositionCode": test_data["position_code"],
                    "PositionId": test_data["position_id"],
                    "JobId": test_data["job_id"],
                    "JobCode": test_data["job_code"],
                    "JobName": test_data["job_name"],
                    "HiringStatus": test_data["hiring_status"],
                    "DepartmentId": test_data["department_id"],
                    "DepartmentName": test_data["department_name"],
                    "BusinessUnitId": test_data["business_unit_id"],
                }
            ]
        }

        # Get all positions
        response = get_positions_oracle()

        # Ensure that get_positions_oracle() executed and returned proper values
        assert response
        assert len(response.positions)
        assert response.positions[0].position_name == test_data["position_name"]
        assert response.positions[0].position_code == test_data["position_code"]
        assert response.positions[0].position_id == test_data["position_id"]
        assert response.positions[0].job_id == test_data["job_id"]
        assert response.positions[0].job_code == test_data["job_code"]
        assert response.positions[0].job_name == test_data["job_name"]
        assert response.positions[0].hiring_status == test_data["hiring_status"]
        assert response.positions[0].department_id == test_data["department_id"]
        assert response.positions[0].department_name == test_data["department_name"]
        assert response.positions[0].business_unit_id == test_data["business_unit_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(entity="positionsLov")


def test_get_positions_oracle_filter() -> None:
    """Test that the `get_positions_oracle` function returns the expected response with filter
    parameter."""

    # Define test data:
    test_data = {
        "position_name": "Academic Advisor",
        "position_code": "PRGCAPOS101",
        "position_id": 300000250515053,
        "job_id": 300000250545331,
        "job_code": "PRGCANJOB250",
        "job_name": "CAN Analyst",
        "hiring_status": "Approved",
        "department_id": 300000250545709,
        "department_name": "Admissions Prg CAN",
        "business_unit_id": 300000250518753,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_positions_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "PositionName": test_data["position_name"],
                    "PositionCode": test_data["position_code"],
                    "PositionId": test_data["position_id"],
                    "JobId": test_data["job_id"],
                    "JobCode": test_data["job_code"],
                    "JobName": test_data["job_name"],
                    "HiringStatus": test_data["hiring_status"],
                    "DepartmentId": test_data["department_id"],
                    "DepartmentName": test_data["department_name"],
                    "BusinessUnitId": test_data["business_unit_id"],
                }
            ]
        }

        # Get all positions
        response = get_positions_oracle(position_name=test_data["position_name"])

        # Ensure that get_positions_oracle() executed and returned proper values
        assert response
        assert len(response.positions)
        assert response.positions[0].position_name == test_data["position_name"]
        assert response.positions[0].position_code == test_data["position_code"]
        assert response.positions[0].position_id == test_data["position_id"]
        assert response.positions[0].job_id == test_data["job_id"]
        assert response.positions[0].job_code == test_data["job_code"]
        assert response.positions[0].job_name == test_data["job_name"]
        assert response.positions[0].hiring_status == test_data["hiring_status"]
        assert response.positions[0].department_id == test_data["department_id"]
        assert response.positions[0].department_name == test_data["department_name"]
        assert response.positions[0].business_unit_id == test_data["business_unit_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(entity="positionsLov")
