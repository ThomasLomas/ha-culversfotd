"""
Custom integration to integrate culvers_fotd with Home Assistant.

For more details about this integration, please refer to
https://github.com/ThomasLomas/ha-culversfotd
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .client import CulversFotdClient
from .coordinator import CulversFotdDataUpdateCoordinator
from .data import CulversFotdData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import CulversFotdConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CulversFotdConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = CulversFotdDataUpdateCoordinator(
        hass=hass,
    )
    entry.runtime_data = CulversFotdData(
        client=CulversFotdClient(
            restaurant=entry.data["restaurant"],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: CulversFotdConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: CulversFotdConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
