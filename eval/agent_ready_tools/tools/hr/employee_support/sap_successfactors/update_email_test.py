from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_email import update_email


def test_update_email() -> None:
    """Test that an email can be updated successfully by the `update_email` tool."""
    # Define test data:
    test_data = {
        "person_id": "109031",
        "email_address": "test@example.com",
        "email_type_id": "8448",
        "is_primary": True,
        "response_http_code": 200,
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_email.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [{"httpCode": test_data["response_http_code"], "message": ""}]
        }
        # Simulate that there is no existing primary email
        mock_client.get_request.return_value = {"d": {"results": []}}

        # Update user's email
        response = update_email(
            person_id_external=test_data["person_id"],
            email_address=test_data["email_address"],
            email_type_id=test_data["email_type_id"],
            is_primary=test_data["is_primary"],
        )

        # Ensure that update_email() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {"uri": "PerEmail", "type": "SFOData.PerEmail"},
                "personIdExternal": test_data["person_id"],
                "emailType": test_data["email_type_id"],
                "emailAddress": test_data["email_address"],
                "isPrimary": test_data["is_primary"],
            }
        )
