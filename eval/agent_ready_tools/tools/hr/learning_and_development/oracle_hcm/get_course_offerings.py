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
class OfferingDetails:
    """Represent a offering detail in Oracle HCM."""

    offering_number: str
    offering_name: str
    offering_status: str
    offering_type: str
    offering_description: Optional[str] = None
    offering_dates: Optional[str] = None


@dataclass
class OfferingDetailsResponse:
    """Represents a list of offering details from Oracle HCM."""

    offering_details: List[OfferingDetails]


def _get_course_offerings_payload() -> api.ExternalReportWssserviceRunReportInput:
    """
    Returns a payload object of type RunReport filled.

    Returns:
        The RunReport object
    """
    return api.ExternalReportWssserviceRunReportInput(
        body=api.ExternalReportWssserviceRunReportInput.Body(
            run_report=api.RunReport(
                report_request=api.ReportRequest(
                    report_absolute_path=OracleBIReportConstants.COURSE_PATH.value,
                    size_of_data_chunk_download=OracleBIReportConstants.SIZE.value,
                )
            )
        )
    )


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_course_offerings(course_name: str) -> Union[OfferingDetailsResponse, str]:
    """
    Gets offering details from Oracle HCM.

    Args:
        course_name: The name of the course in Oracle HCM.

    Returns:
        The offering details.
    """
    client = get_oracle_soap_client()

    payload = _get_course_offerings_payload()
    xml_response = client.get_course_offerings(payload)

    @typing.no_type_check
    def encoded_data_to_internal_response(
        output: api.ExternalReportWssserviceRunReportOutput,
    ) -> OfferingDetailsResponse:

        b64_data = output.body.run_report_response.run_report_return.report_bytes
        excel_binary_data = base64.b64decode(b64_data)

        csv_file = io.StringIO(excel_binary_data.decode("utf-8"))
        csv_reader = csv.DictReader(csv_file)

        json_data = list(csv_reader)

        offering_details: list[OfferingDetails] = []
        course_exists = any(course.get("COURSE_NAME") == course_name for course in json_data)
        if not course_exists:
            return f"There is no course with '{course_name}'. Please provide a valid course name."

        for data in json_data:
            if data.get("COURSE_NAME") == course_name:
                offering_details.append(
                    OfferingDetails(
                        offering_number=data.get("OFFER_NUMBER", ""),
                        offering_name=data.get("OFFER_NAME", ""),
                        offering_description=data.get("OFFER_DESC", ""),
                        offering_status=data.get("OFFER_STATUS", ""),
                        offering_type=data.get("OFFERING_TYPE", ""),
                        offering_dates=data.get("OFFERING_DATES", ""),
                    )
                )
        return OfferingDetailsResponse(offering_details=offering_details)

    return encoded_data_to_internal_response(xml_response)
