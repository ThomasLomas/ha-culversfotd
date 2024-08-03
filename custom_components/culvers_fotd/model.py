"""Model file."""

from dataclasses import dataclass


@dataclass
class RestaurantResponse:
    """Data for the restaurant."""

    restaurant_name: str
    flavor_of_the_day: str
