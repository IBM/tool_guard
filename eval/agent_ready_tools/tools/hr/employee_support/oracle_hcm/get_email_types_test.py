from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_email_types import (
    get_email_types_oracle,
)


def test_get_email_types_oracle() -> None:
    """Test that the `get_email_types_oracle` function returns the expected response."""

    # Define test data:
    test_data = {"email_type_code": "W1", "email_type_name": "Work Email"}

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_email_types.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "Meaning": test_data["email_type_name"],
                    "LookupCode": test_data["email_type_code"],
                }
            ]
        }

        # Get email types
        response = get_email_types_oracle()

        # Ensure that get_email_types_oracle() executed and returned proper values
        assert response
        assert len(response.email_types)
        assert response.email_types[0].email_type_code == test_data["email_type_code"]
        assert response.email_types[0].email_type_name == test_data["email_type_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="commonLookupsLOV", q_expr="LookupType='EMAIL_TYPE'", path="fscmRestApi"
        )
