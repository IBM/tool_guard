
from typing import List, Set
from toolguard.data_types import Domain, ToolPolicyItem
from programmatic_ai import generative

# from toolguard.gen_py.prompts.python_code import PythonCodeModel

@generative
async def create_guard_from_doc(prev_impl: str, domain: Domain, policy_document: str, tool_name: str, dependent_tool_names: List[str], review_comments: List[str])-> str:
    """
    Improve the previous tool-call guard implementation (in Python) so that it fully adheres to the policy document and addresses all review comments.

    Args:
        prev_impl (str): The previous implementation of the tool-call check.
        domain (Domain): Python code defining available data types and other tool interfaces.
        policy_document (str): The document with business policies in natural language; the policies should be enforced in code.
        tool_name (str): The tool we would like to generate a guard for.
        dependent_tool_names (List[str]): Names of other tools that this tool may call to obtain required information.
        review_comments (List[str]): Review feedback on the current implementation (e.g., pylint errors, failed unit tests).

    Returns:
        str: The implementation of the tool-call check.

    Implementation Rules:
        - Do not modify the function signature, parameter names, or type annotations.
        - All policy requirements related to the tool must be validated.
        - Keep the implementation simple and well-documented.
        - Only validate the tool-call arguments; never call the tool itself.
        - Generate code that enforces the given policy only, do not generate any additional logic that is not explicitly mentioned in the policy.

    **Example: ** 
you should return something like:
```python
from typing import *
from airline.airline_types import *
from airline.i_airline import I_Airline

def guard_book_reservation(api: I_Airline, user_id: str, passengers: list[Passenger]):
    \"\"\"
    make sure the reservation has at least one passenger
    \"\"\"
    if len(passengers) <= 0:
        raise PolicyViolationException("at least one passenger is required")
```
    """
    ...
