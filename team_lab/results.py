"""Engineer B: safe fixture result recording."""

def _valid_score(score):
    # bool is a subclass of int in Python, so reject it explicitly.
    return isinstance(score, int) and not isinstance(score, bool) and score >= 0


def record_result(fixtures, fixture_id, home_score, away_score):
    """Record a result once. Validate everything before mutating the fixture.

    Fixtures use dictionaries with: id, status, home_score, away_score.
    Returns the updated fixture. Raises ValueError for invalid submissions.
    """
    if not _valid_score(home_score) or not _valid_score(away_score):
        raise ValueError("Scores must be nonnegative integers (not booleans).")

    fixture = next((item for item in fixtures if item.get("id") == fixture_id), None)
    if fixture is None:
        raise ValueError(f"Unknown fixture ID: {fixture_id}")

    if fixture.get("status") != "pending":
        raise ValueError(f"Fixture {fixture_id} has already been played.")

    if fixture.get("home_score") is not None or fixture.get("away_score") is not None:
        raise ValueError("Pending fixture has inconsistent score data.")

    # Mutate only after every validation succeeds.

    fixture["home_score"] = home_score
    fixture["away_score"] = away_score
    fixture["status"] = "played"
    return fixture
