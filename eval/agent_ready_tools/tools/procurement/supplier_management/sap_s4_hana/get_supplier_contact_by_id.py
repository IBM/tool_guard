from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANAContactPersonDetails:
    """Represents a person in SAP S4 Hana."""

    person_id: str
    full_name: str
    last_name: str
    first_name: str
    email_address: str
    house_number: str
    street: str
    city: str
    country: str
    postal_code: str


@dataclass
class S4HANAContactPersonDetailsResponse:
    """Represents a list of persons available in SAP S4 Hana."""

    persons: list[S4HANAContactPersonDetails]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_supplier_contact_by_id(
    contact_person_id: str,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[S4HANAContactPersonDetailsResponse]:
    """
    Gets the contact person details for a supplier.

    Args:
        contact_person_id: The id of the supplier contact person.
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

    filter_expr = f"BusinessPartnerCategory eq '1' and BusinessPartner eq '{contact_person_id}'"

    expand_expr = "to_BusinessPartnerAddress,to_BusinessPartnerAddress/to_EmailAddress"

    response = client.get_request(
        entity="API_BUSINESS_PARTNER/A_BusinessPartner",
        params=params,
        filter_expr=filter_expr,
        expand_expr=expand_expr,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    persons: list[S4HANAContactPersonDetails] = []
    for person in response["response"]["d"]["results"]:
        if person.get("to_BusinessPartnerAddress", {}).get("results", []) != []:
            for address in person.get("to_BusinessPartnerAddress", {}).get("results", []):
                if address.get("to_EmailAddress", {}).get("results", []) != []:
                    for email in address.get("to_EmailAddress", {}).get("results", []):
                        persons.append(
                            S4HANAContactPersonDetails(
                                person_id=person.get("BusinessPartner", ""),
                                full_name=person.get("BusinessPartnerName", ""),
                                first_name=person.get("FirstName", ""),
                                last_name=person.get("LastName", ""),
                                email_address=email.get("EmailAddress", ""),
                                house_number=address.get("HouseNumber", ""),
                                street=address.get("StreetName", ""),
                                city=address.get("CityName", ""),
                                country=address.get("Country", ""),
                                postal_code=address.get("PostalCode", ""),
                            )
                        )
                else:
                    persons.append(
                        S4HANAContactPersonDetails(
                            person_id=person.get("BusinessPartner", ""),
                            full_name=person.get("BusinessPartnerName", ""),
                            first_name=person.get("FirstName", ""),
                            last_name=person.get("LastName", ""),
                            email_address="",
                            house_number=address.get("HouseNumber", ""),
                            street=address.get("StreetName", ""),
                            city=address.get("CityName", ""),
                            country=address.get("Country", ""),
                            postal_code=address.get("PostalCode", ""),
                        )
                    )

        else:
            persons.append(
                S4HANAContactPersonDetails(
                    person_id=person.get("BusinessPartner", ""),
                    full_name=person.get("BusinessPartnerName", ""),
                    first_name=person.get("FirstName", ""),
                    last_name=person.get("LastName", ""),
                    email_address="",
                    house_number="",
                    street="",
                    city="",
                    country="",
                    postal_code="",
                )
            )

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=S4HANAContactPersonDetailsResponse(persons=persons),
    )
