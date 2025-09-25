from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.list_sections import Section, list_sections


def test_list_sections() -> None:
    """Verifies that the `list_sections` tool can successfully retrieve Zendesk helpcenter
    Sections."""

    # Define the test data
    test_data: dict[str, int | str] = {
        "section_id": "48417511764761",
        "section_name": "Getting started",
        "sections_locale": "en-us",
    }

    # Inputs and expected pagination values
    per_page = 5
    page = 1
    output_page = 2
    output_per_page = 5

    # patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.list_sections.get_zendesk_client"
    ) as mock_zendesk_client:
        # create mock client
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client

        # mock the API response
        mock_client.get_request.return_value = {
            "sections": [
                {
                    "id": test_data["section_id"],
                    "name": test_data["section_name"],
                    "locale": test_data["sections_locale"],
                }
            ],
            "next_page": "https://d3v-ibmappconn.zendesk.com/api/v2/help_center/en-us/sections?page=2&per_page=5",
        }

        with patch(
            "agent_ready_tools.utils.get_id_from_links.get_query_param_from_links"
        ) as mock_get_query_param:
            mock_get_query_param.return_value = {
                "name": test_data["section_name"],
                "page": str(output_page),
                "per_page": str(output_per_page),
            }

            # List Zendesk Sections.
            response = list_sections(
                section_name=test_data["section_name"], per_page=per_page, page=page
            )

            # Ensure that list_sections() has executed and returned proper values.
            expected_output = Section(
                section_id=str(test_data["section_id"]),
                section_name=str(test_data["section_name"]),
                section_locale=str(test_data["sections_locale"]),
            )

            assert response.sections[0] == expected_output
            assert response.page == output_page
            assert response.per_page == output_per_page

            # Ensure the API call was made with expected parameters
            mock_client.get_request.assert_called_once_with(
                entity="help_center/en-us/sections",
                params={
                    "name": test_data["section_name"],
                    "per_page": per_page,
                    "page": page,
                },
            )
