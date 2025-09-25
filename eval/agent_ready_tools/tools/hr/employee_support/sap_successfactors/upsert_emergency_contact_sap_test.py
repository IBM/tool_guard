from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.upsert_emergency_contact_sap import (
    upsert_emergency_contact_sap,
)


def test_upsert_emergency_contact_sap() -> None:
    """Test that an emergency contact can be updated successfully by the
    `upsert_emergency_contact_sap` tool."""
    # Define test data:
    test_data = {
        "person_id": "103362",
        "email": "test1_ramu@test.com",
        "phone": "6303714329",
        "name": "Ramu",
        "relationship": "5462",
        "response_http_code": 200,
        "primary_flag": "Y",
        "is_primary": True,
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.upsert_emergency_contact_sap.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [{"httpCode": test_data["response_http_code"]}]
        }

        # Update emergency contact
        response = upsert_emergency_contact_sap(
            person_id_external=test_data["person_id"],
            name=test_data["name"],
            email=test_data["email"],
            phone=test_data["phone"],
            relationship=test_data["relationship"],
            is_primary=test_data["is_primary"],
        )

        # Ensure that upsert_emergency_contact_sap() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "PerEmergencyContacts",
                    "type": "SFOData.PerEmergencyContacts",
                },
                "name": test_data["name"],
                "personIdExternal": test_data["person_id"],
                "email": test_data["email"],
                "phone": test_data["phone"],
                "relationship": test_data["relationship"],
                "primaryFlag": test_data["primary_flag"],
            }
        )
