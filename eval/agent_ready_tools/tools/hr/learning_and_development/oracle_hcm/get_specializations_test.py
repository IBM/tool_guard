from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_specializations import (
    _get_specializations_payload,
    get_specializations,
)
from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.learning_test_bytes import (
    SPECIALIZATION_REPORT_BYTES,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_specializations_with_filter() -> None:
    """Test that the `get_specializations` function returns the expected response."""

    # Define test data:
    test_data = {
        "specialization_number": "OLC103003",
        "specialization_name": "Corporate Compliance Learning",
        "specialization_start_date": "02/05/2017",
        "specialization_end_date": "",
        "section_name": "Anti Bribery and Corruption",
        "section_number": "OLC100377",
        "course_name": "Anti Corruption and Bribery Compliance",
        "course_number": "OLC420032",
        "name": "Corporate Compliance Learning",
        "learning_id": "300000142478293",
        "report_bytes": SPECIALIZATION_REPORT_BYTES,
    }

    # Patch `get_oracle_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_specializations.get_oracle_soap_client"
    ) as mock_oracle_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.get_specializations.return_value = Obj(
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

        # Get specializations
        response = get_specializations(test_data["name"]).specialization_details[0]

        # Ensure that get_specializations() executed and returned proper values
        assert response
        assert response.specialization_number == test_data["specialization_number"]
        assert response.specialization_name == test_data["specialization_name"]
        assert response.specialization_short_description is not None
        assert response.specialization_description is not None
        assert response.specialization_start_date == test_data["specialization_start_date"]
        assert response.section_name == test_data["section_name"]
        assert response.section_number == test_data["section_number"]
        assert response.course_name == test_data["course_name"]
        assert response.course_number == test_data["course_number"]
        assert response.learning_id == test_data["learning_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_specializations.assert_called_once_with(_get_specializations_payload())


def test_get_specializations_without_filter() -> None:
    """Test that the `get_specializations` function returns the expected response."""

    # Define test data:
    test_data = {
        "specialization_number": "OLC103003",
        "specialization_name": "Corporate Compliance Learning",
        "specialization_start_date": "02/05/2017",
        "specialization_end_date": "",
        "section_name": "Anti Bribery and Corruption",
        "section_number": "OLC100377",
        "course_name": "Anti Corruption and Bribery Compliance",
        "course_number": "OLC420032",
        "learning_id": "300000142478293",
        "report_bytes": SPECIALIZATION_REPORT_BYTES,
    }

    # Patch `get_oracle_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_specializations.get_oracle_soap_client"
    ) as mock_oracle_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.get_specializations.return_value = Obj(
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

        # Get specializations
        response = get_specializations().specialization_details[0]

        # Ensure that get_specializations() executed and returned proper values
        assert response
        assert response.specialization_number == test_data["specialization_number"]
        assert response.specialization_name == test_data["specialization_name"]
        assert response.specialization_short_description is not None
        assert response.specialization_description is not None
        assert response.specialization_start_date == test_data["specialization_start_date"]
        assert response.section_name == test_data["section_name"]
        assert response.section_number == test_data["section_number"]
        assert response.course_name == test_data["course_name"]
        assert response.course_number == test_data["course_number"]
        assert response.learning_id == test_data["learning_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_specializations.assert_called_once_with(_get_specializations_payload())
