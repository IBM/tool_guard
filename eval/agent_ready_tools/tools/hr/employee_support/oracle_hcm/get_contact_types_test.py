from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_contact_types import (
    get_contact_types,
)


def test_get_contact_types() -> None:
    """Test that the `get_contact_types` function returns the expected response."""

    # Define test data:
    test_data = {
        "country": "US",
        "contact_type": "A",
        "relation": "Adopted child",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_contact_types.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "Tag": test_data["country"],
                    "LookupCode": test_data["contact_type"],
                    "Meaning": test_data["relation"],
                }
            ]
        }

        # Get contact types
        response = get_contact_types(country=test_data["country"])

        # Ensure that get_contact_types() executed and returned proper values
        assert response
        assert len(response.contact_types)
        assert response.contact_types[0].contact_type == test_data["contact_type"]
        assert response.contact_types[0].relation == test_data["relation"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"commonLookupsLOV",
            q_expr=f"LookupType='CONTACT'",
            path="fscmRestApi",
            headers={"REST-Framework-Version": "4"},
            params={"limit": 500},
        )
