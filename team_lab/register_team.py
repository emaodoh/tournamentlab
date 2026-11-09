from storage import save_teams, load_teams
from team_id import generate_team_id


def register_team(name):
    """
    Register a new team and save it to JSON.

    Args:
        name (str): Team display name.

    Returns:
        dict: The newly created team.
    """

    # Load tournament data
    data = load_teams()

    for fixture in data["fixtures"]:
        if fixture["status"] != "pending":
            raise ValueError("Game have already started. New teams can not be added,clear the current fixtures and try again")

    # Validate team name
    name = name.strip()

    if not name:
        raise ValueError("Team name cannot be empty")

    # Check duplicate names
    for team in data["teams"]:
        if team["name"].lower() == name.lower():
            raise ValueError("Team already exists")

    # Generate ID
    new_team = {
        "id": generate_team_id(data),
        "name": name
    }

    # Add team
    data["teams"].append(new_team)

    # Save tournament data
    save_teams(data)

    return new_team

