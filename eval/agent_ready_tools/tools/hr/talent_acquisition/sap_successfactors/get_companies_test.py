from typing import Any, Dict
from unittest.mock import patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_companies import (
    sap_get_companies,
)


def test_sap_get_companies() -> None:
    """Tests that the `sap_get_companies` function returns the expected response."""

    test_data: Dict[str, Any] = {
        "external_code": "4000",
        "name": "BestRun India",
        "top": 5,
        "skip": 0,
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_companies.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = mock_sap_client.return_value

        # Mock response from SAP SuccessFactors client
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "externalCode": test_data["external_code"],
                        "name": test_data["name"],
                    }
                ]
            }
        }

        # Call the tool with test input
        response = sap_get_companies(company_name="BestRun India", limit=5, skip=0)

        # Validate response
        assert response
        company = response.companies[0]
        assert company.external_code == test_data["external_code"]
        assert company.name == test_data["name"]

        # Validate underlying API call
        mock_client.get_request.assert_called_once_with(
            entity="FOCompany",
            filter_expr=f"name eq '{test_data['name']}'",
            params={
                "$select": "externalCode,name",
                "$top": test_data["top"],
                "$skip": test_data["skip"],
            },
        )
