import typing
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.workday_soap_services.hr import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class PassportVisaInfoResponse:
    """Represents the response from getting a user's passport/visa info in Workday."""

    user_id: str
    passport_id: Optional[str] = None
    passport_issue_country: Optional[str] = None
    passport_issue_date: Optional[str] = None
    passport_expiry_date: Optional[str] = None
    visa_id: Optional[str] = None
    visa_issue_country: Optional[str] = None
    visa_issue_date: Optional[str] = None
    visa_expiry_date: Optional[str] = None


def _get_passport_and_visa_info_payload(
    user_id: str,
) -> api.GetChangePassportsAndVisasInput:
    """
    Returns a payload object of type GetChangePassportsAndVisasInput filled.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.

    Returns:
        The GetChangePassportsAndVisasInput object.
    """
    return api.GetChangePassportsAndVisasInput(
        body=api.GetChangePassportsAndVisasInput.Body(
            get_change_passports_and_visas_request=api.GetChangePassportsAndVisasRequest(
                request_references=api.GetChangePassportsAndVisasRequestReferencesType(
                    person_reference=[
                        api.RoleObjectType(
                            id=[
                                api.RoleObjectIdtype(
                                    value=user_id,
                                    type_value="WID",
                                ),
                            ]
                        ),
                    ]
                )
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_passport_and_visa_info(user_id: str) -> PassportVisaInfoResponse:
    """
    Gets a user's passport and visa info in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.

    Returns:
        The user's passport and visa info.
    """
    client = get_workday_soap_client()

    payload = _get_passport_and_visa_info_payload(user_id=user_id)
    xml_response = client.get_change_passports_and_visas(payload)

    @typing.no_type_check
    def xml_to_internal_response(
        output: api.GetChangePassportsAndVisasOutput,
    ) -> PassportVisaInfoResponse:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            Internal PassportVisaInfoResponse object.
        """
        response_kwargs = {}

        try:
            change_passports_and_visas_data_node: (
                api.ChangePassportsAndVisasBusinessProcessDataType
            ) = (
                output.body.get_change_passports_and_visas_response.response_data[0]
                .change_passports_and_visas[0]
                .change_passports_and_visas_data[0]
            )
        except (IndexError, AttributeError) as e:
            raise ValueError(
                f"unexpected GetChangePassportsAndVisasOutput format: {e}\nraw output:\n{output}"
            )

        # get user_id from response XML
        try:
            person_ids: List[api.RoleObjectIdtype] = (
                change_passports_and_visas_data_node.person_reference.id
            )
            for pid in person_ids:
                if pid.type_value == "WID":
                    response_kwargs["user_id"] = pid.value
            assert response_kwargs["user_id"]
        except (IndexError, AttributeError, AssertionError) as e:
            raise ValueError(
                f"unexpected GetChangePassportsAndVisasOutput format: {e}\nraw output:\n{output}"
            )

        # If there is neither passport nor visa data.
        if change_passports_and_visas_data_node.passports_and_visas_identification_data is None:
            return PassportVisaInfoResponse(user_id=response_kwargs.get("user_id"))

        # get passport info from XML
        try:
            passport_id_data: api.PassportIdDataType = (
                change_passports_and_visas_data_node.passports_and_visas_identification_data.passport_id[
                    0
                ].passport_id_data
            )
            assert passport_id_data.id
            response_kwargs["passport_id"] = passport_id_data.id
            assert passport_id_data.country_reference
            country_ids: List[api.CountryObjectIdtype] = passport_id_data.country_reference.id
            for cid in country_ids:
                if cid.type_value == "ISO_3166-1_Alpha-3_Code":
                    response_kwargs["passport_issue_country"] = cid.value
            assert response_kwargs["passport_issue_country"]
            assert passport_id_data.issued_date
            response_kwargs["passport_issue_date"] = str(passport_id_data.issued_date)
            assert passport_id_data.expiration_date
            response_kwargs["passport_expiry_date"] = str(passport_id_data.expiration_date)
        except (IndexError, AttributeError, AssertionError) as e:
            raise ValueError(
                f"unexpected GetChangePassportsAndVisasOutput format or value(s): {e}\nraw output:\n{output}"
            )

        # get visa info from XML (not required)
        try:
            visa_id_data: api.VisaIdDataType = (
                change_passports_and_visas_data_node.passports_and_visas_identification_data.visa_id[
                    0
                ].visa_id_data
            )
            assert visa_id_data.id
            response_kwargs["visa_id"] = visa_id_data.id
            assert visa_id_data.country_reference
            country_ids: List[api.CountryObjectIdtype] = visa_id_data.country_reference.id
            for cid in country_ids:
                if cid.type_value == "ISO_3166-1_Alpha-3_Code":
                    response_kwargs["visa_issue_country"] = cid.value
            assert response_kwargs["visa_issue_country"]
            assert visa_id_data.issued_date
            response_kwargs["visa_issue_date"] = str(visa_id_data.issued_date)
            assert visa_id_data.expiration_date
            response_kwargs["visa_expiry_date"] = str(visa_id_data.expiration_date)
        except (IndexError, AttributeError, AssertionError):
            print(
                f"Either No Visa Info or malformed GetPassportsAndVisasResponse returned for EmployeeID: {user_id}"
            )

        return PassportVisaInfoResponse(**response_kwargs)

    return xml_to_internal_response(xml_response)
