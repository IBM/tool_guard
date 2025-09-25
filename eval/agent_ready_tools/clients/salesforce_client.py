import time
from typing import Any, Optional

import jwt
import requests
from simple_salesforce import Salesforce  # type: ignore[attr-defined]

from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class SalesforceClient:
    """A remote client for Salesforce."""

    def __init__(
        self, base_url: str, token_url: str, client_id: str, client_secret: str, domain: str
    ):
        """
        Args:
            base_url: The base URL for the Salesforce API.
            token_url: The URL for authentication tokens for the Coupa API.
            client_id: The client id to authenticate with.
            client_secret: The client id to authenticate with.
            domain: The agent domain
        """
        self.__base_url = base_url
        self.__token_url = token_url
        self.__headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__domain = domain
        self.salesforce_object = Salesforce(
            domain=self.__domain,
            consumer_key=self.__client_id,
            consumer_secret=self.__client_secret,
        )

        self.__expires = None
        self.__token = self.__get_token()

    def post_request(
        self,
        api_version: str,
        resource_name: str,
        payload: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Executes a POST request against Saleforce API.

        Args:
            api_version: Specific api_version.
            resource_name: The specific resource to make the request against.
            payload: The request payload.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the Coupa REST API.
        """

        token = self.__get_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": self.__headers["Accept"],
        }

        response = requests.post(
            url=f"{self.__base_url}/services/data/{api_version}/{resource_name}",
            headers=headers,
            params=params,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    def patch_request(
        self,
        api_version: str,
        resource_name: str,
        payload: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> int:
        """
        Executes a PATCH request against Saleforce API.

        Args:
            api_version: Specific api_version.
            resource_name: The specific resource to make the request against.
            payload: The request payload.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the Coupa REST API.
        """

        token = self.__get_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": self.__headers["Accept"],
        }

        response = requests.patch(
            url=f"{self.__base_url}/services/data/{api_version}/{resource_name}",
            headers=headers,
            params=params,
            json=payload,
        )
        response.raise_for_status()
        return response.status_code

    def delete_request(
        self,
        api_version: str,
        resource_name: str,
        payload: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> int:
        """
        Executes a DELETE request against Saleforce API.

        Args:
            api_version: Specific api_version.
            resource_name: The specific resource to make the request against.
            payload: The request payload.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the Coupa REST API.
        """

        token = self.__get_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": self.__headers["Accept"],
        }

        response = requests.delete(
            url=f"{self.__base_url}/services/data/{api_version}/{resource_name}",
            headers=headers,
            params=params,
            json=payload,
        )
        response.raise_for_status()
        return response.status_code

    def get_request(
        self,
        api_version: str,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Executes a GET request against Saleforce API.

        Args:
            api_version: Specific api_version.
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the Coupa REST API.
        """

        token = self.__get_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": self.__headers["Accept"],
        }

        response = requests.get(
            url=f"{self.__base_url}/services/data/{api_version}/{resource_name}",
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def __get_token(self) -> str:
        """
        Returns:
            The access_token
        """

        if self.__expires is None or time.time() > self.__expires:
            # Prepare the request payload
            payload = {
                "grant_type": "client_credentials",
                "client_id": self.__client_id,
                "client_secret": self.__client_secret,
            }

            # Make the POST request to obtain the token
            response = requests.post(self.__token_url, headers=self.__headers, data=payload)

            response.raise_for_status()

            # Check if the request was successful
            if response.status_code == 200:
                self.__token = response.json()["access_token"]
                self.__expires = jwt.decode(self.__token, options={"verify_signature": False})[
                    "exp"
                ]

        return self.__token

    def get_picklist_options(
        self, object_api_name: str, field_api_name: str, record_type_id: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Gets the picklist options for the specified fields.

        Args:
            object_api_name: The API name of a supported object in Salesforce.
            field_api_name: The API name of the picklist field on the object in Salesforce.
            record_type_id: The record type id of the object API in Salesforce.

        Returns:
            A dictionary representing the picklist options for the specified fields.
        """
        token = self.__get_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": self.__headers["Accept"],
        }
        if not record_type_id:
            record_type_id = (
                requests.get(
                    url=f"{self.__base_url}/services/data/v63.0/ui-api/object-info/{object_api_name}",
                    headers=headers,
                )
                .json()
                .get("defaultRecordTypeId")
            )

        response = requests.get(
            url=f"{self.__base_url}/services/data/v63.0/ui-api/object-info/{object_api_name}/picklist-values/{record_type_id}/{field_api_name}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


def get_salesforce_client() -> SalesforceClient:
    """
    Get the salesforce client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Returns:
        A new instance of Salesforce.
    """
    credentials = get_tool_credentials(Systems.SALESFORCE)
    salesforce_client = SalesforceClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        token_url=credentials[CredentialKeys.TOKEN_URL],
        client_id=credentials[CredentialKeys.CLIENT_ID],
        client_secret=credentials[CredentialKeys.CLIENT_SECRET],
        domain=credentials[CredentialKeys.DOMAIN],
    )
    return salesforce_client
