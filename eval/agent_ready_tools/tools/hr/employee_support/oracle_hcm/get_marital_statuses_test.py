from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_marital_statuses import (
    get_marital_statuses,
)


def test_get_marital_statuses() -> None:
    """Tests that the `get_marital_statuses` function returns the expected response."""

    # Define test data:
    test_data = {
        "description": "Single",
        "martial_status_id": "S",
        "LookupType": "MAR_STATUS",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_marital_statuses.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {"Meaning": test_data["description"], "LookupCode": test_data["martial_status_id"]}
            ]
        }

        # Get the marital statuses
        response = get_marital_statuses()

        # Ensure that get_marital_statuses is executed and returns proper values
        assert response

        assert response.lookups[0].description == test_data["description"]
        assert response.lookups[0].martial_status_id == test_data["martial_status_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "commonLookupsLOV", q_expr="LookupType='MAR_STATUS'", path="fscmRestApi"
        )
