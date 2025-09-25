from typing import Any, Optional

import requests
from requests.auth import HTTPBasicAuth

from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class SAPSuccessFactorsClient:
    """A remote client for SAP SuccessFactors."""

    def __init__(self, base_url: str, username: str, password: str):
        """
        Args:
            base_url: The base URL for the SAP SuccessFactors API.
            username: The username to use for authentication against the SAP SuccessFactors API.
            password: The password to use for authentication against the SAP SuccessFactors API.
        """
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)

    def get_picklist_options(self, picklist_field: str) -> dict[str, Any]:
        """
        Gets the picklist options for the specified field.

        Args:
            picklist_field: The name of the picklist field.

        Returns:
            A dictionary representing the picklist options for the specified field.
        """
        response = requests.get(
            url=f"{self.base_url}/odata/v2/Picklist('{picklist_field}')?$expand=picklistOptions/picklistLabels&$format=JSON",
            auth=self.auth,
        )
        response.raise_for_status()
        return response.json()

    def upsert_request(
        self, payload: dict[str, Any] | list[dict[str, Any]], purge_type_full: bool = False
    ) -> dict[str, Any]:
        """
        Executes a generic upsert request against the SAP SuccessFactors API.

        Args:
            payload: A dictionary containing the input payload.
            purge_type_full: whether the API call should be made with purgeType=Full param

        Returns:
            The JSON response from the SAP SuccessFactors API.
        """
        purge_param = "&purgeType=Full" if purge_type_full else ""
        url = f"{self.base_url}/odata/v2/upsert?$format=JSON{purge_param}"

        response = requests.post(
            url=url,
            auth=self.auth,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    def post_request(
        self,
        entity: str,
        payload: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """
        Executes a generic upsert request against the SAP SuccessFactors API.

        Args:
            entity: The OData entity to query.
            payload: A dictionary containing the input payload (Optional).
            params: A dictionary containing the request params (Optional).

        Returns:
            The JSON response from the SAP SuccessFactors API.
        """
        json_param = {"$format": "JSON"}
        response = requests.post(
            url=f"{self.base_url}/odata/v2/{entity}",
            auth=self.auth,
            json=payload,
            params=params | json_param if params else json_param,
        )
        response.raise_for_status()
        response_json = response.json()
        response_json["http_code"] = response.status_code
        return response_json

    def delete_request(self, entity: str, payload: dict[str, Any]) -> int:
        """
        Executes a generic delete request against the SAP SuccessFactors API.

        Args:
            entity: The OData entity to query.
            payload: A dictionary containing the input payload.

        Returns:
            The status code of the request
        """
        response = requests.delete(
            url=f"{self.base_url}/odata/v2/{entity}", auth=self.auth, json=payload
        )
        response.raise_for_status()
        return response.status_code

    def get_request(
        self,
        entity: str,
        params: Optional[dict[str, Any]] = None,
        filter_expr: Optional[str] = None,
        select_expr: Optional[str] = None,
        expand_expr: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Executes a GET request against the provided OData entity.

        Args:
            entity: The OData entity to query.
            params: Query parameters for the REST API.
            filter_expr: An optional OData filter expression to restrict the results.
            select_expr: An optional OData select expression specifying which fields to include in
                the response.
            expand_expr: An optional OData expand expression specifying which fields to expand.

        Returns:
            The JSON response from the SAP SuccessFactors API.
        """
        url = f"{self.base_url}/odata/v2/{entity}"

        if params is None:
            params = {"$format": "JSON"}
        elif "$format" not in params:
            params["$format"] = "JSON"
        if filter_expr is not None:
            params["$filter"] = filter_expr
        if select_expr is not None:
            params["$select"] = select_expr
        if expand_expr is not None:
            params["$expand"] = expand_expr

        response = requests.get(url=url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json()

    def get_time_management_request(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        """
        Executes a GET request against a Time Management REST API.

        Args:
            endpoint: The specific endpoint to make the request against.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the specific SAP SuccessFactors Time Management REST API.
        """
        response = requests.get(
            url=f"{self.base_url}/rest/timemanagement/absence/v1/{endpoint}",
            params=params,  # TODO It looks like this request returns the same result irrespective of the assignmentId specified
            auth=self.auth,
        )
        response.raise_for_status()
        return response.json()


def get_sap_successfactors_client() -> SAPSuccessFactorsClient:
    """
    Get the sap successfactors client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Returns:
        A new instance of the SAP SuccessFactors client.
    """
    credentials = get_tool_credentials(Systems.SAP_SUCCESSFACTORS)

    sap_client = SAPSuccessFactorsClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        username=credentials[CredentialKeys.USERNAME],
        password=credentials[CredentialKeys.PASSWORD],
    )
    return sap_client
