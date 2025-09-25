from typing import Any, Dict, Optional

import requests

from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems

DEFAULT_SCOPE = "read write"


class ZendeskClient:
    """A remote client for Zendesk."""

    def __init__(
        self,
        base_url: str,
        token_url: str,
        client_id: str,
        client_secret: str,
        scope: Optional[str] = None,
    ):
        """
        Args:
            base_url: The sub domain for the Zendesk API.
            token_url: The URL for authentication tokens for the Zendesk
                API.
            client_id: The client id to authenticate with.
            client_secret: The client secret to authenticate with.
            scope: A list of scopes which is used to get token for API
                requests in Zendesk.
        """
        self.base_url = base_url
        self.token_url = token_url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.client_id = client_id
        self.client_secret = client_secret
        self.bearer = self.get_zendesk_oauth_token(scope=DEFAULT_SCOPE if scope is None else scope)
        self.auth_header = {"Authorization": f"Bearer {self.bearer}"}

    def get_request(
        self,
        entity: str,
        version: str = "v2",
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a GET request against Zendesk API.

        Args:
            entity: The specific entity to make the request against.
            version: The specific version of the API.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the Zendesk REST API.
        """

        response = requests.get(
            url=f"{self.base_url}/api/{version}/{entity}",
            headers=self.auth_header,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def post_request(
        self,
        entity: str,
        version: str = "v2",
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a POST request against Zendesk API.

        Args:
            entity: The specific entity to make the request against.
            version: The specific version of the API.
            params: Query parameters for the REST API.
            payload: The request payload.

        Returns:
            The JSON response from the Zendesk REST API.
        """

        response = requests.post(
            url=f"{self.base_url}/api/{version}/{entity}",
            headers=self.auth_header,
            json=payload,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def put_request(
        self,
        entity: str,
        version: str = "v2",
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a PUT request against Zendesk API.

        Args:
            entity: The specific entity to make the request against.
            version: The specific version of the API.
            params: Query parameters for the REST API.
            payload: The request payload.

        Returns:
            The JSON response from the Zendesk REST API.
        """

        response = requests.put(
            url=f"{self.base_url}/api/{version}/{entity}",
            headers=self.auth_header,
            json=payload,
            params=params,
        )

        response.raise_for_status()
        return response.json()

    def delete_request(
        self,
        entity: str,
        version: str = "v2",
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a DELETE request against Zendesk API.

        Args:
            entity: The specific entity to make the request against.
            version: The specific version of the API.
            params: Query parameters for the REST API.
            payload: The request payload.

        Returns:
            The JSON response from the Zendesk REST API.
        """

        response = requests.delete(
            url=f"{self.base_url}/api/{version}/{entity}",
            headers=self.auth_header,
            json=payload,
            params=params,
        )
        response.raise_for_status()
        result = {}
        if response.content:
            result = response.json()
        else:
            result["status_code"] = response.status_code
        return result

    def patch_request(
        self,
        entity: str,
        version: str = "v2",
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a PATCH request against Zendesk API.

        Args:
            entity: The specific entity to make the request against.
            version: The specific version of the API.
            params: Query parameters for the REST API.
            payload: The request payload.

        Returns:
            The JSON response from the Zendesk REST API.
        """

        response = requests.patch(
            url=f"{self.base_url}/api/{version}/{entity}",
            headers=self.auth_header,
            json=payload,
            params=params,
        )

        response.raise_for_status()
        return response.json()

    def get_zendesk_oauth_token(self, scope: str) -> str:
        """
        The access token generated will expire in 30 mins.

        Args:
            scope: A list of scopes which is used to get token for API
                requests in Zendesk.

        Returns:
            An access token for the specific scope(s).
        """

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": scope,
        }

        response = requests.post(self.token_url, headers=self.headers, data=payload)

        response.raise_for_status()

        access_token = ""

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]

        return access_token


def get_zendesk_client(scope: Optional[str] = None) -> ZendeskClient:
    """
    Get the Zendesk client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Args:
        scope: A list of scopes which is used to get token for API
            requests in Zendesk.

    Returns:
        A new instance of ZendeskClient.
    """
    credentials = get_tool_credentials(Systems.ZENDESK)
    zendesk_client = ZendeskClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        token_url=credentials[CredentialKeys.TOKEN_URL],
        client_id=credentials[CredentialKeys.CLIENT_ID],
        client_secret=credentials[CredentialKeys.CLIENT_SECRET],
        scope=scope,
    )
    return zendesk_client
