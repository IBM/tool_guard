import base64
import json
from typing import Any, Dict, Optional, Union

import requests
from requests.exceptions import RequestException

from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class WatsonCommerceClient:
    """A remote client for WatsonCommerce."""

    def __init__(self, base_url: str, tenant_id: str, client_id: str, client_secret: str):
        """
        Args:
            base_url: The base URL for Watson Commerce API.
            tenant_id: The ID for the tenant.
            client_id: Client ID for Watson Commerce API.
            client_secret: Client secret for Watson Commerce API.
        """
        self.base_url = base_url
        self.tenant_id = tenant_id

        # Base64 encode the credentials
        auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth}",
        }

        payload = {"grant_type": "client_credentials"}
        token_url = f"{self.base_url}/inventory/{tenant_id}/v1/oauth2/token"
        authentication_response = requests.post(url=token_url, data=payload, headers=headers)
        self.bearer_token = authentication_response.json().get("access_token")
        assert self.bearer_token, "Failed to fetch Bearer token for client"

        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def delete_request(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Union[int, Dict[str, Any]]:
        """
        Executes a DELETE request against WatsonCommerce API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.

        Returns:
            HTTP status code on success, or an error dictionary on failure.
        """
        if params is None:
            params = {}

        try:
            response = requests.delete(
                url=f"{self.base_url}/inventory/{self.tenant_id}/{resource_name}",
                headers=self.headers,
                params=json.dumps(params),
            )
            response.raise_for_status()
            return response.status_code
        except RequestException:
            try:
                return response.json()
            except ValueError:
                # Handle the case where response content is not JSON
                return {
                    "errorMessage": response.text,
                    "status_code": response.status_code,
                }

    def patch_request(
        self,
        resource_name: str,
        payload: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a PATCH request against WatsonCommerce API.

        Args:
            resource_name: The specific resource to make the request against.
            payload: The request payload.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the WatsonCommerce REST API.
        """
        if params is None:
            params = {}
        if payload is None:
            payload = {}

        try:
            response = requests.patch(
                url=f"{self.base_url}/inventory/{self.tenant_id}/{resource_name}",
                headers=self.headers,
                params=params,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            try:
                return response.json()
            except ValueError:
                # Handle the case where response content is not JSON
                return {
                    "errorMessage": response.text,
                    "status_code": response.status_code,
                }

    def post_request(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a POST request against WatsonCommerce API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.
            payload: The request payload.
        Returns:
            The JSON response from the WatsonCommerce REST API.
        """
        if params is None:
            params = {}

        try:
            response = requests.post(
                url=f"{self.base_url}/inventory/{self.tenant_id}/{resource_name}",
                headers=self.headers,
                params=params,
                data=json.dumps(payload),
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            try:
                return response.json()
            except ValueError:
                # Handle the case where response content is not JSON
                return {
                    "errorMessage": response.text,
                    "status_code": response.status_code,
                }

    def get_request(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a GET request against WatsonCommerce API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.

        Returns:
            The JSON list response from the WatsonCommerce REST API.
        """
        if params is None:
            params = {}

        try:
            response = requests.get(
                url=f"{self.base_url}/inventory/{self.tenant_id}/{resource_name}",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            try:
                return response.json()
            except ValueError:
                # Handle the case where response content is not JSON
                return {
                    "errorMessage": response.text,
                    "status_code": response.status_code,
                }


def get_watson_commerce_client() -> WatsonCommerceClient:
    """
    Get the WatsonCommerce client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Returns:
        A new instance of the WatsonCommerce client.
    """
    credentials = get_tool_credentials(Systems.WATSON_COMMERCE)
    watson_commerce_client = WatsonCommerceClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        tenant_id=credentials[CredentialKeys.TENANT_ID],
        client_id=credentials[CredentialKeys.CLIENT_ID],
        client_secret=credentials[CredentialKeys.CLIENT_SECRET],
    )
    return watson_commerce_client
