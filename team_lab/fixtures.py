from storage import load_teams, save_teams


def generate_fixtures(data):

    teams = data["teams"]

    for fixture in data["fixtures"]:
        if fixture["status"] != "pending":
            raise ValueError("Game have already started. New teams can not be added,clear the current fixtures and try again")

    fixtures = []
    fixture_id = 1

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            print(teams[i])

            fixture = {
                "id": fixture_id,
                "home_team": teams[i]["id"],
                "away_team": teams[j]["id"],
                "status": "pending",
                "home_score": None,
                "away_score": None
            }

            fixtures.append(fixture)
            fixture_id += 1

    data["fixtures"] = fixtures

    save_teams(data)

    return fixtures


