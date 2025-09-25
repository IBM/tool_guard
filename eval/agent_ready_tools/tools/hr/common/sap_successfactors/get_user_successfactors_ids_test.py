from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.common.sap_successfactors.get_user_successfactors_ids import (
    get_user_successfactors_ids,
)


def test_get_user_successfactors_ids() -> None:
    """Tests that the `get_user_successfactors_ids` tool functions as expected."""
    # Define test data:
    test_data = {
        "email": "ron.diaz@bestrunsap.com",
        "username": "rondiaz",
        "name": "Ron Diaz",
        "user_id": "97382131",
        "person_id": "132152",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.common.sap_successfactors.get_user_successfactors_ids.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "userId": test_data["user_id"],
                        "personIdExternal": test_data["person_id"],
                        "username": test_data["username"],
                        "displayName": test_data["name"],
                    }
                ]
            }
        }

        # Get User SuccessFactors IDs
        response = get_user_successfactors_ids(email=test_data["email"])

        # Ensure that get_user_successfactors_ids() executed and returned proper values
        assert response
        assert response.user_id == test_data["user_id"]
        assert response.username == test_data["username"]
        assert response.name == test_data["name"]
        assert response.person_id_external == test_data["person_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_with(
            "EmpEmployment",
            filter_expr=f"userId eq '{test_data['user_id']}'",
            select_expr="personIdExternal",
        )
