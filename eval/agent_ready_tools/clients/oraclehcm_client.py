# Standard library imports
from typing import Any, Dict, Optional

# Third-party library imports
import requests
from requests.auth import HTTPBasicAuth

from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class OracleHCMClient:
    """A remote client for Oracle HCM."""

    REST_FRAMEWORK_VERSION = "4"

    def __init__(self, base_url: str, username: str, password: str, version: str = "11.13.18.05"):
        """
        Args:
            base_url: The base URL for the Oracle HCM API.
            username: The username to use for authentication against the Oracle HCM API.
            password: The password to use for authentication against the Oracle HCM API.
            version: The version of Oracle HCM API.
        """
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)
        self.version = version

    def get_request(
        self,
        entity: str,
        q_expr: Optional[str] = None,
        expand_expr: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        finder_expr: Optional[str] = None,
        path: Optional[str] = "hcmRestApi",
        params: Optional[Dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Executes a GET request against the provided entity.

        Args:
            entity: The entity to query.
            q_expr: An optional q expression to restrict the results.
            expand_expr: An optional expand expression specifying which fields to expand.
            headers: An optional headers which are required for API request.
            finder_expr: An optional finder expression to search the collection.
            path: An optional path value that is used to called list of values apis.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the Oracle HCM API.
        """
        url = f"{self.base_url}/{path}/resources/{self.version}/{entity}"

        if params is None:
            params = {"links": "self"}
        else:
            params["links"] = "self"

        if q_expr is not None:
            params["q"] = q_expr
        if expand_expr is not None:
            params["expand"] = expand_expr
        if finder_expr is not None:
            params["finder"] = finder_expr
        if headers is None:
            headers = {}

        response = requests.get(url=url, auth=self.auth, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def post_request(
        self,
        entity: str,
        payload: dict[str, Any],
        params: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """
        Executes a generic upsert request against the Oracle HCM API.

        Args:
            entity: The sub-directory entity of the resource to request.
            payload: A dictionary containing the input payload.
            params: A dictionary containing the request params (Optional).
            headers: A dictionary containing the request headers (Optional).

        Returns:
            The JSON response from the Oracle HCM API.
        """

        if headers is None:
            headers = {"REST-Framework-Version": self.REST_FRAMEWORK_VERSION}
        else:
            headers["REST-Framework-Version"] = self.REST_FRAMEWORK_VERSION

        response = requests.post(
            url=f"{self.base_url}/hcmRestApi/resources/{self.version}/{entity}",
            auth=self.auth,
            json=payload,
            headers=headers,
            params=params,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # the oracle error response text is more valuable than 'reason', return if available.
            # response text will contain real reason for failing, such as incorrect zip code format.
            if response.text:
                oracle_error_message = (
                    f"{response.status_code} Server Error: {response.text} for url: {response.url}"
                )
                result: Dict[str, Any] = {}
                result["message"] = oracle_error_message
                result["status_code"] = response.status_code
                return result
            raise e

        result = response.json()
        result["status_code"] = response.status_code
        return result

    def update_request(self, entity: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Executes the update request against the provided entity in Oracle HCM.

        Args:
            entity: The entity to query.
            payload: A dictionary containing the input payload.

        Returns:
            The JSON response from the Oracle HCM API.
        """

        url = f"{self.base_url}/hcmRestApi/resources/{self.version}/{entity}"

        headers = {"Content-Type": "application/json", "effective-Of": "RangeMode=UPDATE"}
        response = requests.patch(url=url, json=payload, auth=self.auth, headers=headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # the oracle error response text is more valuable than 'reason', return if available.
            # response text will contain real reason for failing, such as incorrect zip code format.
            if response.text:
                oracle_error_message = (
                    f"{response.status_code} Server Error: {response.text} for url: {response.url}"
                )
                result: Dict[str, Any] = {}
                result["message"] = oracle_error_message
                result["status_code"] = response.status_code
                return result
            raise e

        result = response.json()
        result["status_code"] = response.status_code
        return result

    def get_response_text(
        self,
        entity: str,
        headers: Optional[Dict[str, str]] = None,
        path: Optional[str] = "hcmRestApi",
    ) -> str:
        """
        Executes a GET request against the provided entity.

        Args:
            entity: The entity to query.
            headers: An optional headers which are required for API request.
            path: An optional path value that is used to called list of values apis.

        Returns:
            The text response from the Oracle HCM API.
        """
        url = f"{self.base_url}/{path}/resources/{self.version}/{entity}"

        if headers is None:
            headers = {}

        response = requests.get(url=url, auth=self.auth, headers=headers)
        response.raise_for_status()
        return response.text


def get_oracle_hcm_client() -> OracleHCMClient:
    """
    Get the oracle hcm client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Returns:
        A new instance of the Oracle HCM client.
    """
    credentials = get_tool_credentials(Systems.ORACLE_HCM)
    oracle_client = OracleHCMClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        username=credentials[CredentialKeys.USERNAME],
        password=credentials[CredentialKeys.PASSWORD],
    )
    return oracle_client
