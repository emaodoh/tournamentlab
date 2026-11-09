# TournamentLab — Engineer B

## Scope
Engineer B owns result entry and validation, standings, ranking/tie-breaks, champion reporting, and the CLI-facing commands.

## Files
- `results.py`: safe one-time result entry.
- `standings.py`: standings derived from played fixtures and champion status.
- `cli.py`: menu and terminal output.
- `test_engineer_b.py`: automated tests.

## Data contract
Teams: `{"id": "TM001", "name": "Thunder"}`

Fixtures:
`{"id": "M001", "home_id": "TM001", "away_id": "TM002", "status": "pending", "home_score": None, "away_score": None}`

Engineer A's scheduling/persistence layer should provide records in this shape or agree on a shared contract before integration.

## Ranking
1. Points descending.
2. Goal difference descending.
3. Goals scored descending.
4. Normalized team name ascending (`strip().casefold()`).

No head-to-head rule is added.

## Run tests
From this folder:
`python -m unittest -v`

## Integration
When Engineer A's module is ready, import its team/fixture generation and JSON save/load functions. Pass the resulting `teams` and `fixtures` lists into `run_cli(teams, fixtures)`. This Engineer B implementation does not generate fixtures or save/load JSON; those belong to Engineer A.
