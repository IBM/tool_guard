from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.create_organization import create_organization


def test_create_organization() -> None:
    """Verifies that the `create_organization` tool can successfully create an organization in
    Zendesk."""

    # Define test data
    test_data = {"organization": {"organization_name": "My org", "domain_name": []}}

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.create_organization.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "organization": {
                "name": test_data["organization"]["organization_name"],
            }
        }

        # Create an organization
        response = create_organization(
            organization_name=test_data["organization"]["organization_name"]
        )

        # Ensure that create_organization() executed and returned proper values
        assert response
        assert response.organization_name == test_data["organization"]["organization_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="organizations",
            payload={
                "organization": {
                    "name": test_data["organization"]["organization_name"],
                }
            },
        )


def test_create_organization_name_and_domains() -> None:
    """Verifies that the `create_organization` tool can successfully creates an organization in
    Zendesk."""

    # Define test data
    test_data = {
        "organization": {"organization_name": "My org", "domain_name": "@gmail.com,@fit.com"}
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.create_organization.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "organization": {
                "name": test_data["organization"]["organization_name"],
            }
        }

        # Create an organization
        response = create_organization(
            organization_name=test_data["organization"]["organization_name"],
            domain_name=test_data["organization"]["domain_name"],
        )

        # Ensure that create_organization() executed and returned proper values
        assert response
        assert response.organization_name == test_data["organization"]["organization_name"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="organizations",
            payload={
                "organization": {
                    "name": test_data["organization"]["organization_name"],
                    "domain_names": test_data["organization"]["domain_name"].split(","),
                }
            },
        )
