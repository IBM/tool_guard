from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.jira.get_projects import GetProject, get_projects


def test_get_projects_first_item() -> None:
    """Tests that the first Jira project in the response matches the expected data."""

    # Define test data
    test_data: dict[str, str] = {
        "project_id": "10001",
        "project_type": "software",
        "project_name": "IBM WO AGENT PROJECT",
        "project_key": "IWAP",
        "project_lead": "Agent Tool",
    }

    # Inputs and expected pagination values
    limit = 50
    skip = 0
    output_limit = 50
    output_skip = 50

    with patch("agent_ready_tools.tools.IT.jira.get_projects.get_jira_client") as mock_get_client:
        # Setup mock client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "values": [
                {
                    "id": test_data["project_id"],
                    "projectTypeKey": test_data["project_type"],
                    "name": test_data["project_name"],
                    "key": test_data["project_key"],
                    "lead": {"displayName": test_data["project_lead"]},
                }
            ],
            "nextPage": "https://agenttool8.atlassian.net/rest/api/3/project/search?startAt=50&maxResults=50",
        }

        # Patch pagination helper if needed
        with patch(
            "agent_ready_tools.tools.IT.jira.get_projects.get_query_param_from_links"
        ) as mock_get_query_params:
            mock_get_query_params.return_value = {
                "startAt": str(output_skip),
                "maxResults": str(output_limit),
            }

            # Call the function
            response = get_projects(limit=limit, skip=skip)

            # Expected first project
            expected_first_project = GetProject(
                project_id=test_data["project_id"],
                project_type=test_data["project_type"],
                project_name=test_data["project_name"],
                project_key=test_data["project_key"],
                project_lead=test_data["project_lead"],
            )

            # Assertions
            assert response.projects[0] == expected_first_project
            assert response.limit == output_limit
            assert response.skip == output_skip

            # Assert correct API call
            mock_client.get_request.assert_called_once_with(
                entity="project/search",
                params={"maxResults": limit, "startAt": skip, "expand": "lead"},
            )
