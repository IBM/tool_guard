from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_ghg_insight_l3 import (
    dnb_get_company_ghg_insight_l3,
)


def test_dnb_get_company_ghg_data_l3() -> None:
    """Test that the `get_company_ghg_data_l3` function returns the expected response."""
    # Define test data:
    test_company_id = "001368083"
    test_data = {
        "company_id": "001368083",
        "climate_score": 78,
        "emissions_score": 72,
        "emission_scope1_volume": 71000.0,
        "emission_scope2_volume": 306000.0,
        "emission_scope3_volume": 143000.0,
        "emission_offset_volume": None,
        "emission_offset_scope": "",
        "emission_neutral_year": "2030",
        "emission_neutral_scopes": "scope 1, scope 2",
        "emission_neutral_type": "net zero",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_ghg_insight_l3.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_data["company_id"],
                "esgRanking": {
                    "environmentalRanking": {
                        "emissionsClimateTopics": {
                            "climateRiskScore": test_data["climate_score"],
                            "ghgEmissionsScore": test_data["emissions_score"],
                        },
                        "ghgEmissionScope1": {
                            "emissionVolume": test_data["emission_scope1_volume"]
                        },
                        "ghgEmissionScope2": {
                            "emissionVolume": test_data["emission_scope2_volume"]
                        },
                        "ghgEmissionScope3": {
                            "emissionVolume": test_data["emission_scope3_volume"]
                        },
                        "emissionOffset": {
                            "offsetVolume": test_data["emission_offset_volume"],
                            "emissionScopes": test_data["emission_offset_scope"],
                        },
                        "emissionNeutralPlan": {
                            "emissionNeutralYear": test_data["emission_neutral_year"],
                            "emissionNeutralScopes": test_data["emission_neutral_scopes"],
                            "emissionNeutralType": test_data["emission_neutral_type"],
                        },
                    },
                },
            },
        }

        # Get purchase by ID
        response = dnb_get_company_ghg_insight_l3(duns_number=test_data["company_id"]).content

        # Ensure that get_company_ghg_data_l3() executed and returned proper values
        assert response.duns_number == test_data["company_id"]
        assert response.climate_score == test_data["climate_score"]
        assert response.emissions_score == test_data["emissions_score"]
        assert response.emission_scope1_volume == test_data["emission_scope1_volume"]
        assert response.emission_scope2_volume == test_data["emission_scope2_volume"]
        assert response.emission_scope3_volume == test_data["emission_scope3_volume"]
        assert response.emission_offset_volume == test_data["emission_offset_volume"]
        assert response.emission_offset_scope == test_data["emission_offset_scope"]
        assert response.emission_neutral_year == test_data["emission_neutral_year"]
        assert response.emission_neutral_scopes == test_data["emission_neutral_scopes"]
        assert response.emission_neutral_type == test_data["emission_neutral_type"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + test_company_id,
            params={"blockIDs": "esginsight_L3_v1"},
        )
