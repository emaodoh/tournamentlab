import json


def save_teams(filename = "data/teams.json"):
    
    """
    Save a list of dictionaries to a JSON file.

    Args:
        data (list[dict]): The data to save.
        filename (str): The JSON file name.
    """
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_teams(filename = "data/teams.json"):
    """
    Load and validate a JSON file containing a list of dictionaries.

    Args:
        filename (str): The JSON file path.

    Returns:
        list[dict]: The validated data.

    Raises:
        ValueError: If the JSON structure is invalid.
        json.JSONDecodeError: If the file contains invalid JSON.
    """

    with open(filename, "r") as file:
        data = json.load(file)

    # Check that the top-level data is a list
    if not isinstance(data, dict):
        raise ValueError("JSON data must be a list")

    # Check that every item in the list is a dictionary
    # for item in data:
    #     if not isinstance(item, dict):
    #         raise ValueError("Every item must be a dictionary")

    return data





