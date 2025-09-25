from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_address_types import (
    get_address_types_oracle,
)


def test_address_types() -> None:
    """Test that the `get_address_types_oracle` function returns the expected response."""

    # Define test data:
    test_data = {"lookup_code": "SG_CQ", "meaning": "Company quarters"}

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_address_types.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "LookupCode": test_data["lookup_code"],
                    "Meaning": test_data["meaning"],
                }
            ]
        }

        # Get address types
        response = get_address_types_oracle()

        # Ensure that get_address_types_oracle() returned proper list of address types
        assert response
        assert response.address_types
        assert response.address_types[0].address_type_code == test_data["lookup_code"]
        assert response.address_types[0].address_type_name == test_data["meaning"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="commonLookupsLOV", q_expr="LookupType='ADDRESS_TYPE'", path="fscmRestApi"
        )
