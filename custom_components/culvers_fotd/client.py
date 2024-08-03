"""Sample API Client."""

from __future__ import annotations

import json
import socket
from typing import Any

import aiohttp
import async_timeout
from bs4 import BeautifulSoup, Tag

from custom_components.culvers_fotd.const import LOGGER
from custom_components.culvers_fotd.model import RestaurantResponse


class CulversFotdClientError(Exception):
    """Exception to indicate a general API error."""


class CulversFotdClientCommunicationError(
    CulversFotdClientError,
):
    """Exception to indicate a communication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    response.raise_for_status()


class CulversFotdClient:
    """Culvers Flavor of the Day Client."""

    def __init__(
        self,
        restaurant: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Culvers Flavor of the Day Client."""
        self._restaurant = restaurant
        self._session = session

    async def async_get_data(self) -> RestaurantResponse:
        """Get data from the website."""
        url = f"https://www.culvers.com/restaurants/{self._restaurant}"
        LOGGER.debug("Fetching data from %s", url)
        response_data = await self.client_wrapper(
            method="get",
            url=url,
        )

        soup = BeautifulSoup(response_data, "html.parser")

        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if script_tag and isinstance(script_tag, Tag):
            json_data = script_tag.string
            LOGGER.debug("JSON data: %s", json_data)

            if json_data:
                json_data = json.loads(json_data)
                restaurant_details = json_data["props"]["pageProps"]["page"][
                    "customData"
                ]["restaurantDetails"]

                return RestaurantResponse(
                    restaurant_details["title"],
                    restaurant_details["flavorOfTheDay"][0]["title"],
                )

        msg = "Invalid data received from the website."
        raise CulversFotdClientError(msg)

    async def client_wrapper(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
    ) -> str:
        """Get information from the website."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                )
                _verify_response_or_raise(response)
                return await response.text()
        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise CulversFotdClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise CulversFotdClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise CulversFotdClientError(
                msg,
            ) from exception
