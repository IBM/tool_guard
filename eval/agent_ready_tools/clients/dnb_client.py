import base64
import json
from typing import Any, Optional

import requests

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class DNBClient:
    """A remote client for DNB."""

    def __init__(self, base_url: str, token_url: str, client_id: str, client_secret: str):
        """
        Args:
            base_url: The base URL for the DNB API.
            token_url: The URL for authentication tokens for the DNB API.
            client_id: Client ID for DNB API.
            client_secret: Client secret for DNB API.
        """
        self.base_url = base_url
        # Combine client_id and client_secret with a colon and encode to bytes
        credentials_string = f"{client_id}:{client_secret}"
        credentials_bytes = credentials_string.encode("utf-8")

        # Base64 encode the credentials
        encoded_credentials_bytes = base64.b64encode(credentials_bytes)
        encoded_credentials_string = encoded_credentials_bytes.decode("utf-8")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials_string}",
        }

        data = {"grant_type": "client_credentials", "scope": "read,write"}
        authentication_response = requests.post(url=token_url, data=data, headers=headers)
        self.bearer_token = authentication_response.json().get("access_token")
        assert self.bearer_token, "Failed to fetch Bearer token for DNB client"

    def get_request(
        self,
        version: str,
        category: str,
        endpoint: Optional[str] = None,
        path_parameter: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Executes a GET request against a DnB API.

        Args:
            version: The specific version of the API, like "v1".
            category: The specific category of the API, like "search".
            endpoint: The specific endpoint to make the request against, like "competitors".
            path_parameter: The path parameter for the REST API.
            params: The Query parameters for the REST API.

        Returns:
            The JSON response from the DnB REST API.
        """
        get_headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}/{version}/{category}"
        if endpoint:
            url += f"/{endpoint}"
        if path_parameter:
            url += f"/{path_parameter}"
        try:
            response = requests.get(
                url=url,
                headers=get_headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            # We still want to return the json blob of the HTTP error message to the tool code
            # This is so that we can output the error message on the agent UI
            try:
                return response.json()
            except ValueError:
                # Handle the case where response content is not JSON
                return {
                    "error": {
                        "errorMessage": "Non-JSON response",
                        "status_code": response.status_code,
                    }
                }

    def post_request(
        self,
        endpoint: str,
        category: str,
        data: dict,
        version: str,
    ) -> dict[str, Any]:
        """
        Executes a POST request against a DnB API.

        Args:
            endpoint: The specific endpoint to make the request against, like "criteria".
            category: The specific category of the API, like "search".
            data: The Input data request.
            version: The specific version of the API, like "v1".

        Returns:
            The JSON response from the DnB REST API.
        """
        post_headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                url=f"{self.base_url}/{version}/{category}/{endpoint}",
                headers=post_headers,
                data=json.dumps(data),
            )
            return response.json()
        except requests.exceptions.HTTPError:
            # We still want to return the json blob of the HTTP error message to the tool code
            # This is so that we can output the error message on the agent UI
            # Example 1: DnB uses 404 for no results returned by search, we want to surface this
            # Example 2: DnB uses 429 for API request error (API limit reached)
            try:
                return response.json()
            except ValueError:
                # Handle the case where response content is not JSON
                return {
                    "error": {
                        "errorMessage": "Non-JSON response",
                        "status_code": response.status_code,
                    }
                }


def get_dnb_client(entitlement: DNBEntitlements) -> DNBClient:
    """
    Get the dnb client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Args:
        entitlement: the credential entitlement (e.g. sales, procurement)

    Returns:
        A new instance of the DnB client.
    """
    credentials = get_tool_credentials(Systems.DNB, sub_category=entitlement)
    dnb_client = DNBClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        client_id=credentials[CredentialKeys.CLIENT_ID],
        token_url=credentials[CredentialKeys.TOKEN_URL],
        client_secret=credentials[CredentialKeys.CLIENT_SECRET],
    )
    return dnb_client
