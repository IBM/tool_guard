import typing

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.workday_soap_services.hr import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class BenefitPlanResponse:
    """Represents the response from getting benefit plans details of user in Workday."""

    benefit_plan_name: str
    coverage_begin_date: str
    deduction_begin_date: str
    coverage: str


def _get_my_benefit_plans_payload(
    user_id: str,
) -> api.GetWorkersInput:
    """
    Returns a payload object of type GetWorkersInput filled.

    Args:
        user_id: The user's user_id uniquely identifying them within the Workday API.

    Returns:
        The GetWorkersInput object
    """
    return api.GetWorkersInput(
        body=api.GetWorkersInput.Body(
            get_workers_request=api.GetWorkersRequest(
                request_references=api.WorkerRequestReferencesType(
                    worker_reference=[
                        api.WorkerObjectType(
                            id=[
                                api.WorkerObjectIdtype(
                                    value=user_id,
                                    type_value="WID",
                                ),
                            ]
                        ),
                    ]
                ),
                response_group=api.WorkerResponseGroupType(include_benefit_enrollments=True),
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_my_benefit_plans(user_id: str) -> BenefitPlanResponse:
    """
    Gets a user's benefit plans details in Workday.

    Args:
        user_id: The user's user_id uniquely identifying them within the Workday API.

    Returns:
        The user's benefit plans details.
    """
    client = get_workday_soap_client()

    payload = _get_my_benefit_plans_payload(user_id=user_id)
    xml_response = client.get_my_benefit_plans(payload)

    @typing.no_type_check
    def xml_to_internal_response(
        output: api.GetWorkersOutput,
    ) -> BenefitPlanResponse:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            Internal BenefitPlanResponse object.
        """
        response_kwargs = {}

        try:
            retirement_savings_coverage_data_node: api.WorkerRetirementSavingsDataType = (
                output.body.get_workers_response.response_data.worker[0]
                .worker_data.benefit_enrollment_data.retirement_savings_data.retirement_savings_period_data[
                    0
                ]
                .retirement_savings_coverage_data[0]
            )
        except (IndexError, AttributeError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        try:
            benefit_election_data_node: api.WorkerBenefitElectionDataType = (
                retirement_savings_coverage_data_node.benefit_election_data
            )
        except (IndexError, AttributeError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get benefit_plan_name from response XML
        try:
            response_kwargs["benefit_plan_name"] = str(
                benefit_election_data_node.benefit_plan_summary_data.benefit_provider_summary_data.benefit_provider_name
            )
            assert response_kwargs["benefit_plan_name"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get coverage_begin_date from response XML
        try:
            response_kwargs["coverage_begin_date"] = str(
                benefit_election_data_node.coverage_begin_date
            )
            assert response_kwargs["coverage_begin_date"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get deduction_begin_date from response XML
        try:
            response_kwargs["deduction_begin_date"] = str(
                benefit_election_data_node.deduction_begin_date
            )
            assert response_kwargs["deduction_begin_date"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get coverage from response XML
        if retirement_savings_coverage_data_node.employee_contribution_amount_data:
            response_kwargs["coverage"] = str(
                retirement_savings_coverage_data_node.employee_contribution_amount_data.contribution_amount_data
            )
        else:
            response_kwargs["coverage"] = str(
                retirement_savings_coverage_data_node.employee_contribution_percentage_data.election_percentage
            )

        return BenefitPlanResponse(**response_kwargs)

    return xml_to_internal_response(xml_response)
