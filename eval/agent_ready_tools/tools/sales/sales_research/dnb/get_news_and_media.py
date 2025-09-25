# Assisted by watsonx Code Assistant
from datetime import datetime, timedelta
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_utils import process_dnb_error
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


@dataclass
class NewsItem:
    """Represents a single news item from the News and Media API."""

    reported_date: Optional[str] = None
    news_categories: Optional[List[str]] = None
    title: Optional[str] = None
    content: Optional[str] = None
    reference_url: Optional[str] = None


@dataclass
class NewsItems:
    """Represents a list of news item from the News and Media API."""

    data: Optional[List[NewsItem]] = None


DAYS_BACK: float = float(90)
MAX_ITEMS: int = 10


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def get_news_and_media(
    duns_number: str,
) -> Optional[NewsItems] | ErrorResponse:
    """
    Retrieves recent news and media content for a given D-U-N-S number using the DNB News and Media
    API.

    Args:
        duns_number: The D-U-N-S number for the entity.

    Returns:
        A list of NewsItem objects if successful, or None if there are no NewsItems
        returned. Each object contains:
            - reported_date (str): The date of the event described in the news item.
            - news_categories (List[str]): The classification category of the news item.
            - title (str): Text that contains the title of the news item.
            - content (str): The body of the news item.
            - reference_url (str): Text that records the location of the web-based news item content.
    """
    # TODO: Filter per news category

    # Retrieve the preconfigured DNB client using the helper function.
    client = get_dnb_client(entitlement=DNBEntitlements.SALES)

    # Build query parameters with the required fields.
    query_parameters = {
        "duns": duns_number,
        "productId": "namstd",  # Product ID for the News and Media, Standard API.
        "versionId": "v1",
    }

    # Calculate start date as 3 months ago from today.
    today = datetime.now().date()
    start_date = (today - timedelta(days=DAYS_BACK)).isoformat()
    query_parameters["startDate"] = start_date

    # Make the GET request using the DNB client.
    response = client.get_request(
        version="v1",
        category="newsandmedia",
        params=query_parameters,
    )

    # Check if we have an error in the response.
    api_url = "https://plus.dnb.com/v1/newsandmedia"
    url_params = query_parameters
    error_response = process_dnb_error(response, api_url, url_params)

    # Extract raw news items from the response.
    raw_news_items = response.get("newsItems")
    # If nothing returned for raw_news_items, then return error_response, otherwise process the newsItems
    if not raw_news_items or not isinstance(raw_news_items, list):
        # Manually over-ride the default "No news found" error message
        if error_response.message == "Requested product not available due to insufficient data.":
            error_response.message = "No news found for this client"
        return error_response
    else:
        # Limit the list to the max returned items.
        limited_news_items = raw_news_items[:MAX_ITEMS]
        news_item_list = []  # New list to hold the converted NewsItem objects.
        for item in limited_news_items:
            # Create a NewsItem instance for each news item.
            timestamp_str = item.get("reportedTimeStamp", "")
            news_item = NewsItem(
                reported_date=(
                    datetime.fromisoformat(timestamp_str).strftime("%Y-%m-%d")
                    if timestamp_str
                    else ""
                ),
                news_categories=item.get("newsCategories", []),
                title=item.get("title", ""),
                content=item.get("content", ""),
                reference_url=item.get("referenceURL", ""),
            )
            news_item_list.append(news_item)

        return NewsItems(data=news_item_list)
