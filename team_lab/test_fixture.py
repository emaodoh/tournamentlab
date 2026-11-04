import unittest
from unittest.mock import patch

from fixtures import generate_fixtures


class TestGenerateFixtures(unittest.TestCase):

    def setUp(self):
        self.data = {
            "teams": [
                {"id": "T001", "name": "Lions"},
                {"id": "T002", "name": "Eagles"},
                {"id": "T003", "name": "Sharks"},
                {"id": "T004", "name": "Tigers"},
            ],
            "fixtures": []
        }

    @patch("fixtures.save_teams")
    def test_fixture_count(self, mock_save):
        fixtures = generate_fixtures(self.data)

        expected = len(self.data["teams"]) * (len(self.data["teams"]) - 1) // 2

        self.assertEqual(len(fixtures), expected)

    @patch("fixtures.save_teams")
    def test_duplicate_fixtures(self, mock_save):
        fixtures = generate_fixtures(self.data)

        seen = set()

        for fixture in fixtures:
            pair = frozenset({
                fixture["home_team"],
                fixture["away_team"]
            })

            self.assertNotIn(pair, seen)
            seen.add(pair)


if __name__ == "__main__":
    unittest.main()