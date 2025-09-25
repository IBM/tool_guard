from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_model import get_model


def test_get_model() -> None:
    """Test that models can be retrieved successfully."""

    # Define test data:
    test_data = {
        "id": "1c1788c287e03300693331a2f5cb0bec",
        "display_name": "Apple iPhone X",
        "model_number": "IPHONE5",
        "model_type": "Generic",
        "model_category": "218323293743100044e0bfc8bcbe5d61",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_model.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "display_name": test_data["display_name"],
                    "model_number": test_data["model_number"],
                    "type": test_data["model_type"],
                    "cmdb_model_category": test_data["model_category"],
                },
            ],
        }

        # Get device models
        response = get_model(model_category_system_id=test_data["model_category"])

        # Ensure that get_model() executed and returned proper values
        assert response
        assert len(response.models)
        assert response.models[0].system_id == test_data["id"]
        assert response.models[0].model_name == test_data["display_name"]
        assert response.models[0].model_number == test_data["model_number"]
        assert response.models[0].model_type == test_data["model_type"]
        assert response.models[0].model_category == test_data["model_category"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="cmdb_model", params={"cmdb_model_category": test_data["model_category"]}
        )
