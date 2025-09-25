import typing
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.workday_soap_services.hr import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.tools.hr.employee_support.workday.get_relationship_id import (
    _get_relationship_id_payload,
)
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class EmergencyContact:
    """The emergency contact, as specified by the `get_workers_emergency_contacts` tool."""

    emergency_contact_reference_wid: str
    related_person_relationship_reference: str
    relationship: str
    country_reference: str
    title_wid: str
    first_name: str
    last_name: str
    phone_device_type_reference_wid: str
    usage_data_type_wid: str
    phone_number: str
    iso_country_code: str
    international_code: Optional[str] = None


@dataclass
class GetEmergencyContactsResponse:
    """Represents the response from getting a user's emergency contacts in Workday."""

    emergency_contacts: list[EmergencyContact]


def _get_workers_emergency_contact_payload(
    user_id: str,
) -> api.GetWorkersInput:
    """
    Returns a payload object of type GetWorkersInput filled.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.

    Returns:
        The GetWorkersInput object.
    """
    return api.GetWorkersInput(
        body=api.GetWorkersInput.Body(
            get_workers_request=api.GetWorkersRequest(
                request_references=api.WorkerRequestReferencesType(
                    worker_reference=[
                        api.WorkerObjectType(
                            id=[api.WorkerObjectIdtype(value=user_id, type_value="WID")]
                        )
                    ]
                ),
                response_group=api.WorkerResponseGroupType(include_related_persons=True),
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_workers_emergency_contacts(user_id: str) -> GetEmergencyContactsResponse:
    """
    Gets a user's `emergency_contact` from Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.

    Returns:
        The emergency contact of the user.
    """
    client = get_workday_soap_client()

    # This retrieves information for all workers
    xml_response = client.get_workers_emergency_contact(
        _get_workers_emergency_contact_payload(user_id=user_id)
    )

    # This retrieves information for all relationships
    xml_relationship_response = client.get_related_person_relationships(
        _get_relationship_id_payload()
    )

    @typing.no_type_check
    def extract_relationship_mapping_from_xml_response(
        output: api.GetRelatedPersonRelationshipsOutput,
    ) -> dict:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            relationship ID.
        """

        try:
            all_relationships = (
                output.body.get_related_person_relationships_response.response_data.related_person_relationship
            )
            relationships = {}
            for rel in all_relationships:
                try:
                    relation_id = rel.related_person_relationship_reference.id[0].value
                    relation_name = rel.related_person_relationship_data[0].relationship_name
                    relationships[relation_id] = relation_name

                except (IndexError, AttributeError) as e:
                    raise ValueError(
                        f"unexpected GetRelatedPersonRelationshipsOutput format: {e}\nraw output:\n{output}"
                    )
            return relationships

        except (IndexError, AttributeError) as e:
            raise ValueError(
                f"unexpected GetRelatedPersonRelationshipsOutput format: {e}\nraw output:\n{output}"
            )

    relationship_mapping = extract_relationship_mapping_from_xml_response(xml_relationship_response)

    @typing.no_type_check
    def retrieve_emergency_contact(
        emergency_contact_reference_wid: str,
        relationship_id: str,
        relationship: str,
        personal_data: api.PersonalInformationDataType,
    ) -> Optional[EmergencyContact]:
        """
        Return EmergencyContact based on pesonal data.

        Args:
            emergency_contact_reference_wid: Emergency contact's ID
            relationship_id: Relationship id for the relation between the user and emergency contact
            relationship: The relation between the user and emergency contact
            personal_data: PersonalInformationDataType of the emergency contact

        Returns:
            EmergencyContact.
        """
        response_kwargs = {}

        try:
            response_kwargs["emergency_contact_reference_wid"] = emergency_contact_reference_wid
            response_kwargs["related_person_relationship_reference"] = relationship_id
            response_kwargs["relationship"] = relationship
            legal_name_data = personal_data.name_data.legal_name_data.name_detail_data
            phone_data = personal_data.contact_data.phone_data[0]

            response_kwargs["country_reference"] = legal_name_data.country_reference.id[0].value
            response_kwargs["title_wid"] = legal_name_data.prefix_data.title_reference.id[0].value
            response_kwargs["first_name"] = legal_name_data.first_name
            response_kwargs["last_name"] = legal_name_data.last_name

            response_kwargs["iso_country_code"] = phone_data.country_iso_code
            response_kwargs["international_code"] = phone_data.international_phone_code
            response_kwargs["phone_number"] = phone_data.phone_number
            response_kwargs["phone_device_type_reference_wid"] = (
                phone_data.phone_device_type_reference.id[0].value
            )
            response_kwargs["usage_data_type_wid"] = (
                phone_data.usage_data[0].type_data[0].type_reference.id[0].value
            )

            return EmergencyContact(**response_kwargs)
        except (IndexError, AttributeError):
            return None

    @typing.no_type_check
    def get_emergency_contact_from_xml_response(
        output: api.GetWorkersOutput,
    ) -> Optional[EmergencyContact]:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            EmergencyContact.
        """

        all_related_people = output.body.get_workers_response.response_data.worker[
            0
        ].worker_data.related_person_data.related_person

        related_people = []
        for related_person in all_related_people:
            relationship = (
                relationship_mapping[
                    related_person.related_person_relationship_reference[0].id[0].value
                ]
                if related_person.related_person_relationship_reference[0].id[0].value
                in relationship_mapping
                else "Not known"
            )

            person = retrieve_emergency_contact(
                related_person.emergency_contact.emergency_contact_reference.id[0].value,
                related_person.related_person_relationship_reference[0].id[0].value,
                relationship,
                related_person.personal_data,
            )
            if person:
                related_people.append(person)
        return GetEmergencyContactsResponse(emergency_contacts=related_people)

    return get_emergency_contact_from_xml_response(xml_response)
