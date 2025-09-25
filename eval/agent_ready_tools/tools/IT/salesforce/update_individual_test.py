from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_individual import update_individual


def test_update_individual() -> None:
    """Test that the `update_individual` function returns the expected response."""

    # Define test data:
    test_data = {
        "individual_id": "0PKgL000002CuA9WAK",
        "first_name": "Test",
        "last_name": "JohnDo",
        "occupation": "Plumber",
        "birth_date": "1985-10-15",
        "owner_id": "005gL000001qXQjQAM",
        "website": "www.helloworld.com",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_individual.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Individual.update.return_value = test_response

        # Update individual
        response = update_individual(**test_data)

        # Ensure that update_individual() has executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Individual.update(test_data["individual_id"], test_data)
