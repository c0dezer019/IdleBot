# Presence

Presence is a Discord bot that tracks member activity and idle time across guilds. It
monitors message events (and other user actions) to maintain a last-seen timestamp per
member, exposes slash commands for querying idle status, and runs an automated purge of
members who have exceeded their guild's inactivity threshold.

The bot is written in Python using [nextcord](https://docs.nextcord.dev/), uses
**Redis** as a caching layer, and a **GraphQL + PostgreSQL** backend for persistent
storage.

```{toctree}
:maxdepth: 2
:caption: Contents

developer
```
