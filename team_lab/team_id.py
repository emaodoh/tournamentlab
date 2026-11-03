from storage import load_teams


def generate_team_id(data):


    teams = data["teams"]
    """
    Generate the next unique team ID.

    Args:
        teams (list[dict]): Existing teams.

    Returns:
        str: New team ID e.g. T001, T002
    """

    if not teams:
        return "T001"

    highest_id = 0

    for team in teams:
        team_id = team["id"]

        # Validate ID format
        if not isinstance(team_id, str) or not team_id.startswith("T"):
            raise ValueError("Invalid team ID format")

        number_part = team_id[1:]

        if not number_part.isdigit():
            raise ValueError("Invalid team ID format")

        number = int(number_part)

        if number > highest_id:
            highest_id = number

    return f"T{highest_id + 1:03d}"
