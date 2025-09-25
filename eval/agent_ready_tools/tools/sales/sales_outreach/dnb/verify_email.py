from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel, ConfigDict, Field
from requests import HTTPError

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


class EmailVerificationResponse(BaseModel):
    """Represents the result of sending an email in Outlook."""

    model_config = ConfigDict(extra="ignore")  # Ignore extra fields

    threat_risk: str = Field(alias="threatRisk")
    disposition: str
    deliverability_score: int = Field(alias="deliverabilityScore")
    deliverability_rating: str = Field(alias="deliverabilityRating")
    email_type: str = Field(alias="emailType")
    is_dark_web: bool = Field(alias="isDarkWeb")


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def verify_email_address(email_address: str) -> Optional[EmailVerificationResponse]:
    """
    Verifies an emails deliverability score and provides other email details.

    Args:
        email_address: The email address to verify.

    Returns:
        A list of objects with email verification score and details, populated iff DnB
        returns with 200. Each object includes:
            - threat_risk (str): An email threat risk is an identifier flag that an email address may be dangerous to email to (regardless of the probability that the email address is valid).
            - disposition (str): The email disposition is a generalized response from the email server for an individual email attempt.
            - deliverability_score (int): The email deliverability score is a quantitiative data point that represents the probability that an email will deliver to the email address for that record. The score can be any integer value from 0-99.
            - deliverability_rating (str): The email deliverability rating is a five point qualitative rating system used to categorize the probability of an email reaching that address.
            - email_type (str): Type of email address. eg: business
            - is_dark_web (bool): whether the given email address is associated with the dark web.
    """
    client = get_dnb_client(entitlement=DNBEntitlements.SALES)
    email_verification_response: Optional[EmailVerificationResponse] = None

    try:
        response = client.get_request(
            version="v1",  # The API version.
            category="emailverification",  # The API category.
            path_parameter=email_address,  # path parameters
            params={
                "isDetailVerificationRequired": "true"
            },  # set detail verification to always true
        )

        email_verification_response = EmailVerificationResponse(
            **response["emailVerificationDetails"]
        )
    except HTTPError as e:
        if e.response.status_code == 404:
            # email not found, ignore
            pass
        else:
            raise e
    return email_verification_response
