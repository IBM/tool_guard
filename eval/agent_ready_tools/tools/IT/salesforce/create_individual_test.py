from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.create_individual import create_individual


def test_create_individual() -> None:
    """Tests that the individual can be created successfully by the `create_individual` tool."""

    # Define test data:
    test_data = {
        "last_name": "Doe",
        "first_name": "John",
        "birth_date": "1990-01-01",
        "occupation": "Engineer",
        "individual_id": "0PKfJ0000000wATWAY",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.create_individual.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Individual.create.return_value = {
            "id": test_data["individual_id"]
        }

        # Create an individual
        response = create_individual(
            last_name=test_data["last_name"],
            first_name=test_data["first_name"],
            birth_date=test_data["birth_date"],
            occupation=test_data["occupation"],
        )

        # Ensure that create_individual() executed and returned proper values
        assert response
        assert response.individual_id is not None

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Individual.create(
            {
                "LastName": test_data["last_name"],
                "FirstName": test_data["first_name"],
                "BirthDate": test_data["birth_date"],
                "Occupation": test_data["occupation"],
            }
        )
