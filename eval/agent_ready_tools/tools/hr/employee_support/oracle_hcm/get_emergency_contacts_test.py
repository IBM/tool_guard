from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_emergency_contacts import (
    get_emergency_contacts,
)


def test_get_emergency_contacts() -> None:
    """Test that the `get_emergency_contacts` function returns the expected response."""

    # Define test data:
    test_data = {
        "contact_id": "00020000000EACED00057708000110D94234EACA0000004AAC",
        "contact_relationship_id": 300000281422542,
        "name": "Rajan",
        "contact_type": "BROTHER",
        "related_person_id": "100000610892530",
        "related_person_id_int": 100000610892530,
        "related_person_number": "6198",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_emergency_contacts.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "names": {"items": [{"DisplayName": test_data["name"]}]},
                    "contactRelationships": {
                        "items": [
                            {
                                "ContactRelationshipId": test_data["contact_relationship_id"],
                                "ContactType": test_data["contact_type"],
                                "RelatedPersonId": test_data["related_person_id"],
                                "RelatedPersonNumber": test_data["related_person_number"],
                            }
                        ]
                    },
                    "links": [
                        {
                            "href": f"example.com/{test_data['related_person_id']}/child/{test_data['contact_id']}",
                        }
                    ],
                }
            ]
        }

        # Get emergency contacts
        response = get_emergency_contacts(person_id=test_data["related_person_id"])

        # Ensure that get_emergency_contacts() executed and returned proper values
        assert response
        assert len(response.emergency_contacts)
        assert response.emergency_contacts[0].contact_id == test_data["contact_id"]
        assert (
            response.emergency_contacts[0].contact_relationship_id
            == test_data["contact_relationship_id"]
        )
        assert response.emergency_contacts[0].name == test_data["name"]
        assert response.emergency_contacts[0].contact_type == test_data["contact_type"]
        assert (
            response.emergency_contacts[0].related_person_id == test_data["related_person_id_int"]
        )
        assert (
            response.emergency_contacts[0].related_person_number
            == test_data["related_person_number"]
        )

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "hcmContacts",
            finder_expr=f"findContactsByWorker;RelatedPersonId={test_data['related_person_id']}",
            expand_expr="contactRelationships,names,phones,emails,addresses",
            q_expr="contactRelationships.EmergencyContactFlag=true",
            headers={"REST-Framework-Version": "4"},
        )
