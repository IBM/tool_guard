from functools import wraps
import inspect
import json
from typing import Any, Callable, Dict

from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse


def coupa_format_error_string(response: Dict[str, Dict]) -> str:
    """
    Format API response to JSON string.

    Args:
        response: API response

    Returns:
        str: JSON string output
    """

    errors_dict = response.get("errors", {})
    errors_dict.pop("warnings", None)

    return json.dumps(errors_dict)


# TODO: DO NOT USE, revisit with @tool decorator and fn={path}
def coupa_validate_and_strip_strings(func: Callable) -> Callable:
    """
    Decorator to validate string parameters by making sure required string parameters are not None
    or empty string "" after stripping, and Optional string parameters should still be stripped if
    provided. Using temporarily to pass pydantic errors until a better and more unified solution
    comes along.

    Args:
        func: The tool function that this decorator is wrapped around.

    Returns:
        The wrapped function with validated and stripped string args.
    """
    sig = inspect.signature(func)  # get full signature of function (param names, types, defaults)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound = sig.bind(*args, **kwargs)  # bind args to function signature
        bound.apply_defaults()  # fill in default values for any missing optional args (like Optional[str] = None)

        errors = []

        for name, param in sig.parameters.items():
            val = bound.arguments[name]

            # required: must not be None or empty string
            if param.default is inspect.Parameter.empty:
                if val is None or (
                    (isinstance(val, str)) and (val.strip() == "" or val.strip() == "null")
                ):
                    errors.append(f"Required parameter '{name}' must be a non-empty string.")
                elif isinstance(val, str):
                    # strip and update arg in-place
                    bound.arguments[name] = val.strip()
            else:  # Optional: can be None, but if not None, must not be empty
                if val is not None:
                    if (isinstance(val, str)) and (val.strip() == "" or val.strip() == "null"):
                        errors.append(f"Optional parameter '{name}' cannot be empty if provided.")
                    elif isinstance(val, str):
                        # strip and update arg in-place
                        bound.arguments[name] = val.strip()

        if errors:
            return ToolResponse(
                success=False,
                message=" ".join(f"{msg}" for msg in errors),
            )

        # call original function with the modified stripped inplace values
        return func(*bound.args, **bound.kwargs)

    return wrapper
