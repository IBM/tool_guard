from unittest.mock import MagicMock, call, patch

from agent_ready_tools.tools.sales.sales_research.dnb.get_company_info import (
    CompanyInfoResponse,
    get_company_info,
)


def test_get_company_info_single_duns() -> None:
    """Test that the `get_company_info` function returns the expected response for a single duns."""

    # Define test data:
    test_data = {
        "duns_number": "804735132",
        "name": "International Business Machines Corporation",
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.get_company_info.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "primaryName": test_data["name"],
            },
        }

        # Get company info
        input_duns = test_data["duns_number"]
        response = get_company_info(duns_number=input_duns)

        # Ensure that get_company_info() executed and returned proper values
        assert isinstance(response[0], CompanyInfoResponse)
        assert response[0].name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            version="v1",
            category="data",
            endpoint="duns",
            path_parameter=test_data["duns_number"],
            params={"blockIDs": "companyinfo_L2_v1"},
        )


def test_get_company_info_multiple_duns() -> None:
    """Test that the `get_company_info` function returns the expected response for multiple duns."""

    # Define test data:
    test_data = {
        "duns_1": "804735132",
        "duns_2": "804735133",
        "duns_3": "804735134",
        "name_1": "International Business Machines Corporation",
        "name_2": "Foo",
        "name_3": "Bar",
    }
    # Use "'" quote format to match external tool output
    test_data["duns_number"] = (
        f"['{test_data["duns_1"]}', '{test_data["duns_2"]}', '{test_data["duns_3"]}']"
    )

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sales_research.dnb.get_company_info.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client

        # Mock the multiple return values to the get requests
        mock_get_request = MagicMock()
        mock_get_request.side_effect = [
            {
                "organization": {
                    "primaryName": test_data["name_1"],
                },
            },
            {
                "organization": {
                    "primaryName": test_data["name_2"],
                },
            },
            {
                "organization": {
                    "primaryName": test_data["name_3"],
                },
            },
        ]
        mock_client.get_request = mock_get_request

        # Get company info
        input_duns = test_data["duns_number"]
        response = get_company_info(duns_number=input_duns)

        # Ensure that get_company_info() executed and returned proper values
        assert isinstance(response[0], CompanyInfoResponse)
        assert response[0].name == test_data["name_1"]
        assert response[1].name == test_data["name_2"]
        assert response[2].name == test_data["name_3"]

        # Ensure the API call was made with expected parameters
        mock_client.assert_has_calls(
            [
                call.get_request(
                    version="v1",
                    category="data",
                    endpoint="duns",
                    path_parameter=test_data["duns_1"],
                    params={"blockIDs": "companyinfo_L2_v1"},
                ),
                call.get_request(
                    version="v1",
                    category="data",
                    endpoint="duns",
                    path_parameter=test_data["duns_2"],
                    params={"blockIDs": "companyinfo_L2_v1"},
                ),
                call.get_request(
                    version="v1",
                    category="data",
                    endpoint="duns",
                    path_parameter=test_data["duns_3"],
                    params={"blockIDs": "companyinfo_L2_v1"},
                ),
            ]
        )
