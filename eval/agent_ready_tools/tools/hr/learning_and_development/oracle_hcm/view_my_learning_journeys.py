from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass(frozen=True)
class LearningJourney:
    """Represents a learning journey in Oracle HCM."""

    journey_id: str
    created_by: str
    favourite_flag: str
    level: str
    category_meaning: str
    level_meaning: str
    name: str
    background_thumbnail_url: Optional[str] = None
    description: Optional[str] = None


@dataclass
class LearningJourneysResponse:
    """A list of learning journeys configured for an Oracle HCM deployment."""

    learning_journeys: list[LearningJourney]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def view_my_learning_journeys(limit: int = 20, offset: int = 0) -> LearningJourneysResponse:
    """
    Gets a list of learning journeys configured for an Oracle HCM deployment.

    Args:
        limit: The maximum number of items to retrieve (default: 20).
        offset: The starting offset for pagination (default: 0).

    Returns:
        A response containing a list of learning journeys.
    """

    client = get_oracle_hcm_client()
    response = client.post_request(
        entity="journeys/action/findByAdvancedSearchQuery",
        headers={"Content-Type": "application/vnd.oracle.adf.action+json"},
        payload={
            "limit": limit,
            "offset": offset,
            "filters": [
                {"name": ["Mode"], "value": ["ORA_PERSONAL"]},
                {"name": ["Category"], "value": ["ORA_LEARN"]},
            ],
            "displayFields": [
                "JourneyId",
                "CategoryMeaning",
                "Name",
                "Description",
                "BackgroundThumbnailURL",
                "Level",
                "FavouriteFlag",
                "LevelMeaning",
                "CreatedBy",
            ],
        },
    )

    learning_journeys: List[LearningJourney] = [
        LearningJourney(
            journey_id=email.get("JourneyId", ""),
            description=email.get("Description", ""),
            created_by=email.get("CreatedBy", ""),
            favourite_flag=email.get("FavouriteFlag", ""),
            level=email.get("Level", ""),
            category_meaning=email.get("CategoryMeaning", ""),
            background_thumbnail_url=email.get("BackgroundThumbnailURL", ""),
            level_meaning=email.get("LevelMeaning", ""),
            name=email.get("Name", ""),
        )
        for email in response.get("items", [])
    ]

    return LearningJourneysResponse(learning_journeys=learning_journeys)
