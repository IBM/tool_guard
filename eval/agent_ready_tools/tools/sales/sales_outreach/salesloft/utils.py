from datetime import datetime
from typing import Optional


def format_datetime(dt_str: Optional[str]) -> Optional[str]:
    """Helper function to make 2023-06-05T08:08:03.288160-04:00 into a readable format."""
    if dt_str is None:
        return None
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime("%m/%d/%Y %I:%M%p").lower()
