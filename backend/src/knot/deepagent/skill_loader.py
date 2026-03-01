"""Load SKILL.md files from disk for StateBackend usage."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

SKILLS_DIR = Path(__file__).parent / "skills"


def load_skill_files() -> dict:
    """Read all SKILL.md files and return a StateBackend-compatible files dict.

    Returns a dict like:
        {"/skills/fto/SKILL.md": create_file_data(content), ...}

    Called once at Container init, merged into every invoke() call via files={}.
    """
    try:
        from deepagents.backends.utils import create_file_data
    except ImportError:
        logger.warning("deepagents not installed — skill files not loaded")
        return {}

    files: dict = {}
    if not SKILLS_DIR.exists():
        logger.warning("Skills directory not found: %s", SKILLS_DIR)
        return files

    for skill_md in SKILLS_DIR.glob("*/SKILL.md"):
        skill_name = skill_md.parent.name
        key = f"/skills/{skill_name}/SKILL.md"
        try:
            content = skill_md.read_text(encoding="utf-8")
            files[key] = create_file_data(content)
            logger.info("Loaded skill: %s", key)
        except Exception:
            logger.exception("Failed to load skill file: %s", skill_md)

    logger.info("Loaded %d skill files", len(files))
    return files
