from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.seismic_client import get_seismic_client
from agent_ready_tools.utils.date_conversion import iso_8601_datetime_convert_to_date
from agent_ready_tools.utils.tool_credentials import SEISMIC_CONNECTIONS


@dataclass
class LibraryContent:
    """Represents the content of a library document in Seismic."""

    id: str
    name: str
    version: str
    # latest_version: str
    created_at: str
    modified_at: str
    type: str
    # format: Optional[str]
    is_checked_out: bool
    is_deleted: bool
    deleted_at: Optional[str]
    # deleted_by_user_id: Optional[str]
    # deleted_by_user_name: Optional[str]
    is_published: bool
    is_available_in_profile: bool
    # published_version_expires_at: Optional[str]
    # latest_library_content_version_created_at: str
    # latest_library_content_version_created_by: Optional[str]
    # latest_library_content_version_created_by_username: Optional[str]
    # latest_library_content_version_id: str
    # latest_library_content_version_size: Optional[int]
    # latest_library_content_version_status: Optional[str]
    # latest_library_content_version_expires_at: Optional[str]
    library_url: str
    # doc_center_url: Optional[str]
    # news_center_url: Optional[str]
    owner_id: str
    owner_username: str
    # owner_email: Optional[str]
    teamsite_id: str
    teamsite_name: Optional[str]
    # preview_image_id: str # no image support so unsure if we're supporting this
    # preview_image_url: str
    # thumbnail_image_id: str
    # thumbnail_image_url: str
    description: Optional[str]
    # short_id: Optional[str]
    # parent_folder_library_content_id: Optional[str]
    # library_path: str
    # has_planner_associations: bool
    # has_program_associations: bool
    # associated_program_library_content_id: str
    # origin_type: Optional[str]
    last_modified: str
    # content_status: Optional[str]
    # published_version_id: Optional[str]
    # published_at: Optional[str]
    # published_by_user_id: Optional[str]
    # published_by_username: Optional[str]
    # add_library_content_to_profile_at: Optional[str]
    # unpublished_at: Optional[str]


@dataclass
class LibraryContentsResponse:
    """Represents the response from getting the library contents."""

    library_contents: List[LibraryContent]


@tool(expected_credentials=SEISMIC_CONNECTIONS)
def get_all_library_contents(
    limit: Optional[str] = "10",
    modified_at_start_time: Optional[str] = None,
    modified_at_end_time: Optional[str] = None,
    last_modified_start_time: Optional[str] = None,
    last_modified_end_time: Optional[str] = None,
    created_at_start_time: Optional[str] = None,
    created_at_end_time: Optional[str] = None,
) -> LibraryContentsResponse:
    """
    Retrieves all contents of a library from Seismic.

    Args:
        limit: Optional, The maximum number of items to return.
        modified_at_start_time: Optional, The start of a date range filter for modified_at values in
            ISO 8601 format (e.g., YYYY-MM-DD).
        modified_at_end_time: Optional, The end of a date range filter for modified_at values in ISO
            8601 format (e.g., YYYY-MM-DD).
        last_modified_start_time: Optional, The start of a date range filter for last_modified
            values in ISO 8601 format (e.g., YYYY-MM-DD).
        last_modified_end_time: Optional, The end of a date range filter for last_modified values in
            ISO 8601 format (e.g., YYYY-MM-DD).
        created_at_start_time: Optional, The start of a date range filter for created_at values in
            ISO 8601 format (e.g., YYYY-MM-DD).
        created_at_end_time: Optional, The end of a date range filter for created_at values in ISO
            8601 format (e.g., YYYY-MM-DD).

    Returns:
        The list of the library contents.
    """

    client = get_seismic_client()

    response = client.get_request_list(
        endpoint="libraryContents",
        category=client.REPORTING,
        params={
            "limit": limit,
            "modifiedAtStartTime": modified_at_start_time,
            "modifiedAtEndTime": modified_at_end_time,
            "lastModifiedStartTime": last_modified_start_time,
            "lastModifiedEndTime": last_modified_end_time,
            "createdAtStartTime": created_at_start_time,
            "createdAtEndTime": created_at_end_time,
        },
    )

    library_contents: List[LibraryContent] = []
    for entry in response:
        # TODO: Explore Schema.load(response) in followup refactoring PR
        library_contents.append(
            LibraryContent(
                id=entry.get("id", ""),
                name=entry.get("name", ""),
                version=entry.get("version", ""),
                created_at=iso_8601_datetime_convert_to_date(entry.get("createdAt", "")),
                modified_at=iso_8601_datetime_convert_to_date(entry.get("modifiedAt", "")),
                type=entry.get("type", ""),
                is_checked_out=entry.get("isCheckedOut", False),
                is_deleted=entry.get("isDeleted", False),
                deleted_at=(
                    iso_8601_datetime_convert_to_date(entry.get("deletedAt", ""))
                    if entry.get("deletedAt")
                    else None
                ),
                is_published=entry.get("isPublished", False),
                is_available_in_profile=entry.get("isAvailableInProfile", False),
                library_url=entry.get("libraryUrl", ""),
                owner_id=entry.get("ownerId", ""),
                owner_username=entry.get("ownerUsername", ""),
                teamsite_id=entry.get("teamsiteId", ""),
                teamsite_name=entry.get("teamsiteName", None),
                description=entry.get("description", None),
                last_modified=iso_8601_datetime_convert_to_date(entry.get("lastModified", "")),
            )
        )

    return LibraryContentsResponse(library_contents=library_contents)
