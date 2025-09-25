from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_principals_l1 import (
    dnb_get_company_principals_l1,
)


def test_dnb_get_company_principals_l1() -> None:
    """Test that the `get_company_principals_l1` function returns the expected response."""

    # Define test data:
    test_job_titles: list[dict[str, str]] = [{"title": "Chief Executive Officer"}]
    test_data = {
        "company_id": "001368083",
        "name": "Brohammad",
        "job_titles": test_job_titles,
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_principals_l1.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_data["company_id"],
                "mostSeniorPrincipals": [
                    {
                        "fullName": test_data["name"],
                        "jobTitles": test_data["job_titles"],
                    },
                ],
            },
        }

        # Get purchase by ID
        response = dnb_get_company_principals_l1(duns_number=test_data["company_id"]).content
        # breakpoint()
        # Ensure that get_company_ceo executed and returned proper values
        assert response
        assert response.duns_number == test_data["company_id"]
        assert len(response.principals) == 1
        assert response.principals[0].name == test_data["name"]

        # assert response.titles == test_data["jobTitles"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + str(test_data["company_id"]),
            params={"blockIDs": "principalscontacts_L1_v1"},
        )
