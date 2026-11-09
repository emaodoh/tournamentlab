import unittest

from team_lab.results import record_result
from team_lab.standings import compute_standings, league_complete, champion_report


def sample_data():
    teams = [
        {"id": "TM001", "name": "Thunder"},
        {"id": "TM002", "name": "Comets"},
        {"id": "TM003", "name": "Phoenix"},
        {"id": "TM004", "name": "Rockets"},
    ]
    fixtures = [
        {"id": "M001", "home_id": "TM001", "away_id": "TM002",
         "status": "pending", "home_score": None, "away_score": None},
        {"id": "M002", "home_id": "TM003", "away_id": "TM004",
         "status": "pending", "home_score": None, "away_score": None},
        {"id": "M003", "home_id": "TM001", "away_id": "TM003",
         "status": "pending", "home_score": None, "away_score": None},
        {"id": "M004", "home_id": "TM002", "away_id": "TM004",
         "status": "pending", "home_score": None, "away_score": None},
        {"id": "M005", "home_id": "TM001", "away_id": "TM004",
         "status": "pending", "home_score": None, "away_score": None},
        {"id": "M006", "home_id": "TM002", "away_id": "TM003",
         "status": "pending", "home_score": None, "away_score": None},
    ]
    return teams, fixtures


class ResultTests(unittest.TestCase):
    def test_valid_result_updates_fixture(self):
        _, fixtures = sample_data()
        result = record_result(fixtures, "M001", 2, 1)
        self.assertEqual((result["home_score"], result["away_score"], result["status"]),
                         (2, 1, "played"))

    def test_rejects_negative_float_and_bool_without_mutation(self):
        _, fixtures = sample_data()
        before = [item.copy() for item in fixtures]
        for home, away in [(-1, 0), (1.5, 0), (True, 0), (0, False)]:
            with self.subTest(home=home, away=away):
                with self.assertRaises(ValueError):
                    record_result(fixtures, "M001", home, away)
                self.assertEqual(fixtures, before)

    def test_unknown_fixture_rejected(self):
        _, fixtures = sample_data()
        with self.assertRaises(ValueError):
            record_result(fixtures, "M999", 1, 0)

    def test_duplicate_result_rejected_without_change(self):
        _, fixtures = sample_data()
        record_result(fixtures, "M001", 2, 1)
        before = [item.copy() for item in fixtures]
        with self.assertRaises(ValueError):
            record_result(fixtures, "M001", 4, 0)
        self.assertEqual(fixtures, before)


class StandingsTests(unittest.TestCase):
    def test_win_draw_loss_points_and_goal_counts(self):
        teams, fixtures = sample_data()
        record_result(fixtures, "M001", 2, 1)  # Thunder win
        record_result(fixtures, "M002", 0, 0)  # draw
        rows = {row["team"]: row for row in compute_standings(teams, fixtures)}
        self.assertEqual(rows["Thunder"]["points"], 3)
        self.assertEqual(rows["Thunder"]["goals_for"], 2)
        self.assertEqual(rows["Comets"]["points"], 0)
        self.assertEqual(rows["Phoenix"]["points"], 1)
        self.assertEqual(rows["Rockets"]["points"], 1)
        self.assertEqual(rows["Phoenix"]["draws"], 1)

    def test_standings_recomputed_from_fixtures(self):
        teams, fixtures = sample_data()
        first = compute_standings(teams, fixtures)
        record_result(fixtures, "M001", 3, 0)
        second = compute_standings(teams, fixtures)
        self.assertNotEqual(first, second)
        self.assertEqual(next(r for r in second if r["team"] == "Thunder")["points"], 3)

    def test_tie_breaks_by_goal_difference_then_goals_for_then_name(self):
        teams = [
            {"id": "A", "name": "Zulu"},
            {"id": "B", "name": "Alpha"},
            {"id": "C", "name": "Beta"},
        ]
        fixtures = [
            {"id": "M1", "home_id": "A", "away_id": "B", "status": "played",
             "home_score": 2, "away_score": 0},
            {"id": "M2", "home_id": "A", "away_id": "C", "status": "played",
             "home_score": 0, "away_score": 2},
            {"id": "M3", "home_id": "B", "away_id": "C", "status": "played",
             "home_score": 1, "away_score": 0},
        ]
        # All teams have 3 points. Beta has the best GD, Zulu is next, Alpha is last.
        rows = compute_standings(teams, fixtures)
        self.assertEqual([r["team"] for r in rows], ["Beta", "Zulu", "Alpha"])

    def test_champion_only_after_all_fixtures_played(self):
        teams, fixtures = sample_data()
        record_result(fixtures, "M001", 2, 0)
        report = champion_report(teams, fixtures)
        self.assertEqual(report["status"], "in progress")
        self.assertIsNone(report["champion"])
        for fixture in fixtures:
            if fixture["status"] == "pending":
                record_result(fixtures, fixture["id"], 0, 0)
        report = champion_report(teams, fixtures)
        self.assertEqual(report["status"], "complete")
        self.assertIsNotNone(report["champion"])
        self.assertTrue(league_complete(fixtures))


if __name__ == "__main__":
    unittest.main()
