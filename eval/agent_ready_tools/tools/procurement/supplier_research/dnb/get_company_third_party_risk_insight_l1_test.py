from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_third_party_risk_insight_l1 import (
    dnb_get_company_third_party_risk_insight_l1,
)


def test_dnb_get_company_third_party_risk_insight_l1() -> None:
    """Test that the `get_company_third_party_risk_insight_l1 function returns the expected
    response."""

    # Define test data:
    test_company_id = "001368083"
    test_evaluation: Dict[str, Any] = {
        "rawScore": 1.0,
        "scoreCommentary": [
            {"description": "Proportion of slow payment experiences", "dnbCode": 26172}
        ],
    }
    test_stability: Dict[str, Any] = {
        "classScore": 1,
        "failureRate": 0.19,
        "scoreCardID": "US03MFIN",
        "scoreCommentary": [
            {"description": "High proportion of payment experiences", "dnbCode": 33333}
        ],
        "scoreDate": "2024-12-14",
        "scoreModel": {"description": "Supplier Stability Indicator"},
    }
    test_data: Dict[str, Any] = {
        "supplierEvaluationRiskScore": test_evaluation,
        "supplierStabilityIndexScore": test_stability,
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_third_party_risk_insight_l1.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_company_id,
                "thirdPartyRiskAssessment": test_data,
            }
        }

        # Get Company insight by third party risk L1
        response = dnb_get_company_third_party_risk_insight_l1(duns_number=test_company_id).content

        # Ensure that get_company_third_party_risk_insight_l1() executed and returned proper values
        assert response
        assert response.duns_number == test_company_id
        assert response.stability_class_score == test_stability["classScore"]
        assert response.stability_failure_rate == test_stability["failureRate"]
        assert response.stability_score_card_id == test_stability["scoreCardID"]
        assert response.stability_score_date == test_stability["scoreDate"]
        assert response.stability_score_model == test_stability["scoreModel"]["description"]
        assert (
            response.stability_commentary_descriptions
            == test_stability["scoreCommentary"][0]["description"]
        )
        assert response.evaluation_raw_score == test_evaluation["rawScore"]
        assert (
            response.evaluation_commentary_descriptions
            == test_evaluation["scoreCommentary"][0]["description"]
        )

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + test_company_id,
            params={"blockIDs": "thirdpartyriskinsight_L1_v4"},
        )
