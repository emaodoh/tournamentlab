"""Small CLI shell for Engineer B.

Engineer A's layer is expected to load/save and provide teams and fixtures.
This module receives those records and implements result/standings commands.
"""
from storage import save_teams
from results import record_result
from standings import compute_standings, champion_report


def print_standings(teams, fixtures):
    rows = compute_standings(teams, fixtures)
    print("\nLEAGUE STANDINGS")
    print("-" * 94)
    print(f"{'Rank':<5}{'Team':<18}{'P':>3}{'W':>3}{'D':>3}{'L':>3}"
          f"{'GF':>5}{'GA':>5}{'GD':>5}{'Pts':>6}")
    print("-" * 94)
    for rank, row in enumerate(rows, start=1):
        print(f"{rank:<5}{row['team']:<18}{row['played']:>3}"
              f"{row['wins']:>3}{row['draws']:>3}{row['losses']:>3}"
              f"{row['goals_for']:>5}{row['goals_against']:>5}"
              f"{row['goal_difference']:>5}{row['points']:>6}")
    return rows



def print_fixtures(fixtures, teams):
    names = {team["id"]: team["name"] for team in teams}

    print("\nFIXTURES")

    for fixture in fixtures:
        home = names.get(fixture.get("home_team"), "UNKNOWN TEAM")
        away = names.get(fixture.get("away_team"), "UNKNOWN TEAM")

        if fixture.get("status") == "played":
            score = (
                f'{fixture["home_score"]} - '
                f'{fixture["away_score"]}'
            )
        else:
            score = "pending"

        print(
            f'Fixture {fixture.get("id")}: '
            f'{home} vs {away} [{score}]'
        )


def run_cli(teams, fixtures):
    """Run the Engineer B menu. Persistence and fixture generation are external."""
    actions = {
        "1": "List fixtures",
        "2": "Record result",
        "3": "View standings",
        "4": "Show champion report",
        "5": "Quit",
    }
    while True:
        print("\nTOURNAMENTLAB — ENGINEER B")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print_fixtures(fixtures, teams)
        
        elif choice == "2":
            try:
                fixture_id = int(input("Fixture ID: ").strip())
                home_score = int(input("Home score: ").strip())
                away_score = int(input("Away score: ").strip())

                record_result(
                    fixtures,
                    fixture_id,
                    home_score,
                    away_score
                )

                # Save the updated tournament data
                save_teams({
                    "teams": teams,
                    "fixtures": fixtures
                })

            except ValueError as exc:
                print(f"Result rejected: {exc}")
            except OSError as exc:
                print(f"Could not save result: {exc}")
            else:
                print("Result recorded and saved successfully.")

        elif choice == "3":
            status = "complete" if fixtures and all(
                f.get("status") == "played" for f in fixtures
            ) else "in progress"
            print(f"Season status: {status}")
            print_standings(teams, fixtures)
        elif choice == "4":
            report = champion_report(teams, fixtures)
            print(report["message"])
            if report["champion"] is not None:
                print_standings(teams, fixtures)
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 5.")
