import json
import os
import tempfile
import unittest

from storage import load_teams


class TestStorage(unittest.TestCase):

    def test_invalid_json_file(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            temp.write("{ invalid json }")
            filename = temp.name

        try:
            with self.assertRaises(json.JSONDecodeError):
                load_teams(filename)
        finally:
            os.remove(filename)


if __name__ == "__main__":
    unittest.main()