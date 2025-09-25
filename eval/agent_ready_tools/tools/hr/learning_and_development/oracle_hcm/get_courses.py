import base64
import csv
import io
import typing
from typing import List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.oracle_hcm_soap_services.learningbireport import api
from agent_ready_tools.clients.oracle_soap_client import get_oracle_soap_client
from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.learning_bi_report_constants import (
    OracleBIReportConstants,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class CourseDetails:
    """Represent a course detail in Oracle HCM."""

    learning_id: str
    course_number: str
    course_name: str
    status: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    learning_category: Optional[str] = None
    course_description: Optional[str] = None


@dataclass
class CourseDetailsResponse:
    """Represents a list of course details from Oracle HCM."""

    course_details: List[CourseDetails]


def _get_courses_payload(
    learning_id: Optional[str] = None,
    learning_category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> api.ExternalReportWssserviceRunReportInput:
    """
    Returns a payload object of type RunReport filled.

    Args:
        learning_id: The learning id of the course in Oracle HCM.
        learning_category: The category of the course in Oracle HCM.
        start_date: The start of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).
        end_date: The end of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).

    Returns:
        The RunReport object
    """
    return api.ExternalReportWssserviceRunReportInput(
        body=api.ExternalReportWssserviceRunReportInput.Body(
            run_report=api.RunReport(
                report_request=api.ReportRequest(
                    parameter_name_values=api.ArrayOfParamNameValue(
                        item=[
                            api.ParamNameValue(
                                name="P_LEARNING_ID",
                                values=api.ArrayOfString(item=[learning_id if learning_id else ""]),
                            ),
                            api.ParamNameValue(
                                name="P_COURSE_CATEGORY",
                                values=api.ArrayOfString(
                                    item=[learning_category if learning_category else ""]
                                ),
                            ),
                            api.ParamNameValue(
                                name="P_START_DATE",
                                values=api.ArrayOfString(item=[start_date if start_date else ""]),
                            ),
                            api.ParamNameValue(
                                name="P_END_DATE",
                                values=api.ArrayOfString(item=[end_date if end_date else ""]),
                            ),
                        ]
                    ),
                    report_absolute_path=OracleBIReportConstants.COURSE_PATH.value,
                    size_of_data_chunk_download=OracleBIReportConstants.SIZE.value,
                )
            )
        )
    )


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_courses(
    name: Optional[str] = None,
    learning_id: Optional[str] = None,
    learning_category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: Optional[str] = "5",
    offset: Optional[str] = "0",
) -> Union[CourseDetailsResponse, str]:
    """
    Gets course details from Oracle HCM.

    Args:
        name: The name of the course in Oracle HCM.
        learning_id: The learning id of the course in Oracle HCM.
        learning_category: The category of the course in Oracle HCM.
        start_date: The start of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).
        end_date: The end of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).
        limit: The maximum number of courses to retrieve in a single API call. Defaults to
            5. Use this to control the size of the result set.
        offset: The number of courses to skip for pagination purposes. Use this to retrieve
            subsequent records when handling large datasets.

    Returns:
        The course details.
    """
    client = get_oracle_soap_client()

    payload = _get_courses_payload(
        learning_id=learning_id,
        learning_category=learning_category,
        start_date=start_date,
        end_date=end_date,
    )
    xml_response = client.get_courses(payload)
    if "<env:Fault>" and "Invalid parameters requested." in str(xml_response):
        return "Unable to get courses due to invalid parameters. Please check your input and try again."
    elif "<env:Fault>" in str(xml_response):
        return f"Unexpected error occured {xml_response!r}."

    @typing.no_type_check
    def encoded_data_to_internal_response(
        output: api.ExternalReportWssserviceRunReportOutput,
    ) -> CourseDetailsResponse:

        b64_data = output.body.run_report_response.run_report_return.report_bytes
        excel_binary_data = base64.b64decode(b64_data)

        csv_file = io.StringIO(excel_binary_data.decode("utf-8"))
        csv_reader = csv.DictReader(csv_file)

        json_data = list(csv_reader)

        course_details: list[CourseDetails] = []

        for data in json_data:
            if name is None or data.get("COURSE_NAME") == name:
                if not any(
                    course.course_name == data.get("COURSE_NAME") for course in course_details
                ):
                    course_details.append(
                        CourseDetails(
                            learning_id=data.get("LEARNING_ITEM_ID", ""),
                            course_number=data.get("LEARNING_ITEM_NUMBER", ""),
                            course_name=data.get("COURSE_NAME", ""),
                            course_description=data.get("COURSE_DESC", ""),
                            status=data.get("STATUS", ""),
                            start_date=data.get("START_DATE", ""),
                            end_date=data.get("END_DATE", ""),
                            learning_category=data.get("CO_ATTRIBUTE1", ""),
                        )
                    )
        if name and not course_details:
            return f"No course details found with the given course '{name}'."
        limit_int = int(limit) if limit is not None else 5
        offset_int = int(offset) if offset is not None else 0
        return CourseDetailsResponse(
            course_details=course_details[offset_int : offset_int + limit_int]
        )

    return encoded_data_to_internal_response(xml_response)
