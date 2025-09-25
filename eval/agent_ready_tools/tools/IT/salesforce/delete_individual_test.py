from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.delete_individual import delete_individual


def test_delete_individual() -> None:
    """Test that the `delete_individual` function returns the expected response."""
    # Define test data:
    individual_id = "0PKgL000002KsvxWAC"
    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.delete_individual.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Individual.delete.return_value = test_response

        # Call the function
        response = delete_individual(individual_id)

        # Ensure that the delete_an_individual() has been executed and returned the expected response
        assert response
        assert response.http_code == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Individual.delete.assert_called_once_with(individual_id)
