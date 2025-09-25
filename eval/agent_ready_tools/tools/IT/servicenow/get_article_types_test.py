from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_article_types import get_article_types


def test_get_article_types() -> None:
    """Test that the `get_article_types`  function returns the expected response."""

    # Define test data:
    test_data = {"article_type_1": "wiki"}

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_article_types.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {"result": [{"value": test_data["article_type_1"]}]}

        # Get articles types
        response = get_article_types()

        # Ensure that get_article_types() executed and returned proper values
        assert response
        assert len(response.articletypes)
        assert response.articletypes[0].article_type == test_data["article_type_1"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "kb_knowledge", "element": "article_type"}
        )
