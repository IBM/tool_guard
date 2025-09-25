from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.oracle_hcm.get_candidates import get_candidates


def test_get_candidates() -> None:
    """Test that the `get_candidates` function returns the expected response."""
    # Define test data
    test_data = {
        "candidate_number": 1227,
        "first_name": "Dheeraj",
        "last_name": "Lall",
        "full_name": "Lall, Dheeraj",
        "candidate_email": "test@abc.com",
        "candidate_type": "ORA_INTERNAL_CANDIDATE",
        "limit": "5",
        "offset": "0",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.oracle_hcm.get_candidates.get_oracle_hcm_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "CandidateNumber": test_data["candidate_number"],
                    "FirstName": test_data["first_name"],
                    "LastName": test_data["last_name"],
                    "FullName": test_data["full_name"],
                    "Email": test_data["candidate_email"],
                    "CandidateType": test_data["candidate_type"],
                },
            ]
        }

        # Get all candidates
        response = get_candidates(
            last_name=test_data["last_name"],
            limit=test_data["limit"],
            offset=test_data["offset"],
        )

        # Ensure that get_candidates() executed and returned proper values
        assert response
        assert len(response.candidates)
        assert response.candidates[0].candidate_number == test_data["candidate_number"]
        assert response.candidates[0].first_name == test_data["first_name"]
        assert response.candidates[0].last_name == test_data["last_name"]
        assert response.candidates[0].full_name == test_data["full_name"]
        assert response.candidates[0].candidate_email == test_data["candidate_email"]
        assert response.candidates[0].candidate_type == test_data["candidate_type"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="recruitingCandidates",
            q_expr=f"LastName={test_data["last_name"]}",
            params={
                "limit": test_data["limit"],
                "offset": test_data["offset"],
            },
        )
