from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_passport_and_visa_info import (
    _get_passport_and_visa_info_payload,
    get_passport_and_visa_info,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_passport_and_visa_info() -> None:
    """Test that the `get_passport_and_visa_info` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "3aa5550b7fe348b98d7b5741afc65534",
        "passport_id": "039845814",
        "passport_issue_country": "USA",
        "passport_issue_date": "1999-01-18",
        "passport_expiry_date": "2009-01-18",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_passport_and_visa_info.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_change_passports_and_visas.return_value = Obj(
            {
                "body": {
                    "get_change_passports_and_visas_response": {
                        "response_data": [
                            Obj(
                                {
                                    "change_passports_and_visas": [
                                        Obj(
                                            {
                                                "change_passports_and_visas_data": [
                                                    Obj(
                                                        {
                                                            "person_reference": {
                                                                "id": [
                                                                    Obj(
                                                                        {
                                                                            "type_value": "WID",
                                                                            "value": test_data[
                                                                                "user_id"
                                                                            ],
                                                                        }
                                                                    )
                                                                ]
                                                            },
                                                            "passports_and_visas_identification_data": {
                                                                "passport_id": [
                                                                    Obj(
                                                                        {
                                                                            "passport_id_data": {
                                                                                "id": test_data[
                                                                                    "passport_id"
                                                                                ],
                                                                                "country_reference": {
                                                                                    "id": [
                                                                                        Obj(
                                                                                            {
                                                                                                "type_value": "ISO_3166-1_Alpha-3_Code",
                                                                                                "value": test_data[
                                                                                                    "passport_issue_country"
                                                                                                ],
                                                                                            }
                                                                                        )
                                                                                    ]
                                                                                },
                                                                                "issued_date": test_data[
                                                                                    "passport_issue_date"
                                                                                ],
                                                                                "expiration_date": test_data[
                                                                                    "passport_expiry_date"
                                                                                ],
                                                                            }
                                                                        }
                                                                    )
                                                                ]
                                                            },
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

        # Get Employee passport and visa
        response = get_passport_and_visa_info(test_data["user_id"])

        # Ensure that get_current_compensation_details() executed and returned proper values
        assert response
        assert response.user_id == test_data["user_id"]
        assert response.passport_id == test_data["passport_id"]
        assert response.passport_issue_country == test_data["passport_issue_country"]
        assert response.passport_issue_date == test_data["passport_issue_date"]
        assert response.passport_expiry_date == test_data["passport_expiry_date"]

        # Ensure the API call was made with expected parameters
        mock_client.get_change_passports_and_visas.assert_called_once_with(
            _get_passport_and_visa_info_payload(user_id=test_data["user_id"])
        )
