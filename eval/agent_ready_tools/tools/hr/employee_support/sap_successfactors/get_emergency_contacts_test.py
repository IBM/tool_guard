from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_emergency_contacts import (
    get_emergency_contacts_sap,
)


def test_get_emergency_contacts() -> None:
    """Test that all the emergency contacts can be retrieved successfully."""

    # Define test data:
    test_data = {
        "person_id": "103362",
        "email": "test1_ramu@test.com",
        "phone": "6303714329",
        "name": "Ramu",
        "relationship": "relation_Child",
        "relationship_id": "1234",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_emergency_contacts.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "name": test_data["name"],
                        "relationship": test_data["relationship_id"],
                        "phone": test_data["phone"],
                        "email": test_data["email"],
                        "relationshipNav": {
                            "externalCode": test_data["relationship"],
                        },
                    }
                ]
            }
        }

        response = get_emergency_contacts_sap(person_id=test_data["person_id"]).emergency_contacts[
            0
        ]

        assert response
        assert response.email == test_data["email"]
        assert response.name == test_data["name"]
        assert response.phone == test_data["phone"]
        assert response.relationship == test_data["relationship"]
        assert response.relationship_id == test_data["relationship_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="PerEmergencyContacts",
            filter_expr=f"personIdExternal eq '{test_data['person_id']}'",
            expand_expr="relationshipNav",
        )
