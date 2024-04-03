"""Initialisation module for Custom Ambilight integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import MyApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Custom Ambilight from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create API instance with host, username, and password from the config entry
    api = MyApi(entry.data["host"], entry.data["username"], entry.data["password"])

    # Create a data update coordinator
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="custom_ambilight",
        update_method=api.get_data,
        update_interval=timedelta(seconds=30),
    )

    # Fetch initial data
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    # Store the data update coordinator for your platforms to access
    coordinator.api = api
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
