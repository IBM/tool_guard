from typing import Any, Dict
from unittest.mock import patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_states import (
    search_states,
)


def test_search_states() -> None:
    """Test that the `search_states` function returns the expected company list."""

    test_data: Dict[str, Any] = {
        "picklist_id": "3982",
        "state": "telangana",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_states.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = mock_sap_client.return_value

        # Mock response from SAP SuccessFactors client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "label": test_data["state"],
                        "picklistOption": {
                            "id": test_data["picklist_id"],
                            "externalCode": "telangana",
                            "picklist": {"picklistId": "state"},
                        },
                    }
                ]
            }
        }

        # Call the tool with test input
        response = search_states(state="telangana").options[0]

        # Validate response
        assert response
        assert response.picklist_id == test_data["picklist_id"]
        assert response.state == test_data["state"]

        # Validate underlying API call
        mock_client.get_request.assert_called_once_with(
            entity="PicklistLabel",
            params={
                "$top": 10,
                "$skip": 0,
            },
            filter_expr=f"picklistOption/picklist/picklistId eq 'state' and locale eq 'en_US' and label eq '{test_data["state"]}'",
            select_expr="label,picklistOption/id",
            expand_expr="picklistOption/picklist",
        )
