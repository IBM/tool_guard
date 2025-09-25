from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_beneficial_ownership_insight_l2 import (
    dnb_get_beneficial_ownership_insight_l2,
)


def test_dnb_get_beneficial_ownership_insight_l2() -> None:
    """Test that the `get_company_financial_insight_l3` function returns the expected response."""

    # Define test data:
    test_company_id = "804735132"
    test_data = {
        "beneficialOwnersCount": 150,
        "relationshipsCount": 100,
        "maximumDegreeOfSeparation": 10,
        "totalAllocatedOwnershipPercentage": 90,
        "organizationsCount": 9,
        "individualsCount": 10010,
        "corporateBeneficiariesCount": 200,
        "stateOwnedOrganizationsCount": 5,
        "govermentOrganiztionsCount": 4,
        "publiclyTradingOrganizationsCount": 15,
        "privatelyHeldOrganizationsCount": 200,
        "pscUniqueTypeCount": 13,
        "countryWisePSCSummary": 14,
        "countryUnknownPSCCount": 15,
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_beneficial_ownership_insight_l2.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_company_id,
                "beneficialOwnershipSummary": test_data,
            }
        }

        # Get company beneficial ownership insight L2
        response = dnb_get_beneficial_ownership_insight_l2(duns_number=test_company_id).content

        # Ensure that get_beneficial_ownership_insight_l2() executed and returned proper values
        assert response
        assert response.duns_number == test_company_id
        assert response.beneficial_owners_count == test_data["beneficialOwnersCount"]
        assert response.relationships_count == test_data["relationshipsCount"]
        assert response.maximum_degree_of_separation == test_data["maximumDegreeOfSeparation"]
        assert (
            response.total_allocated_ownership_percentage
            == test_data["totalAllocatedOwnershipPercentage"]
        )
        assert response.organizations_count == test_data["organizationsCount"]
        assert response.individuals_count == test_data["individualsCount"]
        assert response.corporate_beneficiaries_count == test_data["corporateBeneficiariesCount"]
        assert response.state_owned_organizations_count == test_data["stateOwnedOrganizationsCount"]
        assert response.government_organizations_count == test_data["govermentOrganiztionsCount"]
        assert (
            response.publicly_trading_organizations_count
            == test_data["publiclyTradingOrganizationsCount"]
        )
        assert (
            response.privately_held_organizations_count
            == test_data["privatelyHeldOrganizationsCount"]
        )
        assert response.psc_unique_type_count == test_data["pscUniqueTypeCount"]
        assert response.country_wise_psc_summary == test_data["countryWisePSCSummary"]
        assert response.country_unknown_psc_count == test_data["countryUnknownPSCCount"]

        # Ensure the API call was made with expected parameters
        params = {
            "ownershipType": "BENF_OWRP",
            "productId": "cmpbol",
            "versionId": "v1",
            "duns": test_company_id,
        }

        mock_client.get_request.assert_called_once_with(
            "v1",
            "beneficialowner",
            params=params,
        )
