from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_countries import list_countries
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Country, PickListOptionsPair

_RECORD_TYPE_ID: str = "012000000000000AAA"


def test_list_countries() -> None:
    """Verifies that the `list_countries` tool in Salesforce can successfully retrieve all the
    countries."""

    # Define test data
    test_data = {"country_name": "India", "country_code": "IN"}

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_countries.get_salesforce_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "values": [{"label": test_data["country_name"], "value": test_data["country_code"]}]
        }

        # Call the function
        response = list_countries()

        # Expected response
        expected_response = [
            Country(country_name=test_data["country_name"], country_code=test_data["country_code"])
        ]

        # Verify the response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            PickListOptionsPair.Country.obj_api_name,
            PickListOptionsPair.Country.field_api_name,
            _RECORD_TYPE_ID,
        )
