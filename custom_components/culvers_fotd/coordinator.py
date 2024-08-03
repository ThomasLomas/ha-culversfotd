"""DataUpdateCoordinator for culvers_fotd."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import (
    CulversFotdClientError,
)
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from custom_components.culvers_fotd.model import RestaurantResponse

    from .data import CulversFotdConfigEntry


class CulversFotdDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the client."""

    config_entry: CulversFotdConfigEntry

    data: RestaurantResponse

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=1),
        )

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except CulversFotdClientError as exception:
            raise UpdateFailed(exception) from exception
