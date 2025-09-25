from datetime import datetime
from typing import Any, List, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from xsdata.models.datatype import XmlDate

from agent_ready_tools.apis.workday_soap_services.hr import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class DisabilityResponse:
    """Represents a disability response in Workday."""

    disability_reference_id: str
    disability_id: str
    status_date: str
    date_known: str
    end_date: str


def _update_disability_status_payload(
    user_id: str,
    disability_reference_id: str,
    disability_status_date: str,
    disability_date_known: str,
    disability_end_date: str,
) -> api.ChangePersonalInformationInput:
    """
    Returns a payload object of type ChangePersonalInformationInput filled.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        disability_reference_id: The disability_reference_wid of the disability, as specified by the
            `get_disabilities` tool.
        disability_status_date: The last updated date of the disability status in ISO 8601 format
            (e.g., YYYY-MM-DD).
        disability_date_known: The date the employee first learned about the Disability in ISO 8601
            format (e.g., YYYY-MM-DD).
        disability_end_date: The end date of employee's disability in ISO 8601 format (e.g., YYYY-
            MM-DD).

    Returns:
        The ChangePersonalInformationInput object
    """

    disability_status_date_dt = datetime.fromisoformat(disability_status_date)
    disability_date_known_dt = datetime.fromisoformat(disability_date_known)
    disability_end_date_dt = datetime.fromisoformat(disability_end_date)
    return api.ChangePersonalInformationInput(
        body=api.ChangePersonalInformationInput.Body(
            change_personal_information_request=api.ChangePersonalInformationRequest(
                version="v43.2",
                change_personal_information_data=api.ChangePersonalInformationBusinessProcessDataType(
                    person_reference=api.RoleObjectType(
                        id=[api.RoleObjectIdtype(value=user_id, type_value="WID")]
                    ),
                    personal_information_data=api.ChangePersonalInformationDataType(
                        disability_information_data=api.DisabilityInformationDataType(
                            disability_status_information_data=[
                                api.DisabilityStatusInformationDataType(
                                    disability_status_data=api.DisabilityStatusSubDataType(
                                        disability_reference=api.DisabilityObjectType(
                                            id=[
                                                api.DisabilityObjectIdtype(
                                                    value=disability_reference_id, type_value="WID"
                                                )
                                            ]
                                        ),
                                        disability_status_date=XmlDate(
                                            disability_status_date_dt.year,
                                            disability_status_date_dt.month,
                                            disability_status_date_dt.day,
                                        ),
                                        disability_date_known=XmlDate(
                                            disability_date_known_dt.year,
                                            disability_date_known_dt.month,
                                            disability_date_known_dt.day,
                                        ),
                                        disability_end_date=XmlDate(
                                            disability_end_date_dt.year,
                                            disability_end_date_dt.month,
                                            disability_end_date_dt.day,
                                        ),
                                    )
                                )
                            ]
                        )
                    ),
                ),
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def update_disability_status(
    user_id: str,
    disability_reference_id: str,
    disability_status_date: str,
    disability_date_known: str,
    disability_end_date: str,
) -> DisabilityResponse:
    """
    Update user's disability status in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        disability_reference_id: The disability_reference_wid of the disability, as specified by the
            `get_disabilities` tool.
        disability_status_date: The last updated date of the disability status in ISO 8601 format
            (e.g., YYYY-MM-DD).
        disability_date_known: The date the employee first learned about the Disability in ISO 8601
            format (e.g., YYYY-MM-DD).
        disability_end_date: The end date of employee's disability in ISO 8601 format (e.g., YYYY-
            MM-DD).

    Returns:
        The result of the update to the user's disability.
    """
    client = get_workday_soap_client()

    xml_response = client.update_disability_status(
        _update_disability_status_payload(
            user_id=user_id,
            disability_reference_id=disability_reference_id,
            disability_status_date=disability_status_date,
            disability_date_known=disability_date_known,
            disability_end_date=disability_end_date,
        )
    )

    def _get_xml_value(obj: object, attr_chain: List[Union[str, int]]) -> str:
        """
        Return value from an XML object by path.

        Args:
            obj: Xml object
            attr_chain: Path in form of an array.

        Returns:
            The value
        """
        current: Any = obj
        path: List[str] = []

        for attr in attr_chain:
            path.append(str(attr))
            try:
                if isinstance(attr, int):  # Handle list indexing
                    current = current[attr]
                else:
                    current = getattr(current, attr)
            except AttributeError:
                raise AttributeError(f"Missing XML attribute: {'.'.join(path)}")
            except IndexError:
                raise IndexError(f"Missing index in XML list: {'.'.join(path)}")

        return current

    disability_status_data = _get_xml_value(
        xml_response,
        [
            "body",
            "change_personal_information_response",
            "personal_information_data",
            "disability_information_data",
            "disability_status_information_data",
            0,
            "disability_status_data",
        ],
    )

    disability_wid = _get_xml_value(
        disability_status_data, ["disability_reference", "id", 0, "value"]
    )
    disability_id = _get_xml_value(
        disability_status_data, ["disability_reference", "id", 1, "value"]
    )

    return DisabilityResponse(
        disability_reference_id=disability_wid,
        disability_id=disability_id,
        status_date=disability_status_date,
        date_known=disability_date_known,
        end_date=disability_end_date,
    )
