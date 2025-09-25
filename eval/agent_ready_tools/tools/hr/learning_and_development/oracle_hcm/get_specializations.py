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
class SpecializationDetails:
    """Represent a specialization details in Oracle HCM."""

    learning_id: str
    specialization_number: str
    specialization_name: str
    section_name: str
    section_number: str
    course_name: str
    course_number: str
    specialization_start_date: Optional[str] = None
    specialization_end_date: Optional[str] = None
    specialization_short_description: Optional[str] = None
    specialization_description: Optional[str] = None


@dataclass
class SpecializationDetailsResponse:
    """Represents a list of specializations from Oracle HCM."""

    specialization_details: List[SpecializationDetails]


def _get_specializations_payload(
    learning_id: Optional[str] = None,
    status: Optional[str] = "Active",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> api.ExternalReportWssserviceRunReportInput:
    """
    Returns a payload object of type ExternalReportWssserviceRunReportInput filled.

    Args:
        learning_id: The learning_id of the specialization in Oracle HCM.
        status: The status of the specialization in Oracle HCM. Defaults to Active.
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
                                name="P_STATUS",
                                values=api.ArrayOfString(item=[status if status else ""]),
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
                    report_absolute_path=OracleBIReportConstants.SPECIALISATION_PATH.value,
                    size_of_data_chunk_download=OracleBIReportConstants.SIZE.value,
                )
            )
        )
    )


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_specializations(
    name: Optional[str] = None,
    learning_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: Optional[str] = "5",
    offset: Optional[str] = "0",
) -> Union[SpecializationDetailsResponse, str]:
    """
    Get learning specialization from Oracle HCM.

    Args:
        name: The name of the specialization in Oracle HCM.
        learning_id: The learning_id of the specialization in Oracle HCM.
        start_date: The start of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).
        end_date: The end of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).
        limit: The maximum number of specializations to retrieve in a single API call. Defaults to
            5. Use this to control the size of the result set.
        offset: The number of specializations to skip for pagination purposes. Use this to retrieve
            subsequent records when handling large datasets.

    Returns:
        List of available learning specializations.
    """
    client = get_oracle_soap_client()

    payload = _get_specializations_payload(
        learning_id=learning_id,
        start_date=start_date,
        end_date=end_date,
    )
    xml_response = client.get_specializations(payload)

    @typing.no_type_check
    def encoded_data_to_internal_response(
        output: api.ExternalReportWssserviceRunReportOutput,
    ) -> SpecializationDetailsResponse:

        b64_data = output.body.run_report_response.run_report_return.report_bytes

        excel_binary_data = base64.b64decode(b64_data)

        csv_file = io.StringIO(excel_binary_data.decode("utf-8"))
        csv_reader = csv.DictReader(csv_file)

        json_data = list(csv_reader)

        specialization_details: list[SpecializationDetails] = []

        for data in json_data:
            if name is None or data.get("SPECIALIZATION_NAME") == name:
                specialization_details.append(
                    SpecializationDetails(
                        learning_id=data.get("LEARNING_ITEM_ID", ""),
                        specialization_number=data.get("SPECIALIZATION_NUM", ""),
                        specialization_name=data.get("SPECIALIZATION_NAME", ""),
                        specialization_short_description=data.get("SPECIALIZATION_SHT_DES", ""),
                        specialization_description=data.get("SPECIALIZATION_DES", ""),
                        specialization_start_date=data.get("SPECIALIZATION_DATE", ""),
                        specialization_end_date=data.get("SPL_END_DATE", ""),
                        section_name=data.get("SECTION_NAME", ""),
                        section_number=data.get("SECTION_NUMBER", ""),
                        course_name=data.get("ACTIVITIES_NAME", ""),
                        course_number=data.get("ACTIVITIES_NUMBER", ""),
                    )
                )
        if name and not specialization_details:
            return f"No specialization details found with the given specialization '{name}'."
        limit_int = int(limit) if limit is not None else 5
        offset_int = int(offset) if offset is not None else 0
        return SpecializationDetailsResponse(
            specialization_details=specialization_details[offset_int : offset_int + limit_int]
        )

    return encoded_data_to_internal_response(xml_response)
