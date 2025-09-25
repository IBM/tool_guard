from http import HTTPMethod, HTTPStatus
from typing import Any, Dict, Optional

import requests

from agent_ready_tools.clients.auth_manager import WorkdayAuthManager
from agent_ready_tools.clients.clients_enums import AccessLevel
from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class WorkdayClient:
    """A remote client for Workday."""

    def __init__(
        self,
        base_url: str,
        token_url: str,
        tenant_name: str,
        client_id: str,
        client_secret: str,
        initial_bearer_token: str,
        initial_refresh_token: str,
        access_level: AccessLevel,
    ):
        """
        Args:
            base_url: The base URL for the Workday API.
            token_url: The URL for authentication tokens for the Workday API.
            tenant_name: The name of the tenant.
            client_id: The client ID authenticate with.
            client_secret: The client secret to authenticate with.
            initial_bearer_token: The initial bearer token from wxo-domains credentials file.
            initial_refresh_token: The initial refresh token from wxo-domains credentials file.
            access_level: The access level (account type) the auth tokens correspond to.
        """
        self.base_url = base_url
        self.tenant_name = tenant_name
        self.auth_manager = WorkdayAuthManager(
            token_url=token_url,
            client_id=client_id,
            client_secret=client_secret,
            initial_bearer_token=initial_bearer_token,
            initial_refresh_token=initial_refresh_token,
            access_level=access_level,
        )
        self.headers = {
            "Content-Type": "application/json",
        }

    def _request_with_reauth(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Makes a <method> request to the given URL with the given params and payload, retrying on
        token expiry."""
        for _ in range(2):  # 1 retry
            self.headers["Authorization"] = f"Bearer {self.auth_manager.get_bearer_token()}"
            response = requests.request(
                method=method,
                url=url,
                params=params,
                headers=self.headers,
                json=payload,
            )
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                self.auth_manager.refresh_bearer_token()
            else:
                break
        return response

    def get_request(self, url: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """
        Executes a GET request against Workday API.

        Args:
            url: The full URL to make the request against.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the Workday API.
        """
        response = requests.request(
            method=HTTPMethod.GET,
            url=f"{self.base_url}/{url}",
            params=params,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def update_home_phone(
        self, home_contact_information_change_id: str, home_phone_id: str, new_home_phone: str
    ) -> dict[str, Any]:
        """
        Update a user's home phone in Workday.

        Args:
            home_contact_information_change_id: The unique identifier for the home contact
                information change.
            home_phone_id: The id uniquely identifying the user's home phone to be updated.
            new_home_phone: The new home phone.

        Returns:
            The response for the change request.
        """
        response = self._request_with_reauth(
            HTTPMethod.PATCH,
            url=f"{self.base_url}/api/person/v4/{self.tenant_name}/homeContactInformationChanges/"
            f"{home_contact_information_change_id}/phoneNumbers/{home_phone_id}",
            payload={"completePhoneNumber": new_home_phone},
        )
        response.raise_for_status()
        return response.json()

    def get_href(self, href: str) -> dict[str, Any]:
        """
        Gets the contents from an href from Workday.

        Args:
            href: The href to be requested.

        Returns:
            The requested content.
        """

        response = requests.get(
            url=href,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def initiate_job_change(
        self, worker_id: str, body: dict[str, Any], version: str = "v6"
    ) -> dict[str, Any]:
        """
        Initiates a job change in Workday.

        Args:
            worker_id: The worker id associated with this job change request.
            body: The body to be submitted with the job change request.
            version: The version of Workday API.

        Returns:
            The job change response.
        """

        response = requests.post(
            url=f"{self.base_url}/api/staffing/{version}/{self.tenant_name}/workers/{worker_id}/jobChanges",
            headers=self.headers,
            json=body,
        )

        return response.json()

    def submit_job_change(self, job_change_id: str, version: str = "v6") -> dict[str, Any]:
        """
        Submits a job change request.

        Args:
            job_change_id: The id of the job change to be submitted.
            version: The version of Workday API.

        Returns:
            The result of the job change submission.
        """

        response = requests.post(
            url=f"{self.base_url}/api/staffing/{version}/{self.tenant_name}/jobChanges/{job_change_id}/submit",
            headers=self.headers,
            json={},
        )

        return response.json()

    def update_business_title(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Updates the user's business title in Workday.

        Args:
            user_id: The user's id uniquely identifying them within the Workday API.
            payload: The request payload containing the new business title.

        Returns:
            The JSON response from the Workday API.
        """
        response = self._request_with_reauth(
            HTTPMethod.POST,
            url=f"{self.base_url}/api/common/v1/{self.tenant_name}/workers/{user_id}/businessTitleChanges",
            payload=payload,
        )
        response.raise_for_status()
        return response.json()

    def request_time_off(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Create a time off request for a user in Workday.

        Args:
            user_id: The user's id uniquely identifying them within the Workday API.
            payload: The request payload containing the time off request information.

        Returns:
            The JSON response from the Workday API.
        """
        response = self._request_with_reauth(
            HTTPMethod.POST,
            url=f"{self.base_url}/api/absenceManagement/v1/{self.tenant_name}/workers/{user_id}/requestTimeOff",
            payload=payload,
        )
        response.raise_for_status()
        return response.json()

    def add_home_email(
        self, home_contact_information_change_id: str, new_home_email: str
    ) -> dict[str, Any]:
        """
        Add a user's home email in Workday.

        Args:
            home_contact_information_change_id: The unique identifier for the home contact
                information change.
            new_home_email: The new home email.

        Returns:
            The response for the change request.
        """
        response = self._request_with_reauth(
            HTTPMethod.POST,
            url=f"{self.base_url}/api/person/v4/{self.tenant_name}"
            f"/homeContactInformationChanges/{home_contact_information_change_id}/emailAddresses",
            payload={
                "emailAddress": new_home_email,
                "usage": {"usageType": {"id": "836cf00ef5974ac08b786079866c946f"}, "primary": True},
            },
        )
        response.raise_for_status()
        return response.json()

    def update_home_email(
        self, home_contact_information_change_id: str, home_email_id: str, new_home_email: str
    ) -> dict[str, Any]:
        """
        Update a user's home email in Workday.

        Args:
            home_contact_information_change_id: The unique identifier for the home contact
                information change.
            home_email_id: The id uniquely identifying the user's home email to be updated.
            new_home_email: The new home email.

        Returns:
            The response for the change request.
        """
        response = self._request_with_reauth(
            HTTPMethod.PATCH,
            url=f"{self.base_url}/api/person/v4/{self.tenant_name}"
            f"/homeContactInformationChanges/{home_contact_information_change_id}/emailAddresses/{home_email_id}",
            payload={"emailAddress": new_home_email},
        )
        response.raise_for_status()
        return response.json()

    def post_home_contact_information_changes(
        self, user_id: str, effective_date: str
    ) -> dict[str, Any]:
        """
        Create a home contact information change request.

        Args:
            user_id: The user's id uniquely identifying them within the Workday API.
            effective_date: The effective date for the change in ISO 8601 format.

        Returns:
            The home contact information change response.
        """
        response = self._request_with_reauth(
            HTTPMethod.POST,
            url=f"{self.base_url}/api/staffing/v7/{self.tenant_name}/workers/{user_id}/homeContactInformationChanges",
            payload={"effective_date": effective_date},
        )
        response.raise_for_status()
        return response.json()

    def put_home_address(
        self,
        home_contact_information_changes_id: str,
        address_id: str,
        address_line_1: str,
        city: str,
        state_id: str,
        country_id: str,
        postal_code: str,
        is_primary: bool,
        address_line_2: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Updates the user's home address in Workday.

        Args:
            home_contact_information_changes_id: The home contact information, as specified by the
                `post_home_contact_information_changes` tool.
            address_id: The address id that needs to be updated.
            address_line_1: First line of address.
            city: The name of the city.
            state_id: The state_id corresponding to the state the address is in.
            country_id: The country_id corresponding to the country the address is in.
            postal_code: The postal code or the zip code of the address.
            is_primary: True or false value indicating whether this is the primary address.
            address_line_2: Second line of address.

        Returns:
            The response from updating the home address.
        """
        response = self._request_with_reauth(
            HTTPMethod.PUT,
            url=f"{self.base_url}/api/person/v4/{self.tenant_name}/homeContactInformationChanges/{home_contact_information_changes_id}/addresses/{address_id}",
            payload={
                "countryRegion": {
                    "id": state_id,
                },
                "postalCode": postal_code,
                "usage": {
                    "usageType": {
                        "id": "836cf00ef5974ac08b786079866c946f",
                    },
                    "primary": is_primary,
                },
                "city": city,
                "country": {
                    "id": country_id,
                },
                "addressLine1": address_line_1,
                "addressLine2": address_line_2,
            },
        )
        response.raise_for_status()
        return response.json()

    def post_home_contact_information_changes_submit(
        self,
        home_contact_information_change_id: str,
    ) -> dict[str, Any]:
        """
        Submits a home contact information change.

        Args:
            home_contact_information_change_id: The unique identifier for the home contact
                information change.

        Returns:
            The response from submitting the change.
        """
        response = self._request_with_reauth(
            HTTPMethod.POST,
            url=f"{self.base_url}/api/person/v4/{self.tenant_name}/homeContactInformationChanges/{home_contact_information_change_id}/submit",
            payload={},
        )
        response.raise_for_status()
        return response.json()

    def patch_initiate_a_cost_center_change(
        self, payload: dict, organization_assignment_change_id: str
    ) -> dict[str, Any]:
        """
        Updates a user's cost center in Workday.

        Args:
            payload: The payload containing the cost center information.
            organization_assignment_change_id: The ID of the organization assignment change.

        Returns:
            The response from the Workday API.
        """
        response = self._request_with_reauth(
            HTTPMethod.PATCH,
            url=f"{self.base_url}/api/staffing/v6/{self.tenant_name}/organizationAssignmentChanges/{organization_assignment_change_id}/costCenter/{organization_assignment_change_id}",
            payload=payload,
        )

        return response.json()

    def post_create_organization_assignment_change(
        self, payload: dict, user_id: str
    ) -> dict[str, Any]:
        """
        Creates an organization assignment change in Workday.

        Args:
            payload: The payload containing the date for the organization assignment change.
            user_id: The ID of the worker for whom the organization assignment change is being
                created.

        Returns:
            The response from the Workday API.
        """
        response = self._request_with_reauth(
            HTTPMethod.POST,
            url=f"{self.base_url}/api/staffing/v6/{self.tenant_name}/workers/{user_id}/organizationAssignmentChanges",
            payload=payload,
        )

        return response.json()

    def post_submit_organization_assignment_change_id(
        self, payload: dict[str, Any], organization_assignment_change_id: str
    ) -> dict[str, Any]:
        """
        Creates an organization assignment change in Workday.

        Args:
            payload: The payload containing the date for the organization assignment change.
            organization_assignment_change_id: The ID of the organization assignment change.

        Returns:
            The response from the Workday API.
        """
        response = self._request_with_reauth(
            HTTPMethod.POST,
            url=f"{self.base_url}/api/staffing/v6/{self.tenant_name}/organizationAssignmentChanges/{organization_assignment_change_id}/submit",
            payload=payload,
        )

        return response.json()

    def approve_time_off_and_time_entries(
        self, pending_request_id: str, request_response: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Approves the worker's time off and time entry requests in Workday.

        Args:
            pending_request_id: The pending time off or time entry request id.
            request_response: The response to the request. Acceptable values are: 'approval' or
                'denial'.
            payload: The request payload containing the comment for managing time off and time entry
                request.

        Returns:
            The JSON response from the Workday API.
        """
        response = self._request_with_reauth(
            HTTPMethod.PUT,
            url=f"{self.base_url}/api/common/v1/{self.tenant_name}/inboxTasks/{pending_request_id}?type={request_response}",
            payload=payload,
        )
        response.raise_for_status()
        return response.json()


# TODO We may want to consider removing `access_level` from here if we find a more elegant way to test tools that require multiple personas
def get_workday_client(access_level: AccessLevel = AccessLevel.EMPLOYEE) -> WorkdayClient:
    """
    Get the workday client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Args:
        access_level: It defines the persona of the logged-in user. By default, the value is
            EMPLOYEE.

    Returns:
        A new instance of the Workday client.
    """
    credentials = get_tool_credentials(system=Systems.WORKDAY, sub_category=access_level)
    workday_client = WorkdayClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        token_url=credentials[CredentialKeys.TOKEN_URL],
        tenant_name=credentials[CredentialKeys.TENANT_NAME],
        client_id=credentials[CredentialKeys.CLIENT_ID],
        client_secret=credentials[CredentialKeys.CLIENT_SECRET],
        initial_bearer_token=credentials[CredentialKeys.BEARER_TOKEN],
        initial_refresh_token=credentials[CredentialKeys.REFRESH_TOKEN],
        access_level=access_level,
    )
    return workday_client
