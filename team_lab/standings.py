"""Engineer B: standings calculated from played fixtures, never stored separately."""

def compute_standings(teams, fixtures):

    
    table = {}
    for team in teams:
        team_id = team["id"]
        if team_id in table:
            raise ValueError(f"Duplicate team ID: {team_id}")
        table[team_id] = {
            "team_id": team_id,
            "team": team["name"],
            "normalized_name": team["name"].strip().casefold(),
            "played": 0, "wins": 0, "draws": 0, "losses": 0,
            "goals_for": 0, "goals_against": 0,
            "goal_difference": 0, "points": 0,
        }

    for fixture in fixtures:
        home_id = fixture.get("home_team")
        away_id = fixture.get("away_team")
        if home_id not in table or away_id not in table:
            raise ValueError(f"Fixture {fixture.get('id')} references an unknown team.")
        if home_id == away_id:
            raise ValueError(f"Fixture {fixture.get('id')} cannot be a team playing itself.")

        status = fixture.get("status")
        home_score = fixture.get("home_score")
        away_score = fixture.get("away_score")

        if status == "pending":
            if home_score is not None or away_score is not None:
                raise ValueError(f"Pending fixture {fixture.get('id')} has scores.")
            continue
        if status != "played":
            raise ValueError(f"Fixture {fixture.get('id')} has invalid status.")
        if (not _valid_score(home_score) or not _valid_score(away_score)):
            raise ValueError(f"Played fixture {fixture.get('id')} has invalid scores.")

        home = table[home_id]
        away = table[away_id]
        home["played"] += 1
        away["played"] += 1
        home["goals_for"] += home_score
        home["goals_against"] += away_score
        away["goals_for"] += away_score
        away["goals_against"] += home_score

        if home_score > away_score:
            home["wins"] += 1
            away["losses"] += 1
            home["points"] += 3
        elif home_score < away_score:
            away["wins"] += 1
            home["losses"] += 1
            away["points"] += 3
        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

    for row in table.values():
        row["goal_difference"] = row["goals_for"] - row["goals_against"]

    return sorted(
        table.values(),
        key=lambda row: (
            -row["points"],
            -row["goal_difference"],
            -row["goals_for"],
            row["normalized_name"],
        ),
    )


def _valid_score(score):
    return isinstance(score, int) and not isinstance(score, bool) and score >= 0


def league_complete(fixtures):
    """A season is complete only when every fixture has a played status."""
    return all(fixture.get("status") == "played" for fixture in fixtures)


def champion_report(teams, fixtures):
    """Return a report dictionary; champion is withheld until all fixtures are played."""
    standings = compute_standings(teams, fixtures)
    if not league_complete(fixtures):
        return {
            "status": "in progress",
            "champion": None,
            "standings": standings,
            "message": "League in progress: complete all fixtures to determine the champion.",
        }

    if not standings:
        return {
            "status": "complete",
            "champion": None,
            "standings": standings,
            "message": "Season complete, but no teams are registered.",
        }

    top = standings[0]
    return {
        "status": "complete",
        "champion": top["team"],
        "standings": standings,
        "message": f"Champion: {top['team']}",
    }
