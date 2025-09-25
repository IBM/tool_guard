from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class GetModel:
    """Represents the details of a single model of the asset in ServiceNow."""

    model_name: str
    system_id: str
    model_number: Optional[str] = None
    model_type: Optional[str] = None
    model_category: Optional[str] = None


@dataclass
class GetModelResponse:
    """A list of models of the assets configured in a ServiceNow deployment."""

    models: list[GetModel]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_model(
    model_category_system_id: str,
    name: Optional[str] = None,
    system_id: Optional[str] = None,
) -> GetModelResponse:
    """
    Gets a list of models of the assets configured in this ServiceNow deployment.

    Args:
        model_category_system_id: The system_id of the model category as returned by
            `get_model_category` tool within the ServiceNow API for retrieving any asset.
        name: The display_name of the model within the ServiceNow API for retrieving any model.
        system_id: The system_id of the model uniquely identifying them within the ServiceNow API
            for retrieving any model.

    Returns:
        A list of models.
    """

    client = get_servicenow_client()

    params = {
        "display_name": name,
        "cmdb_model_category": model_category_system_id,
        "system_id": system_id,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="cmdb_model", params=params)

    models_list: list[GetModel] = []
    for item in response["result"]:
        models_list.append(
            GetModel(
                model_name=item.get("display_name"),
                system_id=item.get("sys_id"),
                model_number=item.get("model_number"),
                model_type=item.get("type"),
                model_category=item.get("cmdb_model_category"),
            )
        )

    return GetModelResponse(models=models_list)
