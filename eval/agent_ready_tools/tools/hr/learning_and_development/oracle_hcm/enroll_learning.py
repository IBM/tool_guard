import http
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.date_conversion import iso_8601_datetime_convert_to_date
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class EnrollmentLearningResponse:
    """Represents the enrollment result in Oracle HCM."""

    learning_name: Optional[str] = None
    learning_status: Optional[str] = None
    assigned_by: Optional[str] = None
    assigned_date: Optional[str] = None
    assignment_uuid: Optional[str] = None
    assignment_record_id: Optional[int] = None
    message: Optional[str] = None


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def enroll_learning(person_id: str, course_number: str) -> EnrollmentLearningResponse:
    """
    Initiate a learning enrollment in Oracle HCM.

    Args:
        person_id: The person_id uniquely identifies workers within the Oracle HCM, returned by the
            `get_user_oracle_ids` tool.
        course_number: The course_number of learning returned by `get_courses` tool.

    Returns:
        The result from learning enrollment.
    """

    client = get_oracle_hcm_client()
    result = client.post_request(
        payload={"learningItemNumber": course_number, "assignedToId": person_id},
        entity="learnerLearningRecords",
        headers={"Content-Type": "application/vnd.oracle.adf.resourceitem+json"},
    )

    if result.get("status_code", "") == http.HTTPStatus.CREATED:
        return EnrollmentLearningResponse(
            learning_name=result.get("learningItemTitle", ""),
            learning_status=result.get("assignmentSubStatusMeaning", ""),
            assigned_by=result.get("assignerDisplayName", ""),
            assigned_date=iso_8601_datetime_convert_to_date(result.get("assignedDate", "")),
            assignment_uuid=get_id_from_links(result.get("links", [])[0].get("href", "")),
            assignment_record_id=result.get("assignmentRecordId", ""),
        )
    message = result.get("message", "")
    return EnrollmentLearningResponse(message=message)
