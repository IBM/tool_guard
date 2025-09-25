from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_recruiting_template_details import (
    get_recruiting_template_details,
    get_template_value,
)


def test_get_recruiting_template_details_success() -> None:
    """Test that the `get_recruiting_template_details` function returns the expected response."""
    # Define test data:
    test_data = {
        "template_name": "Basic Job Requisition",
        "message": "[{id=1141, name=Basic Job Requisition, description=null, locale=null}]",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_recruiting_template_details.get_sap_successfactors_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "d": {"getRecruitingTemplate": test_data["message"]}
        }

        response = get_recruiting_template_details(
            template_name=test_data["template_name"],
        )

        # Assertions
        assert response
        assert response.template_id == "1141"
        assert response.template_name == "Basic Job Requisition"
        assert response.description == "null"

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="getRecruitingTemplate",
            params={"templateType": "JOBREQ", "templateName": f"'{test_data['template_name']}'"},
        )


def test_get_template_value() -> None:
    """Test that the `get_template_value` function extracts the correct value from the message
    string."""
    test_data = {
        "message": "[{id=1141, name=Basic Job Requisition, description=null, locale=null}]",
        "key_name": "id",
        "expected_value": "1141",
    }

    response = get_template_value(message=test_data["message"], key_name=test_data["key_name"])

    # Assertions
    assert response == test_data["expected_value"]
