import http
import time
from typing import Any, Optional

import requests

from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class BoxClient:
    """A remote client for Box API."""

    def __init__(
        self,
        base_url: str,
        token_url: str,
        subject_id: str,
        subject_type: str,
        client_id: str,
        client_secret: str,
    ):
        """
        Args:
            base_url: The base URL for the Box API.
            token_url: The URL for authentication tokens for the Box API.
            subject_id: The subject ID for authentication.
            subject_type: The subject type for authentication.
            client_id: The client ID for authentication.
            client_secret: The client secret for authentication.

        Returns:
            None
        """
        self.box_base_url = base_url
        self.token_url = token_url
        self.subject_id = subject_id
        self.subject_type = subject_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.__get_box_access_token()

    def get_request(
        self, entity: str, params: Optional[dict[str, Any]] = None, content: Optional[bool] = False
    ) -> dict[str, Any]:
        """
        Executes a GET request against a Box API.

        Args:
            entity (str): The entity to retrieve from the Box API.
            params (dict[str, Any], optional): The parameters to include in the GET request. Defaults to None.
            content (bool): This is optional parameter to retrieve the file content as text. Defaults to False.

        Returns:
            dict[str, Any]: The JSON response from the Box API.

        Raises:
            requests.exceptions.HTTPError: If the request returns an error status code.
        """
        if self.__is_token_expired():
            self.__get_box_access_token()

        headers = {"Authorization": f"Bearer {self.auth['token']}", "Accept": "application/json"}
        url = self.__build_url(entity)
        response = requests.get(
            url=url,
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        if content:
            return {"content": response.text}
        return response.json()

    def post_request(
        self,
        entity: str,
        data: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, Any]] = None,
        api_type: str = "api",
    ) -> dict[str, Any]:
        """
        Executes a POST request against a Box API.

        Args:
            entity (str): The entity path for the request (e.g., "files/content").
            data (dict[str, Any], optional): The data to include in the POST request. Defaults to None.
            files (dict[str, Any], optional): The files to upload. Defaults to None.
            api_type (str, optional): The API type to use ("api" or "upload"). Defaults to "api".

        Returns:
            dict[str, Any]: The JSON response from the Box API.

        Raises:
            requests.exceptions.HTTPError: If the request returns an error status code.
        """
        if self.__is_token_expired():
            self.__get_box_access_token()

        headers = {"Authorization": f"Bearer {self.auth['token']}", "Accept": "application/json"}
        url = self.__build_url(entity, api_type)

        response = requests.post(
            url=url,
            headers=headers,
            json=data,
            files=files,
        )
        if response.status_code != http.HTTPStatus.CONFLICT.value:
            response.raise_for_status()
        result = response.json()
        result["status_code"] = response.status_code
        return result

    def put_request(
        self,
        entity: str,
        data: Optional[dict[str, Any]] = None,
        api_type: str = "api",
    ) -> dict[str, Any]:
        """
        Executes a PUT request against a Box API.

        Args:
            entity (str): The entity path for the request (e.g., "folders/4353455").
            data (dict[str, Any], optional): The data to include in the PUT request. Defaults to None.
            api_type (str, optional): The API type to use ("api" or "upload"). Defaults to "api".

        Returns:
            dict[str, Any]: The JSON response from the Box API.

        Raises:
            requests.exceptions.HTTPError: If the request returns an error status code.
        """
        if self.__is_token_expired():
            self.__get_box_access_token()

        headers = {"Authorization": f"Bearer {self.auth['token']}", "Accept": "application/json"}
        url = self.__build_url(entity, api_type)

        response = requests.put(
            url=url,
            headers=headers,
            json=data,
        )
        response.raise_for_status()
        return response.json()

    def delete_request(
        self, entity: str, params: Optional[dict[str, Any]] = None, api_type: str = "api"
    ) -> int:
        """
        Executes a DELETE request against a Box API.

        Args:
            entity (str): The entity path for the request (e.g., "folders/4353455").
            params (dict[str, Any], optional): The parameters to include in the DELETE request. Defaults to None.
            api_type (str, optional): The API type to use ("api" or "upload"). Defaults to "api".

        Returns:
            int: The status code of the response if there is no content, otherwise the JSON response from the Box API.

        Raises:
            requests.exceptions.HTTPError: If the request returns an error status code.
        """
        if self.__is_token_expired():
            self.__get_box_access_token()

        headers = {"Authorization": f"Bearer {self.auth['token']}", "Accept": "application/json"}
        url = self.__build_url(entity, api_type)

        response = requests.delete(
            url=url,
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return response.status_code

    def __get_box_access_token(self) -> dict[str, Any]:
        """
        Get an access token from Box API.

        Returns:
            A dictionary containing the access token and its expiration time.
        """

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "box_subject_type": self.subject_type,
            "box_subject_id": self.subject_id,
        }

        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        result = response.json()

        self.auth = {
            "token": result["access_token"],
            "expires": time.time() + result["expires_in"],
        }

        return result

    def __is_token_expired(self) -> bool:
        """
        Check if the token is expired.

        Returns:
            True if the token is expired, False otherwise.
        """
        if self.auth is None:
            return True

        return time.time() > self.auth["expires"]

    def __build_url(self, entity: str, api_type: str = "api") -> str:
        """
        Build the appropriate URL for Box API requests.

        Args:
            entity (str): The entity path for the request.
            api_type (str): The API type to use ("api" or "upload"). Defaults to "api".

        Returns:
            str: The fully constructed URL.
        """
        if api_type == "upload":
            return f"https://upload.{self.box_base_url}/api/2.0/{entity}"
        return f"https://api.{self.box_base_url}/2.0/{entity}"


def get_box_client() -> BoxClient:
    """
    Get the box client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Returns:
        A new instance of the Box client.
    """
    credentials = get_tool_credentials(Systems.BOX)
    box_client = BoxClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        token_url=credentials[CredentialKeys.TOKEN_URL],
        subject_id=credentials[CredentialKeys.SUBJECT_ID],
        subject_type=credentials[CredentialKeys.SUBJECT_TYPE],
        client_id=credentials[CredentialKeys.CLIENT_ID],
        client_secret=credentials[CredentialKeys.CLIENT_SECRET],
    )
    return box_client
