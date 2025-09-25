from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class VisaDetails:
    """Represents a single visa record of a user in SAP SuccessFactors."""

    attachment: Optional[str]
    attachment_file_name: Optional[str]
    attachment_id: Optional[str]
    country: str
    document_number: str
    document_title: str
    document_type: str
    expiration_date: Optional[str]
    is_validated: Optional[bool]
    issue_date: str
    issue_place: Optional[str]
    issuing_authority: Optional[str]


@dataclass
class GetVisaDetailsResponse:
    """Represents all visa records of a user in SAP SuccessFactors."""

    visa_details: List[VisaDetails]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_visa_details(user_id: str) -> GetVisaDetailsResponse:
    """
    Retrieves a user's visa information in SAP SuccessFactors.

    Args:
        user_id: The user's ID uniquely identifying them within SAP SuccessFactors.

    Returns:
        A list of all visa details associated with the user.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(entity="EmpWorkPermit", filter_expr=f"userId eq '{user_id}'")
    results = response["d"]["results"]

    visa_details_list = [
        VisaDetails(
            attachment=record.get("attachment"),
            attachment_file_name=record.get("attachmentFileName"),
            attachment_id=record.get("attachmentId"),
            country=record.get("country"),
            document_number=record.get("documentNumber"),
            document_title=record.get("documentTitle"),
            document_type=record.get("documentType"),
            expiration_date=(
                sap_date_to_iso_8601(record.get("expirationDate"))
                if record.get("expirationDate") is not None
                else None
            ),
            is_validated=record.get("isValidated"),
            issue_date=(sap_date_to_iso_8601(record.get("issueDate"))),
            issue_place=record.get("issuePlace"),
            issuing_authority=record.get("issuingAuthority"),
        )
        for record in results
    ]
    return GetVisaDetailsResponse(visa_details=visa_details_list)
