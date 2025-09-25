from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_workers_emergency_contacts import (
    _get_workers_emergency_contact_payload,
    get_workers_emergency_contacts,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_workers_emergency_contacts() -> None:
    """Test that the `get_workers_emergency_contacts` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "3aa5550b7fe348b98d7b5741afc65534",
        "first_name": "Alice",
        "relation": "Parent",
        "relation_id": "262f8cd97d424539b1f7d30b9221788a",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_workers_emergency_contacts.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_related_person_relationships.return_value = Obj(
            {
                "body": {
                    "get_related_person_relationships_response": {
                        "response_data": {
                            "related_person_relationship": [
                                Obj(
                                    {
                                        "related_person_relationship_reference": {
                                            "id": [Obj({"value": test_data["relation_id"]})]
                                        },
                                        "related_person_relationship_data": [
                                            Obj({"relationship_name": test_data["relation"]})
                                        ],
                                    }
                                )
                            ]
                        }
                    },
                },
            }
        )

        mock_client.get_workers_emergency_contact.return_value = Obj(
            {
                "body": {
                    "get_workers_response": {
                        "response_data": {
                            "worker": [
                                Obj(
                                    {
                                        "worker_data": {
                                            "related_person_data": {
                                                "related_person": [
                                                    Obj(
                                                        {
                                                            "emergency_contact": {
                                                                "emergency_contact_reference": {
                                                                    "id": [
                                                                        Obj(
                                                                            {
                                                                                "value": test_data[
                                                                                    "user_id"
                                                                                ],
                                                                            }
                                                                        )
                                                                    ]
                                                                }
                                                            },
                                                            "related_person_relationship_reference": [
                                                                Obj(
                                                                    {
                                                                        "id": [
                                                                            Obj(
                                                                                {
                                                                                    "value": "262f8cd97d424539b1f7d30b9221788a",
                                                                                }
                                                                            )
                                                                        ]
                                                                    }
                                                                )
                                                            ],
                                                            "personal_data": {
                                                                "name_data": {
                                                                    "legal_name_data": {
                                                                        "name_detail_data": {
                                                                            "first_name": test_data[
                                                                                "first_name"
                                                                            ],
                                                                            "last_name": "Smith",
                                                                            "country_reference": {
                                                                                "id": [
                                                                                    Obj(
                                                                                        {
                                                                                            "value": "1329d1s1h8s12321s2",
                                                                                        }
                                                                                    )
                                                                                ]
                                                                            },
                                                                            "prefix_data": {
                                                                                "title_reference": {
                                                                                    "id": [
                                                                                        Obj(
                                                                                            {
                                                                                                "value": "9u1982u31w1172w1",
                                                                                            }
                                                                                        )
                                                                                    ]
                                                                                }
                                                                            },
                                                                        }
                                                                    }
                                                                },
                                                                "contact_data": {
                                                                    "phone_data": [
                                                                        Obj(
                                                                            {
                                                                                "country_iso_code": "USA",
                                                                                "international_phone_code": "+1",
                                                                                "phone_number": "1234567890",
                                                                                "phone_device_type_reference": {
                                                                                    "id": [
                                                                                        Obj(
                                                                                            {
                                                                                                "value": "2319du19ud1232d1ds",
                                                                                            }
                                                                                        )
                                                                                    ]
                                                                                },
                                                                                "usage_data": [
                                                                                    Obj(
                                                                                        {
                                                                                            "type_data": [
                                                                                                Obj(
                                                                                                    {
                                                                                                        "type_reference": {
                                                                                                            "id": [
                                                                                                                Obj(
                                                                                                                    {
                                                                                                                        "value": "231221s1",
                                                                                                                    }
                                                                                                                )
                                                                                                            ]
                                                                                                        }
                                                                                                    }
                                                                                                )
                                                                                            ]
                                                                                        }
                                                                                    )
                                                                                ],
                                                                            }
                                                                        )
                                                                    ]
                                                                },
                                                            },
                                                        }
                                                    )
                                                ]
                                            }
                                        },
                                    }
                                )
                            ]
                        }
                    },
                },
            }
        )

        # Get worker's emergency contact
        response = get_workers_emergency_contacts(user_id=test_data["user_id"])

        # Ensure that get_workers_emergency_contacts() executed and returned proper values
        assert response
        assert response.emergency_contacts[0].first_name == "Alice"
        assert response.emergency_contacts[0].relationship == "Parent"

        # Ensure the API call was made with expected parameters
        mock_client.get_workers_emergency_contact.assert_called_once_with(
            _get_workers_emergency_contact_payload(user_id=test_data["user_id"])
        )
