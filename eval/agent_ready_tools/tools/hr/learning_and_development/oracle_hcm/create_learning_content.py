from enum import StrEnum
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class LearningTrackingType(StrEnum):
    """The tracking type of the learning in Oracle HCM."""

    ZIP_12 = "ORA_SCORM_12"
    ZIP_2004 = "ORA_SCORM_2004"
    HACP = "ORA_HACP"
    PDF = "ORA_PDF"
    WEBLINK = "ORA_AUTO"
    VIDEO = "ORA_CONTENT_VIDEO"


@dataclass
class LearningStatus(StrEnum):
    """Represents the status of learning in Oracle HCM."""

    ACTIVE = "ORA_CONT_ACTIVE"
    INACTIVE = "ORA_CONT_INACTIVE"


@dataclass
class CreatelearningcontentResponse:
    """Represents the results of learning content create operation in Oracle HCM."""

    http_code: int


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def create_learning_content(
    title: str,
    file_name: str,
    item_number: str,
    start_date: str,
    end_date: str,
    tracking_type: LearningTrackingType,
    url: Optional[str] = None,
    status: Optional[LearningStatus] = None,
    description: Optional[str] = None,
) -> CreatelearningcontentResponse:
    """
    Creates learning content in Oracle HCM.

    Args:
        title: The title of the learning content.
        file_name: The file name of the  learning content.For example, PDFname.pdf, VIDEOname.mov,
            ZIPfile.zip.
        item_number: The item number of the learning content.
        start_date: The start date of the learning content.
        end_date: The end date of the learning content.
        tracking_type: The tracking type of the learning in Oracle HCM.
        url: The url for the WEBLINK tracking type of the learning content.
        status: The status of the learning content. This field is applicable only when the tracking type
            is either 'PDF' or 'WEBLINK'
        description: The description of the learning content.

    Returns:
        The result from performing the create learning content.
    """

    client = get_oracle_hcm_client()

    payload = {
        "Title": title,
        "FileName": file_name,
        "ItemNumber": item_number,
        "TrackingType": LearningTrackingType[tracking_type.upper()].value,
        "StartDate": start_date,
        "EndDate": end_date,
    }

    if (
        tracking_type in (LearningTrackingType.PDF.name, LearningTrackingType.WEBLINK.name)
        and status is not None
    ):
        payload["Status"] = LearningStatus[status.upper()].value

    if tracking_type == (LearningTrackingType.WEBLINK.name) and url is not None:
        payload["URL"] = url

    if description:
        payload["Description"] = description

    print(payload)

    response = client.post_request(entity="learningContentItems", payload=payload)
    print(response)
    return CreatelearningcontentResponse(http_code=response.get("status_code", ""))
