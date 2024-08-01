"""Custom types for culvers_fotd."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import CulversFotdApiClient
    from .coordinator import CulversFotdDataUpdateCoordinator


type CulversFotdConfigEntry = ConfigEntry[CulversFotdData]


@dataclass
class CulversFotdData:
    """Data for the CulversFotd integration."""

    client: CulversFotdApiClient
    coordinator: CulversFotdDataUpdateCoordinator
    integration: Integration
