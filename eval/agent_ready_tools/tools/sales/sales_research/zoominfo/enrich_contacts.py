import re
from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.zoominfo_client import get_zoominfo_client
from agent_ready_tools.tools.sales.sales_research.zoominfo.zoominfo_schemas import (
    ErrorResponse,
    ZoominfoEnrichedContact,
)
from agent_ready_tools.utils.tool_credentials import ZOOMINFO_CONNECTIONS


@tool(expected_credentials=ZOOMINFO_CONNECTIONS)
def zoominfo_enrich_contacts(
    person_id_list: list[str],
) -> List[ZoominfoEnrichedContact] | ErrorResponse:
    """
    Retrieves contact details based on person ID.

    Args:
        person_id_list: A list of person_id.

    Returns:
        A list of enriched contacts for the requested person ID(s). Each object includes:
            - first_name (str): The first name of the contact.  # mapped from firstName
            - last_name (str): The last name of the contact.  # mapped from lastName
            - email (str): The email address of the contact. # mapped from email
            - city (str): The city where the contact is located. # mapped from city
            - job_title (str): The job title of the contact at the current place of employment.  # mapped from jobTitle
            - job_function (str): The job function of the contact at current place of employment. # mapped from jobFunction
            - company_name (str):  Name of the contact's current company # mapped from companyName
            - social_media (str): The social media link of the contact. # mapped from externalUrls
    """
    client = get_zoominfo_client()

    person_input = []
    for person_id in person_id_list:
        person_dic = {"personId": person_id}
        person_input.append(person_dic)

    response = client.post_request(
        category="enrich",
        endpoint="contact",
        data={
            "outputFields": [
                "firstName",
                "lastName",
                "email",
                "city",
                "jobTitle",
                "jobFunction",
                "companyName",
                "externalUrls",
            ],
            "matchPersonInput": person_input,
        },
    )

    if response.get("success"):
        results = response["data"]["result"]
        enriched_contacts: list[ZoominfoEnrichedContact] = []
        for result in results:
            people_data = result.get("data", "")
            for person in people_data:
                job_function_data = person.get("jobFunction", None)
                company_data = person.get("company", None)
                social_media_data = person.get("externalUrls", None)
                social_media_list = (
                    []
                    if social_media_data is None
                    else [
                        x["url"]
                        for x in social_media_data
                        if isinstance(x, dict) and "url" in x and re.search("linkedin", x["url"])
                    ]
                )
                enriched_contacts.append(
                    ZoominfoEnrichedContact(
                        first_name=person.get("firstName", ""),
                        last_name=person.get("lastName", ""),
                        email=person.get("email", ""),
                        city=person.get("city", ""),
                        job_title=person.get("jobTitle", ""),
                        job_function=(
                            ""
                            if len(job_function_data) == 0 or job_function_data is None
                            else job_function_data[0].get("name", "")
                        ),
                        company_name=(
                            ""
                            if len(company_data) == 0 or company_data is None
                            else company_data.get("name", "")
                        ),
                        social_media=("" if len(social_media_list) == 0 else social_media_list[0]),
                    )
                )
        return enriched_contacts
    else:
        return ErrorResponse(message=response.get("error"), status_code=response.get("statusCode"))
