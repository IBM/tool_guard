from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_diversity_insight_l1 import (
    dnb_get_diversity_insight_l1,
)


def test_dnb_get_diversity_insight_l1() -> None:
    """Test that the `get_diversity_insight_l1` function returns the expected response."""

    # Define test data:
    test_company_id = "001368083"
    test_data = {
        "is_8A_certified_business": None,
        "is_woman_owned": None,
        "is_minority_owned": None,
        "is_veteran_owned": None,
        "is_vietnam_veteran_owned": None,
        "ownership_ethnicity_type_description": "",
        "ownership_ethnicity_type_dnb_code": None,
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_diversity_insight_l1.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_company_id,
                "socioEconomicInformation": {
                    "is8ACertifiedBusiness": test_data["is_8A_certified_business"],
                    "isWomanOwned": test_data["is_woman_owned"],
                    "isMinorityOwned": test_data["is_minority_owned"],
                    "isVeteranOwned": test_data["is_veteran_owned"],
                    "isVietnamVeteranOwned": test_data["is_vietnam_veteran_owned"],
                    "ownershipPrimaryEthnicityType": {
                        "description": test_data["ownership_ethnicity_type_description"],
                        "dnbCode": test_data["ownership_ethnicity_type_dnb_code"],
                    },
                },
            },
        }

        # Get purchase by ID
        response = dnb_get_diversity_insight_l1(duns_number=test_company_id).content

        # Ensure that get_diversity_insight_l1() executed and returned proper values
        assert response
        assert response.duns_number == test_company_id
        assert response.is_eight_a_certification == test_data["is_8A_certified_business"]
        assert response.is_minority_owned == test_data["is_woman_owned"]
        assert response.is_women_owned == test_data["is_minority_owned"]
        assert response.is_veteran_owned == test_data["is_veteran_owned"]
        assert response.is_vietnam_veteran_owned == test_data["is_vietnam_veteran_owned"]
        assert response.ethnicity_type == test_data["ownership_ethnicity_type_description"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + test_company_id,
            params={"blockIDs": "diversityinsight_L1_v1"},
        )
