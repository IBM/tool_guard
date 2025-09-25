from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_emails_ids import get_emails_ids


def test_get_emails_ids() -> None:
    """Verifies that get_emails_ids returns the correct output."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D9424C4C740000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000196D664000078",
        "email_id": 300000282955174,
        "email_address": "Kavya.Sri.Thabeti@partner.ibm.com",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_emails_ids.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "EmailAddressId": test_data["email_id"],
                    "EmailAddress": test_data["email_address"],
                },
            ]
        }

        # Get email IDs
        response = get_emails_ids(test_data["worker_id"])

        # Ensure that get_emails_ids() got executed properly and returned proper values
        assert response
        assert len(response.emails_ids)
        assert response.emails_ids[0].email_id == test_data["email_id"]
        assert response.emails_ids[0].email_address == test_data["email_address"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f'workers/{test_data["worker_id"]}/child/emails'
        )
