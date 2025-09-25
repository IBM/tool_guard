from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_all_candidates import (
    get_all_candidates,
)


def test_get_all_candidates() -> None:
    """Test that the `get_all_candidates` function returns the expected response."""
    # Define test data
    test_data = {
        "candidate_id": "1227",
        "country": "India",
        "first_name": "Dheeraj",
        "last_name": "Lall",
        "address": "Andheri",
        "contact_email": "test@abc.com",
        "city": "Mumbai",
        "cell_phone": "+919619524455",
        "zip_code": "473727",
        "top": "5",
        "skip": "0",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_all_candidates.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "candidateId": test_data["candidate_id"],
                        "country": test_data["country"],
                        "firstName": test_data["first_name"],
                        "lastName": test_data["last_name"],
                        "address": test_data["address"],
                        "contactEmail": test_data["contact_email"],
                        "city": test_data["city"],
                        "cellPhone": test_data["cell_phone"],
                        "zip": test_data["zip_code"],
                    },
                ]
            }
        }

        # Get all candidates
        response = get_all_candidates(
            city=test_data["city"],
            top=test_data["top"],
            skip=test_data["skip"],
        )

        # Ensure that get_all_candidates() executed and returned proper values
        assert response
        assert len(response.candidates)
        assert response.candidates[0].candidate_id == test_data["candidate_id"]
        assert response.candidates[0].country == test_data["country"]
        assert response.candidates[0].first_name == test_data["first_name"]
        assert response.candidates[0].last_name == test_data["last_name"]
        assert response.candidates[0].address == test_data["address"]
        assert response.candidates[0].contact_email == test_data["contact_email"]
        assert response.candidates[0].city == test_data["city"]
        assert response.candidates[0].cell_phone == test_data["cell_phone"]
        assert response.candidates[0].zip_code == test_data["zip_code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="Candidate",
            filter_expr=f"city eq '{test_data["city"]}'",
            select_expr=f"candidateId,country,zip,firstName,lastName,education,address,contactEmail,cellPhone,city",
            params={
                "$top": test_data["top"],
                "$skip": test_data["skip"],
            },
        )
