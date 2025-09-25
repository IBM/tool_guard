from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.create_learning_content import (
    LearningStatus,
    LearningTrackingType,
    create_learning_content,
)


def test_create_learning_content_pdf_or_weblink() -> None:
    """Test that a learning content was created successfully by the `create_learning_content`
    tool."""

    # Define test data:
    test_data = {
        "title": "Testweblink123test",
        "file_name": "Testweblink123test",
        "description": "Testweblink123test",
        "item_number": "Testweblink123test",
        "tracking_type": "WEBLINK",
        "url": "https://docs.oracle.com/en/cloud/saas/human-resources/25a/farws/Uploading_Learning_Content.html",
        "status": "ACTIVE",
        "start_date": "2025-01-15",
        "end_date": "2025-12-14",
        "http_code": 201,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.create_learning_content.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        # Create learning content
        response = create_learning_content(
            title=test_data["title"],
            file_name=test_data["file_name"],
            description=test_data["description"],
            item_number=test_data["item_number"],
            tracking_type=test_data["tracking_type"],
            status=test_data["status"],
            url=test_data["url"],
            start_date=test_data["start_date"],
            end_date=test_data["end_date"],
        )

        # Ensure that create_learning_content() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="learningContentItems",
            payload={
                "Title": test_data["title"],
                "FileName": test_data["file_name"],
                "ItemNumber": test_data["item_number"],
                "TrackingType": LearningTrackingType[str(test_data["tracking_type"])].value,
                "URL": test_data["url"],
                "StartDate": test_data["start_date"],
                "EndDate": test_data["end_date"],
                "Status": LearningStatus[str(test_data["status"])].value,
                "Description": test_data["description"],
            },
        )


def test_create_learning_content() -> None:
    """Test that a learning content was created successfully by the `create_learning_content`
    tool."""

    # Define test data:
    test_data = {
        "title": "Testvideo123test",
        "file_name": "Testvideo123test.mov",
        "description": "Testvideo123test",
        "item_number": "Testvideo123test",
        "tracking_type": "VIDEO",
        "start_date": "2025-01-15",
        "end_date": "2025-12-14",
        "http_code": 201,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.create_learning_content.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        # Create learning content
        response = create_learning_content(
            title=test_data["title"],
            file_name=test_data["file_name"],
            description=test_data["description"],
            item_number=test_data["item_number"],
            tracking_type=test_data["tracking_type"],
            start_date=test_data["start_date"],
            end_date=test_data["end_date"],
        )

        # Ensure that create_learning_content() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="learningContentItems",
            payload={
                "Title": test_data["title"],
                "FileName": test_data["file_name"],
                "Description": test_data["description"],
                "ItemNumber": test_data["item_number"],
                "TrackingType": LearningTrackingType[str(test_data["tracking_type"])].value,
                "StartDate": test_data["start_date"],
                "EndDate": test_data["end_date"],
            },
        )
