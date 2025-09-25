import json
from typing import Dict, Optional
from urllib.parse import urlencode

from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse


def process_dnb_error(response: Dict, api_url: str, url_params: Optional[Dict]) -> ErrorResponse:
    """
    Checks the response of a D&B API call and processes the response if we see an error.

    Args:
        response: the api response json object
        api_url: the api being called
        url_params: optional parameters associated with the api call

    Returns:
        An ErrorResponse object that the LLM can interpret
    """
    # Check for a special case where get industry profile returns "empty list", but technically it doesn't return HTTP Error from the API
    # Returns True if we are using "https://plus.dnb.com/v1/industryprofile" and the profiles list is empty
    flag_industry_profile_empty_list = bool(
        api_url == "https://plus.dnb.com/v1/industryprofile" and not response.get("profiles", None)
    )

    if "error" in response or flag_industry_profile_empty_list:

        # If url_params is None or empty, then just use api_url, else add the url_params to end of api_url
        if not url_params or not isinstance(url_params, Dict):
            request_url = api_url
        else:
            request_params = urlencode(url_params)
            request_url = f"{api_url}?{request_params}"
        response["request_url"] = request_url

        # When get industry profile returns "empty list", there is no error object, so need to manually build it
        if (
            api_url == "https://plus.dnb.com/v1/industryprofile"
            and flag_industry_profile_empty_list
        ):
            error_message = "No data returned for get industry profile"
            error_code = 99999
        else:
            error_code = response["error"]["errorCode"]
            error_message = response["error"]["errorMessage"]

        return ErrorResponse(
            message=error_message,
            payload=json.dumps(response),
            status_code=error_code,
        )
    else:
        return ErrorResponse(message="No Error", payload=json.dumps(response), status_code=200)
