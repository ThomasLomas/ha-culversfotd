"""CulversFotdEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .coordinator import CulversFotdDataUpdateCoordinator


class CulversFotdEntity(CoordinatorEntity[CulversFotdDataUpdateCoordinator]):
    """CulversFotdEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: CulversFotdDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            name=coordinator.data.restaurant_name,
            model=coordinator.config_entry.data["restaurant"],
            configuration_url=f"https://www.culvers.com/restaurants/{coordinator.config_entry.data['restaurant']}",
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
        )
