"""Development-only hot reload for cogs.

Watches the ``cogs/`` package for source changes and reloads the
corresponding extension in place via ``bot.reload_extension()``. The
bot's gateway connection is never dropped, so this is meant as a
faster alternative to the manual ``?reload <cog>`` command during
local development — not a production feature.
"""

import logging
from pathlib import Path

from nextcord.ext.commands import Bot
from watchfiles import Change, awatch

logger = logging.getLogger(__name__)

COGS_DIR = Path(__file__).resolve().parent.parent / "cogs"


def _extension_name(path: Path) -> str | None:
    """Map a changed file path to its dotted extension name.

    e.g. ``cogs/setup.py`` -> ``cogs.setup``. Returns ``None`` for
    paths that aren't loadable extensions (non-.py files, dunders,
    files outside the cogs package).
    """
    try:
        relative = path.resolve().relative_to(COGS_DIR.parent)
    except ValueError:
        return None

    if relative.suffix != ".py" or relative.stem.startswith("_"):
        return None

    return ".".join(relative.with_suffix("").parts)


async def watch_cogs(bot: Bot) -> None:
    """Reload cogs as their source files change. Runs until cancelled."""
    logger.info("Hot reload watching %s for changes.", COGS_DIR)

    async for changes in awatch(COGS_DIR):
        for change, raw_path in changes:
            if change == Change.deleted:
                continue

            extension = _extension_name(Path(raw_path))

            if extension is None:
                continue

            try:
                if extension in bot.extensions:
                    # reload_extension() is synchronous in nextcord 3.x -
                    # awaiting it raises TypeError on its None return and
                    # gets misreported as a failed reload below.
                    bot.reload_extension(extension)
                    logger.info("Hot reloaded %s", extension)
                else:
                    bot.load_extension(extension)
                    logger.info("Hot loaded new extension %s", extension)
            except Exception:
                logger.exception("Hot reload failed for %s", extension)
