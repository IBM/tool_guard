from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_personal_details import (
    get_personal_details,
)


def test_get_personal_details() -> None:
    """Test that the `get_personal_details` function returns the expected response."""
    # Define test data:
    test_data = {
        "person_id": "108727",
        "first_name": "John",
        "last_name": "Smith",
        "nationality": "USA",
        "gender": "M",
        "country": "Canada",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_personal_details.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "personalInfoNav": {
                            "results": [
                                {
                                    "firstName": test_data["first_name"],
                                    "lastName": test_data["last_name"],
                                    "nationality": test_data["nationality"],
                                    "gender": test_data["gender"],
                                }
                            ]
                        },
                        "nationalIdNav": {"results": [{"country": test_data["country"]}]},
                    }
                ]
            }
        }

        # Get location ID
        response = get_personal_details(person_id_external=test_data["person_id"])

        # Ensure that get_personal_details() executed and returned proper values
        assert response
        assert response.first_name == test_data["first_name"]
        assert response.last_name == test_data["last_name"]
        assert response.nationality == test_data["nationality"]
        assert response.gender == test_data["gender"]
        assert response.country == test_data["country"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="PerPerson",
            filter_expr=f"personIdExternal eq '{test_data['person_id']}'",
            expand_expr="personalInfoNav,nationalIdNav",
        )
