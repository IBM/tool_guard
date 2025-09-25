import typing

#from fuzzywuzzy import process
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.workday_soap_services.hr import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class WorkdayRelationship:
    """A relationship type configured for a Workday deployment."""

    relationship_id: str
    relationship_name: str


def _get_relationship_id_payload() -> api.GetRelatedPersonRelationshipsInput:
    """
    Returns a payload object of type GetRelatedPersonRelationshipsInput filled.

    Returns:
        The GetRelatedPersonRelationshipsInput object.
    """
    return api.GetRelatedPersonRelationshipsInput(
        body=api.GetRelatedPersonRelationshipsInput.Body(
            get_related_person_relationships_request=api.GetRelatedPersonRelationshipsRequest()
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_relationship_id(relation: str) -> str:
    """
    Get Workday's ID for a relationship.

    Args:
        relation: The related person's relationship .

    Returns:
        The relationship's ID.
    """
    client = get_workday_soap_client()
    xml_response = client.get_related_person_relationships(_get_relationship_id_payload())

    @typing.no_type_check
    def extract_relationship_id_from_xml_response(
        output: api.GetRelatedPersonRelationshipsOutput,
    ) -> str:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            relationship ID.
        """

        try:
            all_relationships = (
                output.body.get_related_person_relationships_response.response_data.related_person_relationship
            )
            relationships = []
            for rel in all_relationships:
                try:
                    relation_id = rel.related_person_relationship_reference.id[0].value
                    relation_name = rel.related_person_relationship_data[0].relationship_name
                    relationships.append(
                        WorkdayRelationship(
                            relationship_id=relation_id, relationship_name=relation_name
                        )
                    )

                except (IndexError, AttributeError) as e:
                    raise ValueError(
                        f"unexpected GetRelatedPersonRelationshipsOutput format: {e}\nraw output:\n{output}"
                    )
            query_object = WorkdayRelationship(relationship_id="", relationship_name=relation)
            top_n_options = [
                option
                for option, score in process.extract(
                    query_object, relationships, processor=lambda x: x.relationship_name, limit=1
                )
            ]
            return top_n_options[0].relationship_id
        except (IndexError, AttributeError) as e:
            raise ValueError(
                f"unexpected GetRelatedPersonRelationshipsOutput format: {e}\nraw output:\n{output}"
            )

    return extract_relationship_id_from_xml_response(xml_response)
