from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_asset_types import (
    AssetTypes,
    AssetTypesResponse,
    get_asset_types,
)


def test_get_asset_types() -> None:
    """Test that the `get_asset_types`  function returns the expected response."""

    # Define test data:
    test_data = {"asset_type_name": "alm_license", "label": "Software License"}

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_asset_types.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [{"name": test_data["asset_type_name"], "label": test_data["label"]}]
        }

        # Get asset types
        response = get_asset_types(label=test_data["label"])

        # Ensure that get_asset_types() executed and returned proper values
        assert response

        assert response == AssetTypesResponse(
            asset_types=[AssetTypes(asset_type_name="alm_license", label="Software License")]
        )

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_db_object",
            params={
                "sysparm_query": "nameINalm_hardware,alm_consumable,alm_license,alm_facility,ORDERBYDESCsys_created_on",
                "label": test_data["label"],
            },
        )
