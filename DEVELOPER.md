# Presence — Developer Documentation

## Overview

Presence is a Discord bot that tracks member activity and idle time across guilds. It monitors message events to maintain a last-seen timestamp per member, exposes slash commands for querying idle status, and runs an automated daily purge of members who have exceeded their guild's inactivity threshold.

The bot uses **nextcord** (Discord API wrapper), **Redis** as a caching layer for hot data, and a **GraphQL backend API** as the source of truth for persistent storage.

---

## Prerequisites

- Docker + Docker Compose
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))
- A running GraphQL backend (see `utility/request_handler.py` for expected API shape)

For local Python tooling (linting, tests) without Docker:
- Python 3.12+
- `pip install -r requirements.txt -r requirements-dev.txt`

---

## Environment Variables

| Variable | Default | Required | Notes |
|---|---|---|---|
| `TOKEN` | — | Yes | Discord bot token |
| `REDIS_HOST` | `localhost` | No | Use `redis` inside Docker (service name) |
| `REDIS_PORT` | `6379` | No | Standard Redis port |

Copy `.env.example` (or create `.env`) in the project root:

```
TOKEN=your_discord_bot_token_here
```

`REDIS_HOST` and `REDIS_PORT` are set automatically by `docker-compose.yml` for the bot container.

---

## Running Locally

```bash
docker-compose up       # Start bot + Redis
docker-compose down     # Stop and remove containers
```

The bot container mounts the project root as a volume (`- .:/app`), so code changes are reflected without rebuilding. The bot attaches to a TTY; `Ctrl+C` stops both services.

Redis must pass its healthcheck before the bot container starts (`depends_on: condition: service_healthy`). On `on_ready`, the bot also retries Redis connection in a loop until successful.

> **Note:** Running `python main.py` directly will fail — Redis is required and `REDIS_HOST=redis` only resolves inside the Docker network.

---

## Project Structure

```
presence/
├── main.py                  # Bot entry point — setup, events, extension loading
├── cogs/                    # Command groups and event listeners (loaded as extensions)
│   ├── admin_cmds.py        # Admin slash commands (reset, set, ping, baseline)
│   ├── automated.py         # Background tasks (daily purge, Redis keepalive)
│   ├── dev_cmds.py          # Developer-only prefix commands (sync, reset, reload, etc.)
│   ├── listeners.py         # Discord event handlers (messages, joins, updates)
│   ├── setup.py             # on_guild_join handler — initializes guild/members in DB + Redis
│   └── user_cmds.py         # User-facing slash commands (/status member, /status guild)
├── utility/
│   ├── redis.py             # AsyncRedisManager — connection pool wrapper
│   ├── request_handler.py   # RequestHandler — all GraphQL API calls
│   ├── helpers.py           # _check_time_idle() — idle duration calculation
│   └── decorators/
│       └── checks.py        # Command check decorators (developer-only, bot-only)
├── lib/
│   ├── typings.py           # Pydantic models (Member, DiscordGuild, Activity, etc.)
│   ├── queries.py           # GraphQL query/mutation strings + `queries` dict
│   └── enums.py             # Enums (Pattern, Mode)
├── tests/
│   └── test_startup.py      # Stub test suite (unittest)
├── Dockerfile.dev           # Bot container image (python:3.14-slim)
├── redis.Dockerfile         # Custom Redis image
├── docker-compose.yml       # Orchestration: bot + redis services
├── pyproject.toml           # Project metadata, black config (version 0.5.0)
├── requirements.txt         # Pinned runtime deps
└── requirements-dev.txt     # Dev deps (pytest, etc.)
```

---

## Architecture

### Bot startup (`main.py`)

1. Loads env vars, creates `AsyncRedisManager` client.
2. Registers Discord intents: `members`, `guilds`, `message_content`, `voice_states`.
3. Loads all cogs from the `extensions` list.
4. On `on_ready`: verifies Redis connection (retries every 5s), prints guild health summary, syncs slash commands, sets presence.
5. Global check `globally_block_dms` rejects all DMs — bot is guild-only.
6. Rotating log handler writes to `bot_log.txt` (500KB, 5 backups).

### Cogs

**`listeners.py`** — core tracking logic:
- `on_message`: for each non-bot guild message not in the ignore list, updates `member:{id}:{guild_id}:meta.idles_at` with `now + 10 minutes` and sets/refreshes a session expiry key in Redis.
- `on_member_join`: writes member meta to Redis; queries GraphQL for existing member record.
- `on_member_update` / `on_user_update`: syncs nickname/username changes to GraphQL.
- `on_guild_update`: syncs guild name changes to GraphQL.

**`setup.py`**:
- `on_guild_join`: registers guild + all non-bot members in GraphQL, then primes Redis with guild meta, stats, and per-member hashes using a pipeline.

**`user_cmds.py`**:
- `/status member [member]`: reads `guild:{id}:member:{id}` from Redis, computes idle duration via `_check_time_idle`, responds with human-readable time.
- `/status guild`: same but for the guild aggregate (`guild:{id}:meta` + `guild:{id}:stats`).

**`admin_cmds.py`** (requires `administrator` permission):
- `/reset`: triggers guild data reset via GraphQL.
- `/set auto_kick`, `/set time_until_inactive`, `/set auto_prune_timer`: update guild settings in GraphQL.
- `/ping [member]`: DMs a member an inactivity warning (requires `kick_members`).
- `/baseline`: stub — intended to backfill last-activity timestamps from message history.

**`dev_cmds.py`** (hardcoded developer Discord ID only):
- Prefix commands (`?`): `sync`, `reset`, `delete`, `reload <cog>`, `setup`.
- `reload` hot-reloads a cog by name without restarting the bot.

**`automated.py`**:
- `purge` loop (every 86400s): fetches purge list from GraphQL, kicks each member from their guild, removes them from the list.
- `ping` loop (every 300s): Redis keepalive.

### Redis key schema

| Key | Type | Contents |
|---|---|---|
| `guild:{guild_id}:meta` | Hash | `guild_id`, `name`, `status`, `settings`, `date_added` |
| `guild:{guild_id}:stats` | Hash | `last_act`, `idle_stats` |
| `guild:{guild_id}:members` | Set | Member IDs |
| `guild:{guild_id}:member:{member_id}` | Hash | Member fields from GraphQL + `name` |
| `member:{member_id}:{guild_id}:meta` | Hash | `name`, `status`, `admin_access`, `flags`, `discord_status`, `idles_at` |
| `session:{member_id}:{guild_id}:expires_at` | String | Session expiry timestamp |

### GraphQL backend (`utility/request_handler.py`)

`RequestHandler` wraps all API calls. Dev URL: `http://localhost:8000/gql`. Prod URL: `https://combot.bblankenship.me/v1/`.

Environment is set at instantiation (`Environment.DEV` by default). All queries are defined as strings in `lib/queries.py` and referenced via the `queries` dict.

Key operations: `get_guild`, `get_member`, `update_guild`, `update_member`, `remove_guild`, `remove_member`, `get_purge_list`, `add_to_purge_list`, `remove_from_purge_list`.

---

## Adding a New Cog

1. Create `cogs/your_cog.py` with a `Cog` subclass and a `setup(bot)` function.
2. Add `"cogs.your_cog"` to the `extensions` list in `main.py`.
3. Reload during dev with `?reload your_cog` (developer account only) or restart the container.

---

## Code Style & Tooling

- **Formatter**: `black` (line length 99, target py312) — configured in `pyproject.toml`.
- **Import order**: `isort` — configured in `.isort.cfg`.
- **Lint**: `pylint` — configured in `.pylintrc`.
- **Pre-commit hooks**: `.pre-commit-config.yaml` (install with `pre-commit install`).
- **Tests**: `pytest` via `tox` (`tox.ini`). Test coverage is minimal — `tests/test_startup.py` is a stub.

---

## Logging

`main.py` configures a `RotatingFileHandler` → `bot_log.txt` at `INFO` level. Format:

```
%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(message)s
```

`RequestHandler` logs operation timing at `INFO` and failures at `DEBUG`.
