from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_course_offerings import (
    _get_course_offerings_payload,
    get_course_offerings,
)
from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.learning_test_bytes import (
    COURSE_REPORT_BYTES,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_course_offerings() -> None:
    """Test that the `get_course_offerings` function returns the expected response."""

    # Define test data:
    test_data = {
        "offering_number": "OLC101106",
        "offering_name": "Inspirational Leadership",
        "offering_status": "Active",
        "offering_type": "Self-Paced",
        "offering_dates": "",
        "course_name": "Inspirational Leadership",
        "report_bytes": COURSE_REPORT_BYTES,
    }

    # Patch `get_oracle_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_course_offerings.get_oracle_soap_client"
    ) as mock_oracle_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.get_course_offerings.return_value = Obj(
            {
                "body": {
                    "run_report_response": {
                        "run_report_return": {
                            "report_bytes": test_data["report_bytes"],
                        }
                    }
                }
            }
        )

        # Get offering details
        response = get_course_offerings(test_data["course_name"]).offering_details[0]

        # Ensure that get_course_offerings() executed and returned proper values
        assert response
        assert response.offering_number == test_data["offering_number"]
        assert response.offering_name == test_data["offering_name"]
        assert response.offering_description is not None
        assert response.offering_status == test_data["offering_status"]
        assert response.offering_type == test_data["offering_type"]

        # Ensure the API call was made with expected parameters
        mock_client.get_course_offerings.assert_called_once_with(_get_course_offerings_payload())


def test_get_course_offerings_empty() -> None:
    """Test that the `get_course_offerings` function returns the expected response."""

    # Define test data:
    test_data = {
        "offering_number": "OLC101056",
        "offering_name": "Microsoft Excel 2019",
        "offering_status": "Active",
        "offering_type": "Self-Paced",
        "offering_dates": "",
        "course_name": "Microsoft Excel 2019 - Beginner",
        "report_bytes": COURSE_REPORT_BYTES,
    }

    # Patch `get_oracle_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_course_offerings.get_oracle_soap_client"
    ) as mock_oracle_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.get_course_offerings.return_value = Obj(
            {
                "body": {
                    "run_report_response": {
                        "run_report_return": {
                            "report_bytes": test_data["report_bytes"],
                        }
                    }
                }
            }
        )

        # Get offering details
        response = get_course_offerings(test_data["course_name"])

        # Ensure that get_course_offerings() executed and returned proper values
        assert (
            response
            == "There is no course with 'Microsoft Excel 2019 - Beginner'. Please provide a valid course name."
        )

        # Ensure the API call was made with expected parameters
        mock_client.get_course_offerings.assert_called_once_with(_get_course_offerings_payload())
