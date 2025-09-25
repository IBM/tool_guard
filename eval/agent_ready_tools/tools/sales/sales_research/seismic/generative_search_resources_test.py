from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sales_research.seismic.generative_search_resources import (
    get_generative_search_sources,
)


def test_get_generative_search_sources() -> None:
    """
    Test that the `get_generative_search_sources` function returns a valid generative search sources
    response.

    This test directly calls the function using a sample search term and asserts that:
      - The response is not None.
      - The response has integer values for query_time_in_ms, service_time_in_ms, and total_count.
      - The documents attribute is a list.
      - If any documents are returned, the first document contains a non-empty id and a score of type float.
    """

    # Define test data:
    test_data = {
        "search_term": "sample search",
        "search_size": 10,
        "document_id": "DSAADD1ED231",
        "query_time_in_ms": 20,
        "service_time_in_ms": 20,
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
        "agent_ready_tools.tools.sales.sales_research.seismic.generative_search_resources.get_seismic_client"
    ) as mock_seismic_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_seismic_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "documents": [document],
            "queryTimeInMs": test_data["query_time_in_ms"],
            "serviceTimeInMs": test_data["service_time_in_ms"],
            "totalCount": test_data["total_count"],
        }

        # Get Generative Search Sources
        response = get_generative_search_sources(
            term=test_data["search_term"], size=test_data["search_size"]
        )

        # Ensure that get_generative_search_sources() executed and returned proper values
        assert response, "Response should not be None."
        assert response.query_time_in_ms == test_data["query_time_in_ms"]
        assert response.service_time_in_ms == test_data["service_time_in_ms"]
        assert response.total_count == test_data["total_count"]

        assert len(response.documents) == response.total_count
        assert response.documents[0].id == document["id"]
        assert response.documents[0].name == document["name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            endpoint="generative",
            category="search",
            version="v1",
            custom_path_suffix="source",
            payload={"term": test_data["search_term"], "size": test_data["search_size"]},
        )
