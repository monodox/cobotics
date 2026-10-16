"""Application settings.

Resolution order (lowest to highest precedence):
    defaults.yaml -> environment variables (COBOTICS_*) -> .env file.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_DEFAULTS_PATH = Path(__file__).with_name("defaults.yaml")


def _load_defaults() -> dict:
    if _DEFAULTS_PATH.exists():
        with _DEFAULTS_PATH.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    return {}


class Settings(BaseSettings):
    """Runtime settings, overridable via COBOTICS_* env vars and .env."""

    model_config = SettingsConfigDict(
        env_prefix="COBOTICS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # AI
    ai_backend: str = "stub"              # stub | openai | anthropic | nebius
    ai_model: str = "gpt-4o-mini"

    # Nebius Token Factory (OpenAI-compatible inference API serving NVIDIA models)
    nebius_base_url: str = "https://api.studio.nebius.com/v1/"

    # Hardware
    hardware_backend: str = "simulator"

    # Logging
    log_level: str = "INFO"

    # Simulator world
    world_bounds: tuple[float, float] = (10.0, 10.0)
    start_position: tuple[float, float] = (0.0, 0.0)
    move_speed: float = 1.0

    # Raw API keys (not prefixed, read directly from env)
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    nebius_api_key: str | None = Field(default=None, alias="NEBIUS_API_KEY")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Build settings, seeding from defaults.yaml then letting env/.env win."""
    defaults = _load_defaults()

    seed: dict = {}
    if ai := defaults.get("ai"):
        seed["ai_backend"] = ai.get("backend", "stub")
        seed["ai_model"] = ai.get("model", "gpt-4o-mini")
    if hw := defaults.get("hardware"):
        seed["hardware_backend"] = hw.get("backend", "simulator")
    if sim := defaults.get("simulator"):
        seed["world_bounds"] = tuple(sim.get("world_bounds", (10.0, 10.0)))
        seed["start_position"] = tuple(sim.get("start_position", (0.0, 0.0)))
        seed["move_speed"] = sim.get("move_speed", 1.0)
    if log := defaults.get("logging"):
        seed["log_level"] = log.get("level", "INFO")

    # Settings() reads env + .env, which override the YAML seed.
    return Settings(**seed)
