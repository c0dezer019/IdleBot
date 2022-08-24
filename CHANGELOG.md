# Version 1.1a (in-development)

## Highlights

- Added pre-commit hooks for formatting and linting.
- Added new calls to the API.
- Added automated tasks to purge inactive members from a guild with purging enabled.
- Settable settings.

### GraphQL

- Reformed queries to be more precise.
- New schema, generated with Postman.
- json file of all queries stored in JSON via Postman. Will replace query strings in request_handler.

### New API Calls

- Added CRUD for a new database that will serve as a PurgeList. This is to keep time complexity down as much as possible.

### Automated Tasks

- The bot will purge members from guilds that are entered into the PurgeList, using the loop decorator from Discord API.
- Added a second loop that will either add or remove members from the PurgeList based on recent stats.

### Bot Settings

- Bot now has the ability for guild admin to change settings.

### QOL Changes

- Implemented pre-commit and pre-commit hooks to lint and test on commit.
- Implemented isort to keep imports organized.
- Added pip-tools to make sure packages are up-to-date.
