
import json
import os

from storage import load_teams, save_teams
from register_team import register_team
from team_id import generate_team_id
from fixtures import generate_fixtures
from cli import run_cli
from results import record_result
from standings import (
    compute_standings,
    league_complete,
    champion_report,
)



DATA_FILE = "teams.json"


def initialize_data():
    """Create the tournament JSON file if it does not exist."""
    if not os.path.exists(DATA_FILE):
        save_teams({
            "teams": [],
            "fixtures": []
        })

    data = load_teams()

    if not isinstance(data, dict):
        raise ValueError(
            "Tournament data must be a dictionary."
        )

    data.setdefault("teams", [])
    data.setdefault("fixtures", [])

    return data


def show_teams(teams):
    """Display all registered teams."""
    if not teams:
        print("\nNo teams registered yet.")
        return

    print("\n--- Registered Teams ---")

    for team in teams:
        print(f'{team["id"]}: {team["name"]}')


def show_fixtures(fixtures):
    """Display all tournament fixtures."""
    if not fixtures:
        print("\nNo fixtures generated yet.")
        return

    print("\n--- Fixtures ---")

    for fixture in fixtures:
        print(
            f'Fixture {fixture["id"]}: '
            f'{fixture["home_team"]} vs '
            f'{fixture["away_team"]} | '
            f'Status: {fixture["status"]} | '
            f'Score: {fixture["home_score"]} - '
            f'{fixture["away_score"]}'
        )


def register_new_team():
    """Register a team using Engineer A's function."""
    name = input("Enter team name: ").strip()

    try:
        team = register_team(name)
        print(
            f'Successfully registered '
            f'{team["name"]} with ID {team["id"]}.'
        )
    except (ValueError, FileNotFoundError) as error:
        print(f"Registration failed: {error}")


def create_fixtures():
    """Generate round-robin fixtures."""
    try:
        data = load_teams()

        if len(data["teams"]) < 2:
            print("Register at least two teams first.")
            return

        fixtures = generate_fixtures(data)

        print(f"\nGenerated {len(fixtures)} fixtures.")
        show_fixtures(fixtures)

    except (ValueError, KeyError, FileNotFoundError) as error:
        print(f"Fixture generation failed: {error}")


def enter_result():
    """Record a score using Engineer B's function."""
    data = load_teams()
    fixtures = data["fixtures"]

    pending = [
        fixture for fixture in fixtures
        if fixture["status"] == "pending"
    ]

    if not pending:
        print("\nThere are no pending fixtures.")
        return

    show_fixtures(fixtures)

    try:
        fixture_id = int(input("\nEnter fixture ID: "))
        home_score = int(input("Enter home team score: "))
        away_score = int(input("Enter away team score: "))

        record_result(
            fixtures,
            fixture_id,
            home_score,
            away_score
        )

        save_teams(data)
        print("Result recorded and saved successfully.")

    except ValueError as error:
        print(f"Could not record result: {error}")
    except (KeyError, TypeError) as error:
        print(f"Invalid fixture data: {error}")


def display_standings():
    data = load_teams()

    standings = compute_standings(
        data["teams"],
        data["fixtures"]
    )

    print("\n" + "=" * 85)
    print("                     |LEAGUE STANDINGS|")
    print("=" * 85)

    print(
        f"{'Rank|':<6}"
        f"{'  Team |':<18}"
        f"{'P|':>4}"
        f"{'W|':>4}"
        f"{' D|':>4}"
        f"{'    L|':>4}"
        f"{'      GF|':>6}"
        f"{'      GA|':>6}"
        f"{'      GD|':>7}"
        f"{'      Pts|':>7}"
    )

    print("-" * 85)

    for rank, row in enumerate(standings, start=1,):
        print(
            f"{rank:<6}|"
            f"{row['team']:<18}"
            f"{row['played']:>2}|"
            f"{row['wins']:>3}|"
            f"{row['draws']:>3}|"
            f"{row['losses']:>5}|"
            f"{row['goals_for']:>8}|"
            f"{row['goals_against']:>8}|"
            f"{row['goal_difference']:>8}|"
            f"{row['points']:>9}|"
        )

    print("=" * 85)

def display_champion():
    """Display the champion only when the league is complete."""
    data = load_teams()

    try:
        if not league_complete(data["fixtures"]):
            print(
                "\nThe tournament is not complete. "
                "Record all fixture results first."
            )
            return

        report = champion_report(
            data["teams"],
            data["fixtures"]
        )

        print("\n--- Champion Report ---")

        if isinstance(report, (dict, list)):
            print(json.dumps(report, indent=4))
        else:
            print(report)

    except (ValueError, KeyError, TypeError) as error:
        print(f"Could not generate champion report: {error}")


def test_team_id_generator():
    """Run Engineer A's ID generator against current data."""
    data = load_teams()

    try:
        next_id = generate_team_id(data)
        print(f"Next available team ID: {next_id}")
    except (ValueError, KeyError, TypeError) as error:
        print(f"ID generation failed: {error}")


def main():
    """Main tournament application."""
    try:
        initialize_data()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"Could not initialize tournament data: {error}")
        return

    while True:
        print("\n========== TOURNAMENT LAB ==========")
        print("1. Register a team")
        print("2. View registered teams")
        print("3. Generate fixtures")
        print("4. View fixtures")
        print("5. Enter a match result")
        print("6. View league standings")
        print("7. View champion report")
        print("8. Test team ID generator")
        print("9. Run Engineer B's CLI")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        try:
            if choice == "1":
                register_new_team()

            elif choice == "2":
                data = load_teams()
                show_teams(data["teams"])

            elif choice == "3":
                create_fixtures()

            elif choice == "4":
                data = load_teams()
                show_fixtures(data["fixtures"])

            elif choice == "5":
                enter_result()

            elif choice == "6":
                display_standings()

            elif choice == "7":
                display_champion()

            elif choice == "8":
                test_team_id_generator()

            elif choice == "9":
                data = load_teams()
                run_cli(data["teams"], data["fixtures"])

            elif choice == "0":
                print("Tournament application closed.")
                break

            else:
                print("Invalid option. Choose from 0 to 9.")

        except (FileNotFoundError, json.JSONDecodeError) as error:
            print(f"Could not access tournament data: {error}")
        except (KeyError, TypeError) as error:
            print(f"Tournament data error: {error}")


if __name__ == "__main__":
    main()
