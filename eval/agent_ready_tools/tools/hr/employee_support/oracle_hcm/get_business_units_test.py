from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_business_units import (
    get_business_units_oracle,
)


def test_get_business_units_oracle() -> None:
    """Test that the `get_business_units_oracle` function returns the expected response."""

    # Define test data:
    test_data = {
        "name": "Algeria Business Unit",
    }
    limit = 20
    offset = 0

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_business_units.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "Name": test_data["name"],
                }
            ]
        }

        # Get all business units
        response = get_business_units_oracle(business_unit_name=test_data["name"])

        # Ensure that get_business_units_oracle() executed and returned proper values
        assert response
        assert len(response.business_units)
        assert response.business_units[0].business_unit_name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="hcmBusinessUnitsLOV",
            q_expr=f"Name='{test_data['name']}'",
            params={"limit": limit, "offset": offset},
        )
