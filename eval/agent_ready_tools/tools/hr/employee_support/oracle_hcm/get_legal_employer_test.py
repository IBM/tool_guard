from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_legal_employer import (
    get_legal_employer,
)


def test_get_legal_employer() -> None:
    """Test that the `get_legal_employer` function returns the expected response."""

    # Define test data:
    test_data = {"name": "IBM", "legal_name": "Internation Business Machines, USA"}
    limit = 20
    offset = 0
    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_legal_employer.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "Name": test_data["legal_name"],
                }
            ]
        }

        # Get employer legal name
        response = get_legal_employer(legal_employer_name=test_data["name"])

        # Ensure that get_legal_employer() executed and returned proper values
        assert response
        assert len(response.legal_employer_names)
        assert response.legal_employer_names[0].legal_employer_name == test_data["legal_name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="legalEmployersLov",
            q_expr=f"Name='{test_data['name']}'",
            params={"limit": limit, "offset": offset},
        )
