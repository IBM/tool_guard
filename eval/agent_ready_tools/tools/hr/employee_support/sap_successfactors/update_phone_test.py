from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_phone import update_phone


def test_update_phone() -> None:
    """Test that a phone can be updated successfully by the `update_phone` tool."""
    # Define test data:
    test_data = {
        "person_id": "100241",
        "phone_number": "+12345678910",
        "phone_type_id": "2214",
        "area_code": "234",
        "country_code": "1",
        "extension": "39",
        "is_primary": False,
        "response_http_code": 200,
        "response_message": "success",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_phone.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [
                {
                    "httpCode": test_data["response_http_code"],
                    "message": test_data["response_message"],
                }
            ]
        }

        # Update user's phone
        response = update_phone(
            area_code=test_data["area_code"],
            country_code=test_data["country_code"],
            extension=test_data["extension"],
            is_primary=test_data["is_primary"],
            person_id_external=test_data["person_id"],
            phone_number=test_data["phone_number"],
            phone_type_id=test_data["phone_type_id"],
        )

        # Ensure that update_phone() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]
        assert response.messages == [test_data["response_message"]]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {"uri": "PerPhone", "type": "SFOData.PerPhone"},
                "areaCode": test_data["area_code"],
                "countryCode": test_data["country_code"],
                "extension": test_data["extension"],
                "isPrimary": test_data["is_primary"],
                "personIdExternal": test_data["person_id"],
                "phoneNumber": test_data["phone_number"],
                "phoneType": test_data["phone_type_id"],
            }
        )
