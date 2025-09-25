from typing import Any, Dict, Optional

import msal
import requests

from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class MicrosoftClient:
    """A remote client for Microsoft Graph API."""

    VERSION_1 = "v1.0"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        authority: str,
        base_url: str,
        delegate_mode: bool = False,
    ):
        """
        Args:
            client_id: The Microsoft Entra Application (client) ID.
            client_secret: The Microsoft Entra client secret.
            username: The Microsoft account username (email address).
            password: The Microsoft account password.
            authority: The Microsoft Entra authority URL.
            base_url: The Microsoft Graph API URL.
            delegate_mode: True to indicate the client should use the delegated URL:
                "https://.../me". False to use the impersonation URL: "https://.../users/[user
                email]/...".
        """

        self.base_url = base_url
        self.token_cache = msal.TokenCache()

        self.__username = username
        self.__password = password
        self.__scopes: list[str] = [f"{base_url}/.default"]
        self.__user_resource_path = "me" if delegate_mode else f"users/{username}"

        self.msal_client_app = msal.ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret,
            token_cache=self.token_cache,
        )

        self.token = self.__get_access_token()

    def get_request(
        self,
        endpoint: str,
        version: str = VERSION_1,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Executes a GET request against a Microsoft Graph API.

        Args:
            endpoint: The specific endpoint to make the request against.
            version: The specific version of the API, usually but not limited to "v1.0"
            params: Query parameters for the request.

        Returns:
            The JSON response from the request.
        """

        self.token = self.__get_access_token()

        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(
            url=f"{self.base_url}/{version}/{endpoint}",
            headers=headers,
            params=params,
        )

        response.raise_for_status()
        result = response.json()
        result["status_code"] = response.status_code
        return result

    def post_request(
        self,
        endpoint: str,
        data: dict,
        version: str = VERSION_1,
        headers: Optional[Dict[str, str]] = None,
    ) -> dict[str, Any]:
        """
        Executes a POST request against a Microsoft Graph API.

        Args:
            endpoint: The specific endpoint to make the request against.
            data: The Input data request.
            version: The specific version of the API, usually but not limited to "v1.0"
            headers: The headers value for the request.

        Returns:
            The JSON response from the request.
        """

        self.token = self.__get_access_token()

        if headers is None:
            headers = {"Authorization": f"Bearer {self.token}"}
        else:
            headers["Authorization"] = f"Bearer {self.token}"

        response = requests.post(
            url=f"{self.base_url}/{version}/{endpoint}",
            headers=headers,
            json=data,
        )
        response.raise_for_status()
        result = {}
        if response.content:
            result = response.json()

        result["status_code"] = response.status_code
        return result

    def update_request(self, endpoint: str, data: dict, version: str = VERSION_1) -> dict[str, Any]:
        """
        Executes an update (PATCH) request against the Microsoft Graph API.

        Args:
            endpoint: The specific endpoint to make the request against. The endpoint should contain
                the entity ID to be updated.
            data: A dictionary containing the input payload.
            version: The specific version of the API, usually but not limited to "v1.0"

        Returns:
            The JSON response from the request.
        """

        self.token = self.__get_access_token()

        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.patch(
            url=f"{self.base_url}/{version}/{endpoint}",
            headers=headers,
            json=data,
        )

        response.raise_for_status()
        result = {}
        if response.content:
            result = response.json()
        else:
            result["status_code"] = response.status_code
        return result

    def delete_request(self, endpoint: str, version: str = VERSION_1) -> int:
        """
        Executes a DELETE request against the Microsoft Graph API.

        Args:
            endpoint: The specific endpoint to make the request against. The endpoint should contain
                the entity ID to be deleted.
            version: The specific version of the API, usually but not limited to "v1.0"

        Returns:
            The status code of the request.
        """

        self.token = self.__get_access_token()

        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.delete(url=f"{self.base_url}/{version}/{endpoint}", headers=headers)

        response.raise_for_status()
        return response.status_code

    def put_request(
        self,
        endpoint: str,
        data: Any = None,
        version: str = VERSION_1,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Executes a PUT request against a Microsoft Graph API.

        Args:
            endpoint: Graph endpoint (e.g. "sites/{site_id}/drive/root:/file.txt:/content")
            data: Request body or binary data to send.
            version: API version, default "v1.0".
            headers: Optional headers dict.
            params: Optional query parameters.
        Returns:
            Parsed JSON response plus a "status_code" key.
        """
        self.token = self.__get_access_token()
        if headers is None:
            headers = {"Authorization": f"Bearer {self.token}"}
        else:
            headers["Authorization"] = f"Bearer {self.token}"

        response = requests.put(
            url=f"{self.base_url}/{version}/{endpoint}",
            headers=headers,
            params=params,
            data=data,
        )
        response.raise_for_status()

        result = {}
        if response.content:
            result = response.json()
        result["status_code"] = response.status_code
        return result

    def __get_access_token(self) -> str:
        """
        Returns:
            An access token.
        """

        result = None

        accounts = self.msal_client_app.get_accounts(username=self.__username)

        if accounts:
            result = self.msal_client_app.acquire_token_silent(self.__scopes, account=accounts[0])

        if not result:
            result = self.msal_client_app.acquire_token_for_client(scopes=self.__scopes)

        if "access_token" in result:
            return result["access_token"]

        raise Exception(result)

    def get_user_resource_path(self) -> str:
        """
        Returns the first part of the resource path associated with the MicrosoftClient instance.

        Returns:
            The first part of the resource path.
        """
        return self.__user_resource_path


def get_microsoft_client() -> MicrosoftClient:
    """
    Get the microsoft client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Returns:
        A new instance of the Microsoft client.
    """
    credentials = get_tool_credentials(Systems.MICROSOFT)
    microsoft_client = MicrosoftClient(
        client_id=credentials[CredentialKeys.CLIENT_ID],
        client_secret=credentials[CredentialKeys.CLIENT_SECRET],
        username=credentials[CredentialKeys.USERNAME],
        password=credentials[CredentialKeys.PASSWORD],
        authority=credentials[CredentialKeys.AUTHORITY],
        base_url=credentials[CredentialKeys.BASE_URL],
        delegate_mode=credentials.get(CredentialKeys.DELEGATE_MODE, False),
    )
    return microsoft_client
