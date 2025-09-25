from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.oracle_hcm.get_recruiting_organization import (
    get_recruiting_organizations,
)


def test_get_recruiting_organizations() -> None:
    """Test that the get_recruiting_organization tool function returns the expected response."""

    # Define data
    test_data = {
        "organization_id": 1,
        "organization_name": "corporation",
        "organization_type": "Enterprise",
        "limit": 20,
        "offset": 0,
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.oracle_hcm.get_recruiting_organization.get_oracle_hcm_client"
    ) as mock_oracle_client:

        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "OrganizationId": test_data["organization_id"],
                    "Name": test_data["organization_name"],
                    "Orgtype": test_data["organization_type"],
                }
            ]
        }

        response = get_recruiting_organizations()

        assert response
        assert response.recruiting_organizations[0].organization_id == test_data["organization_id"]
        assert (
            response.recruiting_organizations[0].organization_name == test_data["organization_name"]
        )
        assert (
            response.recruiting_organizations[0].organization_type == test_data["organization_type"]
        )

        mock_client.get_request.assert_called_once_with(
            entity="recruitingOrganizationsLOV",
            params={"limit": test_data["limit"], "offset": test_data["offset"]},
        )
