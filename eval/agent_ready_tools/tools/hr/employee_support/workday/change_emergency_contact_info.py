from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.apis.workday_soap_services.hr import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.tools.hr.employee_support.workday.get_workers_emergency_contacts import (
    EmergencyContact,
)
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


def _change_emergency_contact_info_payload(
    user_id: str,
    emergency_contact: EmergencyContact,
    relationship: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    phone_number: Optional[str] = None,
) -> api.ChangeEmergencyContactsInput:
    """
    Returns a payload object of type ChangeEmergencyContactsInput filled.

    Args:
        user_id: The user's id uniquely identifying them within the Workday.
        emergency_contact: The emergency contact, as specified by the
            `get_workers_emergency_contacts` tool.
        relationship: The emergency contact's relationship_id with the user, as specified by the
            `get_relationship_id` tool.
        first_name: Emergency contact's first name.
        last_name: Emergency contact's last name.
        phone_number: Emergency contact's phone_number.

    Returns:
        The ChangeEmergencyContactsInput object
    """

    # The emergency contact that needs to be updated was not retrieved.
    if emergency_contact is None:
        return None

    if not first_name:
        first_name = emergency_contact.first_name

    if not last_name:
        last_name = emergency_contact.last_name

    if not phone_number:
        phone_number = emergency_contact.phone_number

    if not relationship:
        relationship = emergency_contact.related_person_relationship_reference

    return api.ChangeEmergencyContactsInput(
        body=api.ChangeEmergencyContactsInput.Body(
            change_emergency_contacts_request=api.ChangeEmergencyContactsRequest(
                change_emergency_contacts_data=api.ChangeEmergencyContactsBusinessProcessDataType(
                    person_reference=api.RoleObjectType(
                        id=[api.RoleObjectIdtype(value=user_id, type_value="WID")]
                    ),
                    emergency_contacts_reference_data=[
                        api.ChangeEmergencyContactsDataType(
                            emergency_contact_reference=api.EmergencyContactObjectType(
                                id=[
                                    api.EmergencyContactObjectIdtype(
                                        value=emergency_contact.emergency_contact_reference_wid,
                                        type_value="WID",
                                    )
                                ]
                            ),
                            emergency_contact_data=api.ChangeEmergencyContactDataType(
                                related_person_relationship_reference=[
                                    api.RelatedPersonRelationshipObjectType(
                                        id=[
                                            api.RelatedPersonRelationshipObjectIdtype(
                                                value=relationship, type_value="WID"
                                            )
                                        ]
                                    )
                                ],
                                emergency_contact_personal_information_data=api.EmergencyContactPersonalInformationDataType(
                                    person_name_data=[
                                        api.PersonNameDataType(
                                            legal_name_data=api.LegalNameDataType(
                                                name_detail_data=api.PersonNameDetailDataType(
                                                    country_reference=api.CountryObjectType(
                                                        id=[
                                                            api.CountryObjectIdtype(
                                                                value=emergency_contact.country_reference,
                                                                type_value="WID",
                                                            )
                                                        ]
                                                    ),
                                                    prefix_data=api.PersonNamePrefixDataType(
                                                        title_reference=api.CountryPredefinedPersonNameComponentValueObjectType(
                                                            id=[
                                                                api.CountryPredefinedPersonNameComponentValueObjectIdtype(
                                                                    value=emergency_contact.title_wid,
                                                                    type_value="WID",
                                                                )
                                                            ]
                                                        )
                                                    ),
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                )
                                            )
                                        )
                                    ],
                                    # here here
                                    contact_information_data=[
                                        api.ContactInformationDataType(
                                            phone_data=[
                                                api.PhoneInformationDataType(
                                                    country_iso_code=emergency_contact.iso_country_code,
                                                    international_phone_code=emergency_contact.international_code,
                                                    phone_number=phone_number,
                                                    phone_device_type_reference=api.PhoneDeviceTypeObjectType(
                                                        id=[
                                                            api.PhoneDeviceTypeObjectIdtype(
                                                                value=emergency_contact.phone_device_type_reference_wid,
                                                                type_value="WID",
                                                            )
                                                        ]
                                                    ),
                                                    usage_data=[
                                                        api.CommunicationMethodUsageInformationDataType(
                                                            type_data=[
                                                                api.CommunicationUsageTypeDataType(
                                                                    type_reference=api.CommunicationUsageTypeObjectType(
                                                                        id=[
                                                                            api.CommunicationUsageTypeObjectIdtype(
                                                                                value=emergency_contact.usage_data_type_wid,
                                                                                type_value="WID",
                                                                            )
                                                                        ]
                                                                    ),
                                                                    primary=True,
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                )
                                            ]
                                        )
                                    ],
                                ),
                            ),
                        )
                    ],
                )
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def change_emergency_contact_info(
    user_id: str,
    emergency_contact_reference_wid: str,
    related_person_relationship_reference_id: str,
    relationship: str,
    country_reference: str,
    title_wid: str,
    first_name: str,
    last_name: str,
    phone_device_type_reference_wid: str,
    usage_data_type_wid: str,
    phone_number: str,
    iso_country_code: str,
    international_code: Optional[str] = None,
    new_relationship: Optional[str] = None,
    new_first_name: Optional[str] = None,
    new_last_name: Optional[str] = None,
    new_phone_number: Optional[str] = None,
) -> Optional[api.ChangeEmergencyContactsOutput]:
    """
    Updates a user's emergency contact in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday.
        emergency_contact_reference_wid: emergency contact wid, as specified by the
            `get_workers_emergency_contacts` tool.
        related_person_relationship_reference_id: related person relationship reference id, as specified by the
            `get_workers_emergency_contacts` tool.
        relationship: Existing relationship with user of the emergency contact person, as specified by the
            `get_workers_emergency_contacts` tool.
        country_reference: Country of the Emergency contact person, as specified by the
            `get_workers_emergency_contacts` tool.
        title_wid: title reference wid, as specified by the
            `get_workers_emergency_contacts` tool.
        first_name: Existing first name of the emergency contact person, as specified by the
            `get_workers_emergency_contacts` tool.
        last_name: Existing last name of the emergency contact person, as specified by the
            `get_workers_emergency_contacts` tool.
        phone_device_type_reference_wid:  phone device type reference id, as specified by the
            `get_workers_emergency_contacts` tool.
        usage_data_type_wid: usage data type wid, as specified by the
            `get_workers_emergency_contacts` tool.
        phone_number: existing phone number of the emergency contact person, as specified by the
            `get_workers_emergency_contacts` tool.
        iso_country_code: ISO country code of the emergency contact person, as specified by the
            `get_workers_emergency_contacts` tool.
        international_code: international code of the emergency contact person, as specified by the
            `get_workers_emergency_contacts` tool.
        new_relationship: The emergency contact's relationship_id with the user, as specified by the
            `get_relationship_id` tool.
        new_first_name: Emergency contact's first name.
        new_last_name: Emergency contact's last name.
        new_phone_number: Emergency contact's phone_number.

    Returns:
        is change_emergency_contact_info successful
    """

    client = get_workday_soap_client()

    emergency_contact = EmergencyContact(
        emergency_contact_reference_wid=emergency_contact_reference_wid,
        related_person_relationship_reference=related_person_relationship_reference_id,
        first_name=first_name,
        relationship=relationship,
        last_name=last_name,
        phone_number=phone_number,
        country_reference=country_reference,
        title_wid=title_wid,
        iso_country_code=iso_country_code,
        international_code=international_code,
        phone_device_type_reference_wid=phone_device_type_reference_wid,
        usage_data_type_wid=usage_data_type_wid,
    )

    payload = _change_emergency_contact_info_payload(
        user_id=user_id,
        emergency_contact=emergency_contact,
        relationship=new_relationship,
        first_name=new_first_name,
        last_name=new_last_name,
        phone_number=new_phone_number,
    )

    xml_response = client.change_emergency_contact_info(payload)
    return xml_response
