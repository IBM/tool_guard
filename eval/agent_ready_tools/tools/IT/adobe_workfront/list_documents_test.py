from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_documents import Documents, list_documents


def test_list_documents() -> None:
    """Verify that the `list_documents` tool can successfully retrieve Adobe workfront documents."""

    # Define test data:
    test_data = {
        "document_id": "63d43ba9000c52db7483c5848069a1e6",
        "document_name": "Web__Geo_Localization_template_-_with_UX_and_design_Exported_Template_Tasks (2)",
        "document_description": "null",
        "object_code": "DOCU",
        "last_update_date": "2023-01-27T16:01:29:557-0500",
    }
    limit = 100
    skip = 1

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_documents.get_adobe_workfront_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["document_id"],
                    "name": test_data["document_name"],
                    "description": test_data["document_description"],
                    "objCode": test_data["object_code"],
                    "lastUpdateDate": test_data["last_update_date"],
                }
            ]
        }
        # Get adobe_workfront documents
        response = list_documents(document_name=test_data["document_name"], skip=1)

        # Ensure that list_documents() executed and returned proper values
        assert response
        expected_data = Documents(
            document_id=test_data["document_id"],
            document_name=test_data["document_name"],
            document_description=test_data["document_description"],
            object_code=test_data["object_code"],
            last_update_date=test_data["last_update_date"],
        )

        assert response.documents[0] == expected_data

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="docu/search",
            params={
                "name": test_data["document_name"],
                "$$LIMIT": limit,
                "$$FIRST": skip,
            },
        )
