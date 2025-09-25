from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_phone_types import (
    get_phone_types_oracle,
)


def test_get_phone_types_oracle() -> None:
    """Test that the `get_phone_types_oracle` function returns the expected response."""

    # Define test data:
    test_data = {"type_code": "W1", "type_name": "Work Phone"}

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_phone_types.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [{"Meaning": test_data["type_name"], "LookupCode": test_data["type_code"]}]
        }

        # Get phone types
        response = get_phone_types_oracle()

        # Ensure that get_phone_types_oracle() executed and returned proper values
        assert response
        assert len(response.phone_types)
        assert response.phone_types[0].phone_type_code == test_data["type_code"]
        assert response.phone_types[0].phone_type_name == test_data["type_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="commonLookupsLOV", q_expr="LookupType='PHONE_TYPE'", path="fscmRestApi"
        )
