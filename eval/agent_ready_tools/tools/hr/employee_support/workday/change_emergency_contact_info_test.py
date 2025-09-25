from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.change_emergency_contact_info import (
    _change_emergency_contact_info_payload,
    change_emergency_contact_info,
)
from agent_ready_tools.tools.hr.employee_support.workday.get_workers_emergency_contacts import (
    EmergencyContact,
)


def test_change_emergency_contact_info() -> None:
    """Test that the `change_emergency_contact_info` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "3aa5550b7fe348b98d7b5741afc65534",
        "emergency_contact_reference_wid": "9d0b359e64d74019aec43ff03a4365e8",
        "related_person_relationship_reference": "262f8cd97d424539b1f7d30b9221788a",
        "first_name": "Alice",
        "last_name": "Mcgarvy",
        "phone_number": "4356444463",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.change_emergency_contact_info.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.approve_time_off_and_time_entries.return_value = {
            "body": {
                "change_emergency_contacts_response": {
                    "emergency_contact_event_reference": {
                        "id": [
                            {
                                "value": test_data["emergency_contact_reference_wid"],
                                "type_value=": "WID",
                            }
                        ],
                        "descriptor": None,
                    }
                },
                "version": "v43.2",
            },
            "fault": None,
        }

        # Change emergency contact
        emergency_contact = EmergencyContact(
            emergency_contact_reference_wid=test_data["emergency_contact_reference_wid"],
            related_person_relationship_reference=test_data[
                "related_person_relationship_reference"
            ],
            first_name=test_data["first_name"],
            relationship="Parent",
            last_name=test_data["last_name"],
            phone_number=test_data["phone_number"],
            country_reference="bc33aa3152ec42d4995f4791a106ed09",
            title_wid="c24e65d18f47435e9a3a6b0f7504f01c",
            iso_country_code="USA",
            international_code="1",
            phone_device_type_reference_wid="3014da0ed66f41a3b88085b19175300e",
            usage_data_type_wid="836cf00ef5974ac08b786079866c946f",
        )
        response = change_emergency_contact_info(
            user_id=test_data["user_id"],
            emergency_contact_reference_wid=test_data["emergency_contact_reference_wid"],
            related_person_relationship_reference_id=test_data[
                "related_person_relationship_reference"
            ],
            first_name=test_data["first_name"],
            relationship="Parent",
            last_name=test_data["last_name"],
            phone_number=test_data["phone_number"],
            country_reference="bc33aa3152ec42d4995f4791a106ed09",
            title_wid="c24e65d18f47435e9a3a6b0f7504f01c",
            iso_country_code="USA",
            international_code="1",
            phone_device_type_reference_wid="3014da0ed66f41a3b88085b19175300e",
            usage_data_type_wid="836cf00ef5974ac08b786079866c946f",
            new_relationship=test_data["related_person_relationship_reference"],
            new_first_name=test_data["first_name"],
            new_last_name=test_data["last_name"],
            new_phone_number=test_data["phone_number"],
        )

        # Ensure that change_emergency_contact_info() executed and returned proper values
        assert response
        assert response.id

        # Ensure the API call was made with expected parameters
        mock_client.change_emergency_contact_info.assert_called_once_with(
            _change_emergency_contact_info_payload(
                user_id=test_data["user_id"],
                emergency_contact=emergency_contact,
                relationship=test_data["related_person_relationship_reference"],
                first_name=test_data["first_name"],
                last_name=test_data["last_name"],
                phone_number=test_data["phone_number"],
            )
        )
