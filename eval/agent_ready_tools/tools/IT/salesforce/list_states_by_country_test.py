from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_states_by_country import list_states_by_country
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import PickListOptionsPair


def test_list_states() -> None:
    """Test that retrieves all the states successfully by the `list_states_by_country` tool."""
    # Define test data:
    test_data = {"state": "Delhi", "country_code": "IN", "country_value": "99"}

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_states_by_country.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client

        # Mock the response for get_picklist_options
        mock_client.get_picklist_options.return_value = {
            "controllerValues": {test_data["country_code"]: test_data["country_value"]},
            "values": [{"label": test_data["state"], "validFor": test_data["country_value"]}],
        }

        # Get states
        response = list_states_by_country(test_data["country_code"])
        expected = test_data["state"]

        # Assert the expected and actual response
        assert response
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_any_call(
            PickListOptionsPair.Contact.obj_api_name, PickListOptionsPair.Contact.field_api_name
        )
