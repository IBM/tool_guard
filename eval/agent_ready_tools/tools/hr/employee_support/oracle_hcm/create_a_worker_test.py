from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_a_worker import create_a_worker


def test_create_a_worker() -> None:
    """Test that a worker was created successfully by the `create_a_worker` tool."""

    # Define test data:
    test_data = {
        "first_name": "John",
        "last_name": "Smith",
        "date_of_birth": "1980-01-01",
        "legal_employer_name": "India Legal Entity",
        "country_code": "US",
        "action_code": "HIRE",
        "business_unit_name": "India Business Unit",
        "email": "agentv1test1@ibm.com",
        "email_type": "W1",
        "phone": "8974839827",
        "phone_type": "W1",
        "http_code": 201,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_a_worker.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        # Create a Worker
        response = create_a_worker(
            employee_first_name=test_data["first_name"],
            employee_last_name=test_data["last_name"],
            date_of_birth=test_data["date_of_birth"],
            legal_employer_name=test_data["legal_employer_name"],
            country_code=test_data["country_code"],
            business_unit_name=test_data["business_unit_name"],
            employee_email_address=test_data["email"],
            employee_phone_number=test_data["phone_type"],
            action_code=test_data["action_code"],
        )

        # Ensure that create_a_worker() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="workers",
            payload={
                "names": [
                    {
                        "FirstName": test_data["first_name"],
                        "LastName": test_data["last_name"],
                        "LegislationCode": test_data["country_code"],
                    }
                ],
                "DateOfBirth": test_data["date_of_birth"],
                "workRelationships": [
                    {
                        "LegalEmployerName": test_data["legal_employer_name"],
                        "assignments": [
                            {
                                "ActionCode": test_data["action_code"],
                                "BusinessUnitName": test_data["business_unit_name"],
                            }
                        ],
                    }
                ],
                "emails": [
                    {"EmailAddress": test_data["email"], "EmailType": test_data["email_type"]}
                ],
                "phones": [
                    {"PhoneNumber": test_data["phone_type"], "PhoneType": test_data["phone_type"]}
                ],
            },
        )
