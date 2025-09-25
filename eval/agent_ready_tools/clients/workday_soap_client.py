from http import HTTPMethod, HTTPStatus

import requests
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from agent_ready_tools.apis.workday_soap_services.compensation import api as comp_api
from agent_ready_tools.apis.workday_soap_services.hr import api as hr_api
from agent_ready_tools.apis.workday_soap_services.integration import api as integration_api
from agent_ready_tools.apis.workday_soap_services.integrations import api as integrations_api
from agent_ready_tools.apis.workday_soap_services.staff import api as staff_api
from agent_ready_tools.clients.auth_manager import WorkdayAuthManager
from agent_ready_tools.clients.clients_enums import AccessLevel
from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems


class WorkdaySOAPClient:
    """A remote client for Workday SOAP endpoints."""

    def __init__(
        self,
        base_url: str,
        token_url: str,
        tenant_name: str,
        client_id: str,
        client_secret: str,
        initial_bearer_token: str,
        initial_refresh_token: str,
        soapenv_attr: str = "http://schemas.xmlsoap.org/soap/envelope/",
        api_version: str = "v43.2",
    ):
        """
        Args:
            base_url: The base URL for the Workday API.
            token_url: The URL for authentication tokens for the Workday API.
            tenant_name: The name of the tenant.
            client_id: The client ID to authenticate with.
            client_secret: The client secret to authenticate with.
            initial_bearer_token: The initial bearer token from wxo-domains credentials file.
            initial_refresh_token: The initial refresh token from wxo-domains credentials file.
            soapenv_attr: The value for the 'soapenv' XML tag attribute to include in requests.
            api_version: The version of the workday SOAP API being used.
        """
        self.base_url = base_url
        self.tenant_name = tenant_name
        self.headers = {
            "Content-Type": "text/xml;charset=UTF-8",
        }
        self.auth_manager = WorkdayAuthManager(
            token_url=token_url,
            client_id=client_id,
            client_secret=client_secret,
            initial_bearer_token=initial_bearer_token,
            initial_refresh_token=initial_refresh_token,
            # TODO: make this an init param if a SOAP endpoint ever needs manager creds
            access_level=AccessLevel.EMPLOYEE,
        )

        self.soapenv_attr = soapenv_attr
        self.api_version = api_version
        self.xml_namespace_map = {"bsvc": "urn:com.workday/bsvc"}

        serializer_config = SerializerConfig(
            pretty_print=True,
            xml_declaration=True,
            indent="    ",
        )
        self.serializer = XmlSerializer(config=serializer_config)
        self.parser = XmlParser(context=XmlContext())

    def _request_with_reauth(
        self,
        method: str,
        url: str,
        data: str,
    ) -> requests.Response:
        """Makes a <method> request to the given URL with the given data, retrying on token
        expiry."""
        for _ in range(2):  # 1 retry
            self.headers["Authorization"] = f"Bearer {self.auth_manager.get_bearer_token()}"

            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                data=data,
            )
            if response.status_code == HTTPStatus.UNAUTHORIZED:
                self.auth_manager.refresh_bearer_token()
            else:
                break

        return response

    def get_change_passports_and_visas(
        self, payload: hr_api.GetChangePassportsAndVisasInput
    ) -> hr_api.GetChangePassportsAndVisasOutput:
        """
        Gets a user's passport and visa info in Workday.

        Args:
            payload: The dataclass representing the GetChangePassportsAndVisas request XML input.

        Returns:
            The dataclass representing the GetChangePassportsAndVisas request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)
        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, hr_api.GetChangePassportsAndVisasOutput)
        return output

    def change_preferred_name(
        self, payload: hr_api.ChangePreferredNameInput
    ) -> hr_api.ChangePreferredNameOutput:
        """
        Changes a user's preferred name in Workday.

        Args:
            payload: The dataclass representing the ChangePreferredName request XML input.

        Returns:
            The dataclass representing the ChangePreferredName request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)
        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, hr_api.ChangePreferredNameOutput)
        return output

    def get_holiday_calendar(
        self, payload: hr_api.GetHolidayCalendarsInput
    ) -> hr_api.GetHolidayCalendarsOutput:
        """
        Gets a country's holiday calendar for a given year in Workday.

        Args:
            payload: The dataclass representing the GetHolidayCalendars request XML input.

        Returns:
            The dataclass representing the GetHolidayCalendars request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)
        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, hr_api.GetHolidayCalendarsOutput)
        return output

    def get_current_compensation_details(
        self, payload: hr_api.GetWorkersInput
    ) -> hr_api.GetWorkersOutput:
        """
        Gets a user's current compensation details in Workday.

        Args:
            payload: The dataclass representing the GetCurrentCompensationDetails request XML input.

        Returns:
            The dataclass representing the GetCurrentCompensationDetails request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)
        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, hr_api.GetWorkersOutput)
        return output

    def update_disability_status(
        self, payload: hr_api.ChangePersonalInformationInput
    ) -> hr_api.ChangePersonalInformationOutput:
        """
        Update user's disability information Workday.

        Args:
            payload: The dataclass representing the ChangePersonalInformationInput request XML
                input.

        Returns:
            The dataclass representing the ChangePersonalInformationOutput request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)

        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, hr_api.ChangePersonalInformationOutput)
        return output

    def get_disabilities(self) -> hr_api.GetDisabilitiesOutput:
        """
        Gets Workday disabilities.

        Returns:
            The list of disabilities and their details obtained from the Workday API.
        """
        payload = hr_api.GetDisabilitiesInput(
            body=hr_api.GetDisabilitiesInput.Body(
                get_disabilities_request=hr_api.GetDisabilitiesRequest(version="v43.2")
            )
        )

        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)

        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, hr_api.GetDisabilitiesOutput)
        return output

    def request_compensation_change(
        self, payload: comp_api.RequestCompensationChangeInput
    ) -> comp_api.RequestCompensationChangeOutput:
        """
        Request an hourly or salary compensation change for a worker in Workday.

        Args:
            payload: The dataclass representing the RequestCompensationChange request XML input.

        Returns:
            The dataclass representing the RequestCompensationChange request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)

        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Compensation/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, comp_api.RequestCompensationChangeOutput)
        return output

    def get_compensation_change_references(
        self, payload: integrations_api.GetReferencesInput
    ) -> integrations_api.GetReferencesOutput:
        """
        Get the possible reasons references for changing compensation in Workday.

        Args:
            payload: The dataclass representing the GetReferences request XML input.

        Returns:
            The dataclass representing the GetReferences request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)

        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Integrations/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, integrations_api.GetReferencesOutput)
        return output

    def change_emergency_contact_info(
        self, payload: hr_api.ChangeEmergencyContactsInput
    ) -> hr_api.ChangeEmergencyContactsOutput:
        """
        Change emergency contact for the user in Workday.

        Args:
            payload: The dataclass representing the ChangeEmergencyContacts request XML input.

        Returns:
            The dataclass representing the ChangeEmergencyContacts request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)
        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, hr_api.ChangeEmergencyContactsOutput)
        return output

    def get_workers_emergency_contact(
        self, payload: hr_api.GetWorkersInput
    ) -> hr_api.GetWorkersOutput:
        """
        Gets worker data in Workday.

        Args:
            payload: The dataclass representing the GetWorkers request XML input.

        Returns:
            The dataclass representing the GetWorkers request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)
        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )

        response.raise_for_status()
        output = self.parser.from_bytes(response.content, hr_api.GetWorkersOutput)
        return output

    def get_related_person_relationships(
        self, payload: hr_api.GetRelatedPersonRelationshipsInput
    ) -> hr_api.GetRelatedPersonRelationshipsOutput:
        """
        Gets a relationship ID mapping in Workday.

        Args:
            payload: The dataclass representing the GetRelatedPersonRelationships request XML input.

        Returns:
            The dataclass representing the GetRelatedPersonRelationships request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)
        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )

        response.raise_for_status()
        output = self.parser.from_bytes(
            response.content, hr_api.GetRelatedPersonRelationshipsOutput
        )
        return output

    def post_job_change(
        self, payload: staff_api.StaffingPortChangeJobInput
    ) -> staff_api.StaffingPortChangeJobOutput:
        """
        Iniciate user's promotion n Workday.

        Args:
            payload: The dataclass representing the ChangeJobRequest request XML input.

        Returns:
            The dataclass representing the ChangeJobResponse request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)

        response = requests.post(
            url=f"{self.base_url}/service/{self.tenant_name}/Staffing/{self.api_version}",
            headers=self.headers,
            data=serialized_request,
        )

        response.raise_for_status()
        output = self.parser.from_bytes(response.content, staff_api.StaffingPortChangeJobOutput)

        return output

    def post_cancel_business_process_request(
        self, payload: integration_api.IntegrationsPortCancelBusinessProcessInput
    ) -> integration_api.IntegrationsPortCancelBusinessProcessOutput:
        """
        Cancel a business process event.

        Args:
            payload: The event to cancel within the Workday API.

        Returns:
            The event cancelated info.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)
        response = requests.post(
            url=f"{self.base_url}/service/{self.tenant_name}/Integrations/{self.api_version}",
            headers=self.headers,
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(
            response.content, integration_api.IntegrationsPortCancelBusinessProcessOutput
        )
        return output

    def get_my_benefit_plans(self, payload: hr_api.GetWorkersInput) -> hr_api.GetWorkersOutput:
        """
        Gets a user's benefit plans details in Workday.

        Args:
            payload: The dataclass representing the GetMyBenefitPlans request XML input.

        Returns:
            The dataclass representing the GetMyBenefitPlans request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)

        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/ccx/service/{self.tenant_name}/Human_Resources/{self.api_version}",
            data=serialized_request,
        )

        response.raise_for_status()
        output = self.parser.from_bytes(response.content, hr_api.GetWorkersOutput)
        return output

    def get_reference_ids(
        self, payload: integrations_api.GetReferencesInput
    ) -> integrations_api.GetReferencesOutput:
        """
        Get the possible references ids in Workday.

        Args:
            payload: The dataclass representing the GetReferences request XML input.

        Returns:
            The dataclass representing the GetReferences request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)

        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Integrations/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(response.content, integrations_api.GetReferencesOutput)
        return output

    def terminate_event(
        self, payload: staff_api.StaffingPortTerminateEmployeeInput
    ) -> staff_api.StaffingPortTerminateEmployeeOutput:
        """
        Terminates an employee in Workday.

        Args:
            payload: The dataclass representing the StaffingPortTerminateEmployee request XML input.

        Returns:
            The dataclass representing the StaffingPortTerminateEmployee request XML output.
        """
        serialized_request = self.serializer.render(payload, ns_map=self.xml_namespace_map)

        response = self._request_with_reauth(
            method=HTTPMethod.POST,
            url=f"{self.base_url}/service/{self.tenant_name}/Staffing/{self.api_version}",
            data=serialized_request,
        )
        response.raise_for_status()
        output = self.parser.from_bytes(
            response.content, staff_api.StaffingPortTerminateEmployeeOutput
        )
        return output


def get_workday_soap_client(access_level: AccessLevel = AccessLevel.EMPLOYEE) -> WorkdaySOAPClient:
    """
    Get the workday soap client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Args:
        access_level: It defines the persona of the logged-in user. By default, the value is
            EMPLOYEE.

    Returns:
        A new instance of the Workday SOAP client.
    """
    credentials = get_tool_credentials(system=Systems.WORKDAY, sub_category=access_level)
    workday_soap_client = WorkdaySOAPClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        token_url=credentials[CredentialKeys.TOKEN_URL],
        client_id=credentials[CredentialKeys.CLIENT_ID],
        client_secret=credentials[CredentialKeys.CLIENT_SECRET],
        tenant_name=credentials[CredentialKeys.TENANT_NAME],
        initial_bearer_token=credentials[CredentialKeys.BEARER_TOKEN],
        initial_refresh_token=credentials[CredentialKeys.REFRESH_TOKEN],
    )

    return workday_soap_client
