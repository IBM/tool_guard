# Standard library imports
from typing import Any, Dict, Optional

# Third-party library imports
import requests
from requests.auth import HTTPBasicAuth

from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class JiraClient:
    """A remote client for Jira."""

    def __init__(self, base_url: str, username: str, password: str, version: Optional[int] = 3):
        """
        Args:
            base_url: The base URL for the Jira API.
            username: The username to use for authentication against the Jira API.
            password: The password to use for authentication against the Jira API.
            version: The version of Jira API.
        """
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)
        self.version = version

    def get_request(
        self,
        entity: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Executes a GET request against the provided entity.

        Args:
            entity: The entity to query.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the Jira API.
        """
        url = f"{self.base_url}/rest/api/{self.version}/{entity}"

        response = requests.get(url=url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json()

    def post_request(
        self,
        entity: str,
        payload: dict[str, Any],
        headers: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """
        Executes a generic post request against the Jira API.

        Args:
            entity: The entity to query.
            payload: A dictionary containing the input payload.
            headers: A dictionary containing the request headers (Optional).

        Returns:
            The JSON response from the Jira API.
        """

        response = requests.post(
            url=f"{self.base_url}/rest/api/{self.version}/{entity}",
            auth=self.auth,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        result = response.json()
        result["status_code"] = response.status_code
        return result

    def update_request(self, entity: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Executes the update request against the provided entity in Jira API.

        Args:
            entity: The entity to query.
            payload: A dictionary containing the input payload.

        Returns:
            The JSON response from the Jira API.
        """

        url = f"{self.base_url}/rest/api/{self.version}/{entity}"

        response = requests.patch(url=url, json=payload, auth=self.auth)
        response.raise_for_status()
        result = response.json()
        result["status_code"] = response.status_code
        return result

    def delete_request(self, entity: str, payload: Optional[dict[str, Any]] = None) -> int:
        """
        Executes a generic delete request against the Jira API.

        Args:
            entity: The entity to query.
            payload: A dictionary containing the input payload.

        Returns:
            The status code of the request
        """
        response = requests.delete(
            url=f"{self.base_url}/rest/api/{self.version}/{entity}", auth=self.auth, json=payload
        )
        response.raise_for_status()
        return response.status_code

    def put_request(self, entity: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Executes the put request against the provided entity in Jira API.

        Args:
            entity: The entity to query.
            payload: A dictionary containing the input payload.

        Returns:
            The JSON response from the Jira API.
        """

        url = f"{self.base_url}/rest/api/{self.version}/{entity}"

        response = requests.put(url=url, json=payload, auth=self.auth)
        response.raise_for_status()
        result = {}
        if response.content:
            result = response.json()
        else:
            result["status_code"] = response.status_code
        return result


def get_jira_client() -> JiraClient:
    """
    Get the jira client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!
    To test, either mock this call or call the client directly.

    Returns:
        A new instance of JiraClient.
    """

    credentials = get_tool_credentials(system=Systems.JIRA)
    jira_client = JiraClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        username=credentials[CredentialKeys.USERNAME],
        password=credentials[CredentialKeys.PASSWORD],
    )
    return jira_client
