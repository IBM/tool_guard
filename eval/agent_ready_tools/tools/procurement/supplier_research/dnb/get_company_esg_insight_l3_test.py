from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_esg_insight_l3 import (
    dnb_get_company_esg_insight_l3,
)


def test_dnb_get_company_esg_insight_l3() -> None:
    """Test that the `get_company_esg_insight_l3` function returns the expected response."""

    # Define test data:
    test_data = {
        "company_id": "001368083",
        "score": "9999",
        "indicator": "SSX",
        "hs": "100",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_esg_insight_l3.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_data["company_id"],
                "esgRanking": {
                    "score": test_data["score"],
                    "dataDepth": {"indicator": test_data["indicator"]},
                    "socialRanking": {
                        "humanCapitalTopics": {
                            "healthSafetyScore": "100",
                            "humanRightsAbusesScore": "1",
                            "diversityInclusionScore": "3",
                            "laborRelationsScore": "2",
                        },
                    },
                },
            },
        }

        # Get purchase by ID
        response = dnb_get_company_esg_insight_l3(duns_number=test_data["company_id"]).content
        # breakpoint()
        # Ensure that get_company_esg_insight_l3() executed and returned proper values
        assert response
        assert response.duns_number == test_data["company_id"]
        assert response.esg_score == test_data["score"]
        assert response.esg_ranking == test_data["indicator"]
        assert response.health_safety_score == "100"
        assert response.human_rights_abuses_score == "1"
        assert response.labor_relations_score == "2"
        assert response.diversity_inclusion_score == "3"

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + test_data["company_id"],
            params={"blockIDs": "esginsight_L3_v1"},
        )
