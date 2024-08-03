"""Adds config flow for CulversFotd."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .client import (
    CulversFotdClient,
    CulversFotdClientCommunicationError,
    CulversFotdClientError,
)
from .const import DOMAIN, LOGGER


class CulversFotdFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for CulversFotd."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_lookup(restaurant=user_input["restaurant"])
            except CulversFotdClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except CulversFotdClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input["restaurant"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "restaurant",
                        default=(user_input or {}).get("restaurant", vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_lookup(self, restaurant: str) -> None:
        """Validate credentials."""
        client = CulversFotdClient(
            restaurant=restaurant,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
