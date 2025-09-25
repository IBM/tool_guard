from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.common.sap_successfactors.get_location_id import get_location_id


def test_get_location_id_live() -> None:
    """Test that the `get_location_id` function returns the expected response."""
    # Define test data:
    test_data = {"location": "New York", "location_id": "1710-2007", "company": "1710"}

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.common.sap_successfactors.get_location_id.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {"externalCode": test_data["location_id"], "name": test_data["location"]}
                ]
            }
        }

        # Get location ID
        response = get_location_id(
            location_query=test_data["location"], company=test_data["company"]
        )

        # Ensure that get_location_id() executed and returned proper values
        assert response
        assert len(response.locations)
        assert response.locations[0].location == test_data["location"]
        assert response.locations[0].location_id == test_data["location_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="FOLocation",
            filter_expr=f"status eq 'A' and name eq '{test_data['location']}' and companyFlxNav/externalCode eq '{test_data['company']}'",
            select_expr="externalCode,name",
        )
