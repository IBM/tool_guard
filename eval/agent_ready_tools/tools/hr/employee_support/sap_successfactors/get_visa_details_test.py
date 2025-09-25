from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_visa_details import (
    get_visa_details,
)


def test_get_visa_details() -> None:
    """Test that all visa details can be retrieved successfully for a given user."""
    # Define test data:
    test_data = {
        "user_id": "100173",
        "country": "44",
        "document_number": "DF112345DD",
        "document_title": "Visa 1010",
        "document_type": "9944",
        "expiration_date": "2026-03-04",
        "is_validated": True,
        "issue_date": "2025-03-04",
        "issue_place": "Beijing",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.get_visa_details.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "country": test_data["country"],
                        "documentNumber": test_data["document_number"],
                        "documentTitle": test_data["document_title"],
                        "documentType": test_data["document_type"],
                        "expirationDate": test_data["expiration_date"],
                        "isValidated": test_data["is_validated"],
                        "issueDate": test_data["issue_date"],
                        "issuePlace": test_data["issue_place"],
                    }
                ]
            }
        }

        # Get visa Details
        response = get_visa_details(user_id=test_data["user_id"])
        # Ensure that get_visa_details() executed and returned proper values
        assert response
        assert len(response.visa_details)
        assert response.visa_details[0].document_number == test_data["document_number"]
        assert response.visa_details[0].document_title == test_data["document_title"]
        assert response.visa_details[0].document_type == test_data["document_type"]
        assert response.visa_details[0].is_validated == test_data["is_validated"]
        assert response.visa_details[0].issue_date == test_data["issue_date"]
        assert response.visa_details[0].issue_place == test_data["issue_place"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="EmpWorkPermit", filter_expr=f"userId eq '{test_data['user_id']}'"
        )
