from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_ta_utility import (
    get_country_code,
)


def test_get_country_code() -> None:
    """Tests that the `get_country_code` function returns the expected response."""
    # Define test data:
    test_data: Dict[str, Any] = {"country": "india", "id": "1234"}

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_ta_utility.get_sap_successfactors_client"
    ) as mock_sap_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_response = {"d": {"results": [{"picklistOption": {"id": test_data["id"]}}]}}

        mock_client.get_request.return_value = mock_response
        mock_sap_client.return_value = mock_client

        response = get_country_code(test_data["country"])

        # Ensure that get_country_code() executed and returned proper values
        assert response
        assert response == test_data["id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="PicklistLabel",
            filter_expr=f"picklistOption/picklist/picklistId eq 'country' and locale eq 'en_US' and label eq '{test_data["country"]}'",
            expand_expr="picklistOption/picklist",
            select_expr="label,picklistOption/id,picklistOption/externalCode",
        )
