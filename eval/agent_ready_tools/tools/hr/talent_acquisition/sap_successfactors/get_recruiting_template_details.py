from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class GetRecruitingTemplateDetailsResponse:
    """Represents the response of the recruiting template details in SAP SuccessFactors."""

    template_id: Optional[str]
    template_name: Optional[str]
    description: Optional[str]
    http_code: Optional[int]
    message: Optional[str]


def get_template_value(message: str, key_name: str) -> Optional[str]:
    """
    Retrieves the value associated with a specified key from a message string, from the api response
    of the `get_recruiting_template_details` method.

    Args:
        message: The message string from the SAP SuccessFactors API response for the `/getRecruitingTemplate` request.
        key_name: The name of the field (id, name and description) to extract from the message.

    Returns:
        The extracted value as a string, or None if not found or malformed.
    """
    try:
        key = message.split(f"{key_name}=")
        if len(key) < 2:
            return None

        value = key[1].split(",")
        if not value:
            return None

        value_str = value[0].strip()
        return value_str if value_str else None

    except (IndexError, AttributeError):
        return None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_recruiting_template_details(template_name: str) -> GetRecruitingTemplateDetailsResponse:
    """
    Gets the recruiting template details in SAP SuccessFactors.

    Args:
        template_name: The specific name of the recruiting template for which the user wants to retrieve details.

    Returns:
        The API response for retrieving the details of recruiting template, in the form of a `GetRecruitingTemplateDetailsResponse` object.
    """

    client = get_sap_successfactors_client()

    params = {"templateType": "JOBREQ", "templateName": f"'{template_name}'"}
    try:
        response = client.get_request(entity="getRecruitingTemplate", params=params)
    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        message = (
            error_response.get("error", {}).get("message", {}).get("value", None)
            if error_response
            else None
        )
        if not message:
            message = "An unexpected error occurred."

        return GetRecruitingTemplateDetailsResponse(
            template_id=None,
            template_name=None,
            description=None,
            http_code=(
                e.response.status_code
                if e.response and e.response.status_code
                else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )

    result = response.get("d", {})

    message = result.get("getRecruitingTemplate", "")
    if message == "[]":
        return GetRecruitingTemplateDetailsResponse(
            template_id=None,
            template_name=None,
            description=None,
            http_code=response.get("status_code", HTTPStatus.OK),
            message="Recruiting template details do not exist.",
        )
    template_id = get_template_value(message, "id")
    name = get_template_value(message, "name")
    description = get_template_value(message, "description")

    return GetRecruitingTemplateDetailsResponse(
        template_id=template_id,
        template_name=name,
        description=description,
        http_code=response.get("status_code", HTTPStatus.OK),
        message=None,
    )
