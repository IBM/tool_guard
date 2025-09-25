from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_personal_information import (
    update_personal_information,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_update_personal_information() -> None:
    """Test that the personal information can be updated successfully by the
    `update_personal_information` tool."""
    # Define test data:
    test_data = {
        "person_id": "100241",
        "name": "Nicole Amenta",
        "start_date": "2025-07-10",
        "response_http_code": 200,
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_personal_information.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [{"httpCode": test_data["response_http_code"]}]
        }

        # Update user's personal information
        response = update_personal_information(
            person_id_external=test_data["person_id"],
            preferred_name=test_data["name"],
            start_date=test_data["start_date"],
        )

        # Ensure that update_personal_information() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {"uri": "PerPersonal", "type": "SFOData.PerPersonal"},
                "personIdExternal": test_data["person_id"],
                "preferredName": test_data["name"],
                "startDate": iso_8601_to_sap_date(str(test_data["start_date"])),
            }
        )
