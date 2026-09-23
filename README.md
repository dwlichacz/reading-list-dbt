# reading-list-dbt

A dbt project that turns a messy, hand-kept reading log into clean, tested analytics tables.

It runs locally on [DuckDB](https://duckdb.org/), so there's nothing to sign up for and no credentials to configure.

```bash
pip install -r requirements.txt
dbt build
```

That loads the raw data, builds every model, and runs the tests in a few seconds.

## What it does

The raw reading log has the problems real exports usually have:

| Field | Raw data | After staging |
|---|---|---|
| Status | `READ`, `done`, ` Finished`, `Did Not Finish`, `IN PROGRESS` | `finished`, `dnf`, `reading` |
| Dates | A mix of `2024-03-05` and `03/05/2024` | Proper `DATE` values |
| Rating | `4`, `4/5`, or blank | Integer or null |
| Format | `HC`, `Hardback`, `kindle `, `Audible`, `soft cover` | `hardcover`, `paperback`, `ebook`, `audiobook` |

## Models

| Layer | Models | Job |
|---|---|---|
| **staging** (views) | `stg_books`, `stg_reading_log` | Clean and type each raw table. No joins. |
| **marts** (tables) | `fct_reading_sessions`, `dim_books` | What an analyst or dashboard would query. |

A [GitHub Actions workflow](.github/workflows/dbt-build.yml) runs `dbt build` on every push.

## About the data

The data is **mock data** from [`scripts/generate_mock_data.py`](scripts/generate_mock_data.py). It uses a fixed random seed, so it's fully reproducible. The book titles are real, but the reading history is invented.

## Exploring the results

```python
import duckdb

con = duckdb.connect("reading_list.duckdb", read_only=True)
con.sql("select * from dim_books order by times_finished desc").show()
```

## Roadmap

- [ ] Richer tests (accepted values, relationships, custom range checks, business rules, unit tests)
- [ ] Genre bridge table
- [ ] Reusable macros for the cleanup logic
- [ ] Intermediate layer and summary marts (year in books, genre summary)
- [ ] Dash front end
- [ ] Claude API agent that answers questions about the reading history
