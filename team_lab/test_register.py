import unittest
from unittest.mock import patch

from register_team import register_team


class TestTeamRegistration(unittest.TestCase):

    def setUp(self):
        self.data = {
            "teams": [],
            "fixtures": []
        }


    @patch("register_team.save_teams")
    @patch("register_team.load_teams")
    def test_register_new_team(self, mock_load, mock_save):
        mock_load.return_value = self.data

        team = register_team("Lions")

        self.assertEqual(team["name"], "Lions")
        self.assertEqual(team["id"], "T001")

        self.assertEqual(len(self.data["teams"]), 1)

        mock_save.assert_called_once()


    @patch("register_team.load_teams")
    def test_duplicate_team_registration(self, mock_load):
        mock_load.return_value = {
            "teams": [
                {
                    "id": "T001",
                    "name": "Lions"
                }
            ],
            "fixtures": []
        }

        with self.assertRaises(ValueError):
            register_team("lions")


    @patch("register_team.load_teams")
    def test_empty_team_name(self, mock_load):
        mock_load.return_value = {
            "teams": [],
            "fixtures": []
        }

        with self.assertRaises(ValueError):
            register_team("   ")


if __name__ == "__main__":
    unittest.main()