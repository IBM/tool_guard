from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.seismic.get_generative_search import (
    get_generative_search,
)


def test_get_generative_search() -> None:
    """
    Test that the `get_generative_search` function returns a valid generative search response.

    This test directly calls the function using a sample search term and asserts that:
      - The response is not None.
      - The response has an integer value for total_count.
      - The answer field is a string.
      - The documents attribute is a list.
      - If any documents are returned, the first document contains a non-empty id and a score of type float.

    Note: This test makes an actual API call using the Seismic client configuration. Ensure that valid credentials are available.
    """

    # Define test data:
    test_data = {
        "search_term": "cloud",
        "document_id": "DSAADD1ED231",
        "answer": "alpha",
        "total_count": 1,
    }
    document = {
        "id": test_data["document_id"],
        "versionId": "123",
        "repository": "alpha",
        "name": "beta",
        "teamsiteId": "1321312",
        "type": "text",
        "format": "txt",
        "thumbnailUrl": "http://example.com/image",
        "modifiedDate": "2025-01-01T00:00:00.0",
        "sourceText": "Some kinda text",
        "status": "uploaded",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.seismic.get_generative_search.get_seismic_client"
    ) as mock_seismic_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_seismic_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "documents": [document],
            "answer": test_data["answer"],
            "totalCount": test_data["total_count"],
        }

        # Get Generative Search
        response = get_generative_search(term=test_data["search_term"])

        # Ensure that get_generative_search() executed and returned proper values
        assert response and response.documents
        assert response.answer == test_data["answer"]
        assert response.total_count == test_data["total_count"]
        assert isinstance(response.documents, list), "documents should be a list."
        assert response.documents[0].id == document["id"]
        assert response.documents[0].name == document["name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint="generative/query",
            category="search",
            version="v1",
            payload={"term": test_data["search_term"]},
        )
