from datetime import datetime, timedelta
from typing import Dict

from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_utils import process_dnb_error


def test_process_dnb_error() -> None:
    """Verifies that the `process_dnb_error` function will return ErrorResponse object."""
    duggal_duns = "001815794"
    example_response: Dict = {
        "transactionDetail": {
            "transactionID": "e3000556-1f69-4a79-9aab-0c2642fceac838400",
            "transactionTimestamp": "2025-07-09T19:05:11.937Z",
            "inLanguage": "en-US",
            "productID": "namstd",
            "productVersion": "v1",
        },
        "error": {
            "errorCode": "40105",
            "errorMessage": "Requested product not available due to insufficient data.",
        },
        "inquiryDetail": {
            "duns": "001815794",
            "startDate": "2025-04-10",
            "productID": "namstd",
            "productVersion": "v1",
        },
    }
    expected_payload: Dict = {
        "transactionDetail": {
            "transactionID": "e3000556-1f69-4a79-9aab-0c2642fceac838400",
            "transactionTimestamp": "2025-07-09T19:05:11.937Z",
            "inLanguage": "en-US",
            "productID": "namstd",
            "productVersion": "v1",
        },
        "error": {
            "errorCode": "40105",
            "errorMessage": "Requested product not available due to insufficient data.",
        },
        "inquiryDetail": {
            "duns": "001815794",
            "startDate": "2025-04-10",
            "productID": "namstd",
            "productVersion": "v1",
        },
        "request_url": "https://plus.dnb.com/v1/newsandmedia?duns=001815794&productId=namstd&versionId=v1&startDate=2025-04-11",
    }
    example_query_parameters = {
        "duns": duggal_duns,
        "productId": "namstd",  # Product ID for the News and Media, Standard API.
        "versionId": "v1",
        "startDate": (datetime.now().date() - timedelta(days=float(90))).isoformat(),
    }

    example_api_url = "https://plus.dnb.com/v1/newsandmedia"
    example_url_params = example_query_parameters
    result_error_response = process_dnb_error(example_response, example_api_url, example_url_params)
    expected_error_response = ErrorResponse(
        message="Requested product not available due to insufficient data.",
        payload=expected_payload,
        status_code=40105,
    )

    # Run Unit Tests to check that the error message is the same
    assert result_error_response.message == expected_error_response.message
    assert result_error_response.status_code == expected_error_response.status_code
