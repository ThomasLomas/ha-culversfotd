# Culver's Flavor of the Day for Home Assistant

Absolutely no connection to Culver's. Not official whatsoever. No warranty provided on accurancy. I'm just someone who spends too much money on their concerete mixers.

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show the current flavor of the day

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `culvers_fotd`.
1. Download _all_ the files from the `custom_components/culvers_fotd/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Culver's FOTD"

## Configuration is done in the UI

Set the restaurant slug as per the instructions.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)
