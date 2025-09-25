from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.update_organization import update_organization


def test_update_organization() -> None:
    """Verifies that the `update_organization` tool can successfully update an organization in
    Zendesk."""

    # Define test data
    test_data = {"notes": "Something interesting", "organization_id": "6288314909081"}

    # Patch the Zendesk client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.update_organization.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.patch_request.return_value = {
            "organization": {"id": test_data["organization_id"]}
        }

        # Update an organization
        response = update_organization(
            organization_id=test_data["organization_id"], notes=test_data["notes"]
        )

        # Ensure that update_organization() executed and returned proper values
        assert response
        assert response.organization_id == test_data["organization_id"]

        # Ensure API call was made with correct payload
        mock_client.patch_request.assert_called_once_with(
            entity=f"organizations/{test_data['organization_id']}",
            payload={"organization": {"notes": test_data["notes"]}},
        )
