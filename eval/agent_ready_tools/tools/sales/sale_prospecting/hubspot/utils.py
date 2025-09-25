from typing import Any, Dict


def hubspot_create_search_filter(contains_group: Dict[str, str]) -> Dict[str, Any]:
    """
    Create the filter dictionary for a Hubspot search.

    Args:
        contains_group: A key/value pair of the property and the value to search

    Returns:
        Filter dictionary
    """
    filters = []

    for key, value in contains_group.items():
        filt = {
            "propertyName": key,
            "operator": "CONTAINS_TOKEN",
            "value": f"*{value}*",
        }
        filters.append(filt)
    out = {"filterGroups": [{"filters": filters}]}
    return out
