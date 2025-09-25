from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    Department,
    FunctionOfPartner,
    SAPS4HANASupplierCategory,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS

# The 'has a contact person' id of the relationship category.
RELATIONSHIP_CATEGORY_HAS_A_CONTACT = "BUR001"


@dataclass
class S4HANAAddContactResponse:
    """Represents the result of add supplier contact operation in SAP S4 HAHA."""

    supplier_id: str
    person_id: str


@dataclass
class S4HanaPerson:
    """Represents a person in SAP S4 Hana."""

    person_id: str
    full_name: str
    last_name: str
    first_name: str
    email_address: str


@dataclass
class S4HanaPersonResponse:
    """Represents a list of persons available in SAP S4 Hana."""

    persons: list[S4HanaPerson]


@dataclass
class S4HANACreatePersonResponse:
    """Represents a person in SAP S4 HANA."""

    person_id: str
    first_name: str
    last_name: str


def sap_s4_hana_get_persons(
    first_name: str,
    last_name: str,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HanaPersonResponse]:
    """
    Gets a list of persons.

    Args:
        first_name: First name of the person.
        last_name: Last name of the person.
        limit: The number of persons returned.
        skip: The number of persons to skip for pagination.

    Returns:
        The list of persons.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    params = {"$top": limit, "$skip": skip}

    filter_expr = f"BusinessPartnerCategory eq '1' and LastName eq '{last_name}' and FirstName eq '{first_name}'"

    expand_expr = "to_BusinessPartnerAddress,to_BusinessPartnerAddress/to_EmailAddress"

    response = client.get_request(
        entity="API_BUSINESS_PARTNER/A_BusinessPartner",
        params=params,
        filter_expr=filter_expr,
        expand_expr=expand_expr,
    )

    if "error" in response or "fault" in response:
        return ToolResponse(
            success=False, message="Request unsuccessful", content=S4HanaPersonResponse(**response)
        )

    persons: list[S4HanaPerson] = []
    for person in response["response"]["d"]["results"]:
        if person.get("to_BusinessPartnerAddress", {}).get("results", []) != []:
            for address in person.get("to_BusinessPartnerAddress", {}).get("results", []):
                if address.get("to_EmailAddress", {}).get("results", []) != []:
                    for email in address.get("to_EmailAddress", {}).get("results", []):
                        persons.append(
                            S4HanaPerson(
                                person_id=person.get("BusinessPartner", ""),
                                full_name=person.get("BusinessPartnerName", ""),
                                first_name=person.get("FirstName", ""),
                                last_name=person.get("LastName", ""),
                                email_address=email.get("EmailAddress", ""),
                            )
                        )
                else:
                    persons.append(
                        S4HanaPerson(
                            person_id=person.get("BusinessPartner", ""),
                            full_name=person.get("BusinessPartnerName", ""),
                            first_name=person.get("FirstName", ""),
                            last_name=person.get("LastName", ""),
                            email_address="",
                        )
                    )

        else:
            persons.append(
                S4HanaPerson(
                    person_id=person.get("BusinessPartner", ""),
                    full_name=person.get("BusinessPartnerName", ""),
                    first_name=person.get("FirstName", ""),
                    last_name=person.get("LastName", ""),
                    email_address="",
                )
            )

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=S4HanaPersonResponse(persons=persons),
    )


def sap_s4_hana_create_person(
    first_name: str,
    last_name: str,
    email_address: str,
    country: str,
    house_number: Optional[str] = None,
    street: Optional[str] = None,
    city: Optional[str] = None,
    postal_code: Optional[str] = None,
) -> ToolResponse[S4HANACreatePersonResponse]:
    """
    Creates a person in SAP S4 HANA.

    Args:
        first_name: The first name of the person.
        last_name: The last name of the person.
        email_address: The email address of the person.
        country: The country_code of the person's address, returned by sap_s4_hana_get_countries
            tool.
        house_number: The house number of the person's address.
        street: The street name of the person's address.
        city: The city of the person's address.
        postal_code: The postal code of the person's address.

    Returns:
        The result of creating a person.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    payload: Dict[str, Any] = {
        "BusinessPartnerCategory": SAPS4HANASupplierCategory.PERSON.value,
        "FirstName": first_name,
        "LastName": last_name,
    }

    address: Dict[str, List[Dict[str, Any]]] = {
        "to_BusinessPartnerAddress": [
            {
                "HouseNumber": house_number,
                "StreetName": street,
                "CityName": city,
                "Country": country,
                "PostalCode": postal_code,
                "to_EmailAddress": {"results": [{"EmailAddress": email_address}]},
            }
        ]
    }

    address = {
        key: [{key: value for key, value in item.items() if value} for item in value]
        for key, value in address.items()
        if value
    }

    payload.update(address)

    response = client.post_request(entity="API_BUSINESS_PARTNER/A_BusinessPartner", payload=payload)

    if "error" in response:
        content = response.get("error", {}).get("message", {}).get("value", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    person_id = response.get("d", {}).get("BusinessPartner", "")
    first_name = response.get("d", {}).get("FirstName", "")
    last_name = response.get("d", {}).get("LastName", "")

    return ToolResponse(
        success=True,
        message="The person was successfully created.",
        content=S4HANACreatePersonResponse(
            person_id=person_id, first_name=first_name, last_name=last_name
        ),
    )


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_add_supplier_contact(
    supplier_id: str,
    first_name: str,
    last_name: str,
    email_address: str,
    country: str,
    house_number: Optional[str] = None,
    street: Optional[str] = None,
    city: Optional[str] = None,
    postal_code: Optional[str] = None,
    start_date: Optional[str] = None,
    person_function: Optional[FunctionOfPartner] = None,
    person_department: Optional[Department] = None,
    phone_number: Optional[str] = None,
    phone_country_code: Optional[str] = None,
) -> ToolResponse[S4HANAAddContactResponse]:
    """
    Adds a contact to a supplier in SAP S4 HANA.

    Args:
        supplier_id: The id of the supplier, returned by sap_s4_hana_get_suppliers tool.
        first_name: The first name of the person.
        last_name: The last name of the person.
        email_address: The email address of the person.
        country: The country_code of the person's address, returned by sap_s4_hana_get_countries
            tool.
        house_number: The house number of the person's address.
        street: The street name of the person's address.
        city: The city of the person's address.
        postal_code: The postal code of the person's address.
        start_date: The start date of the relation in `YYYY-MM-DD` format.
        person_function: The person function in SAP S4 HANA.
        person_department: The person department in SAP S4 HANA.
        phone_number: The phone number of the contact.
        phone_country_code: The country code for the phone number of the contact.

    Returns:
        The result from performing the sap_s4_hana_add_supplier_contact tool in SAP S4 HANA.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    # calling this function to check the person already exists or not
    get_person_response = sap_s4_hana_get_persons(first_name=first_name, last_name=last_name)

    if not get_person_response.success:
        error: Dict[str, Any] = (
            get_person_response.content if isinstance(get_person_response.content, dict) else {}
        )
        message = (
            f"{error.get('fault', {}).get('faultstring')}"
            or f"{error.get('error', {}).get('message', {}).get('status_code', '')} : "
            f"{error.get('error', {}).get('message', {}).get('value', '')}"
        )
        return ToolResponse(success=False, message=f"Request unsuccessful {message}")

    person_response = get_person_response.content

    person_id = ""
    persons = person_response.persons if person_response is not None else []
    if persons:
        if len(persons) == 1 and persons[0].email_address == email_address:
            person_id = persons[0].person_id
        elif len(persons) > 1:
            for person in persons:
                if email_address == person.email_address:
                    person_id = person.person_id
                    break

    if person_id == "":
        # if person does not exists creating new person
        create_person_response = sap_s4_hana_create_person(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            country=country,
            house_number=house_number,
            street=street,
            city=city,
            postal_code=postal_code,
        )

        if not create_person_response.success:
            errors: Dict[str, Any] = (
                create_person_response.content
                if isinstance(create_person_response.content, dict)
                else {}
            )
            if isinstance(errors, dict):
                message = (
                    errors.get("fault", {}).get("faultstring")
                    or f"{errors.get('error', {}).get('message', {}).get('status_code', '')} : "
                    f"{errors.get('error', {}).get('message', {}).get('value', '')}"
                )
            else:
                message = str(errors)
            return ToolResponse(success=False, message=f"Request unsuccessful {message}")

        if create_person_response.content is not None:
            person_id = create_person_response.content.person_id

    payload = {
        "BusinessPartnerCompany": supplier_id,
        "BusinessPartnerPerson": person_id,
        "RelationshipCategory": RELATIONSHIP_CATEGORY_HAS_A_CONTACT,
        "to_ContactRelationship": {
            "BusinessPartnerCompany": supplier_id,
            "ContactPersonFunction": (
                FunctionOfPartner[person_function.upper()].value if person_function else None
            ),
            "ContactPersonDepartment": (
                Department[person_department.upper()].value if person_department else None
            ),
            "PhoneNumber": phone_number,
            "PhoneNumberExtension": phone_country_code,
            "EmailAddress": email_address,
        },
    }

    if start_date:
        payload["ValidityStartDate"] = iso_8601_to_sap_date(start_date)

    payload = {
        key: (
            {key: value for key, value in value.items() if value}
            if isinstance(value, dict)
            else value
        )
        for key, value in payload.items()
        if value
    }

    response = client.post_request(
        entity="API_BUSINESS_PARTNER/A_BusinessPartnerContact", payload=payload
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {}).get("value", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    supplier_id = response.get("d", {}).get("BusinessPartnerCompany", "")
    person_id = response.get("d", {}).get("BusinessPartnerPerson", "")

    return ToolResponse(
        success=True,
        message="The contact was successfully added to the supplier.",
        content=S4HANAAddContactResponse(person_id=person_id, supplier_id=supplier_id),
    )
