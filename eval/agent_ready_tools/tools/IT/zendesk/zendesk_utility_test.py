from agent_ready_tools.tools.IT.zendesk.zendesk_utility import get_name_by_id


def test_get_name_by_id() -> None:
    """Tests the get_name_by_id function with mock data."""

    # Define test data
    data = [
        {"id": "903556258786", "name": "pratik"},
        {"id": "16722876680089", "name": "Alison Lucas"},
        {"id": "35376705273369", "name": "vae"},
    ]
    target_id = "16722876680089"
    expected_name = "Alison Lucas"

    # Call the function
    result = get_name_by_id(data, target_id)

    # Assertions
    assert result == expected_name
