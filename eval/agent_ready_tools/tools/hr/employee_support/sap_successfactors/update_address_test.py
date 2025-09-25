from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_address import (
    update_address,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_update_address() -> None:
    """Test that an address can be updated successfully by the `update_address` tool."""
    # Define test data:
    test_data = {
        "person_id": "100241",
        "start_date": "2025-11-11",
        "zip_code": "30-120",
        "city": "Krakow",
        "country": "PL",
        "address_type": "home",
        "response_http_code": 200,
        "response_message": "updated successfully",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_address.get_sap_successfactors_client"
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

        # Update user address
        response = update_address(
            address_type=test_data["address_type"],
            person_id_external=test_data["person_id"],
            country=test_data["country"],
            city=test_data["city"],
            start_date=test_data["start_date"],
            zip_code=test_data["zip_code"],
        )

        # Ensure that update_address() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]
        assert response.message == test_data["response_message"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {"uri": "PerAddressDEFLT", "type": "SFOData.PerAddressDEFLT"},
                "addressType": test_data["address_type"],
                "country": test_data["country"],
                "personIdExternal": test_data["person_id"],
                "city": test_data["city"],
                "startDate": iso_8601_to_sap_date(str(test_data["start_date"])),
                "zipCode": test_data["zip_code"],
            }
        )


def test_update_address_error() -> None:
    """Test that an address can be updated successfully by the `update_address` tool."""
    # Define test data:
    test_data = {
        "person_id": "100241",
        "start_date": "2025-11-11",
        "zip_code": "30-120",
        "city": "Krakow",
        "country": "PL",
        "address_type": "home",
        "response_http_code": 500,
        "response_message": "Invalid zip code value",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.sap_successfactors.update_address.get_sap_successfactors_client"
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

        # Update user address
        response = update_address(
            address_type=test_data["address_type"],
            person_id_external=test_data["person_id"],
            country=test_data["country"],
            city=test_data["city"],
            start_date=test_data["start_date"],
            zip_code=test_data["zip_code"],
        )

        # Ensure that update_address() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]
        assert response.message == test_data["response_message"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {"uri": "PerAddressDEFLT", "type": "SFOData.PerAddressDEFLT"},
                "addressType": test_data["address_type"],
                "country": test_data["country"],
                "personIdExternal": test_data["person_id"],
                "city": test_data["city"],
                "startDate": iso_8601_to_sap_date(str(test_data["start_date"])),
                "zipCode": test_data["zip_code"],
            }
        )
