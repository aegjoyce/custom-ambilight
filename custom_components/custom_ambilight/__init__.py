"""The Custom Ambilight integration."""

from __future__ import annotations

import logging
import ssl

import aiohttp
from aiohttp import BasicAuth

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Custom Ambilight from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    # Create API instance
    host = entry.data["host"]
    username = entry.data["username"]
    password = entry.data["password"]
    jointspace_api = JointSpaceAPI(host, username, password)

    # Validate the API connection (and authentication)
    valid = await jointspace_api.validate_connection()
    if not valid:
        return False

    # Store an API object for your platforms to access
    hass.data[DOMAIN][entry.entry_id] = jointspace_api

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class JointSpaceAPI:
    def __init__(self, host, username, password):
        self.base_url = f"https://{host}:1926/6/ambilight/currentconfiguration"
        self.auth = BasicAuth(login=username, password=password)
        self.headers = {"Content-Type": "application/json"}
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def validate_connection(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url,
                headers=self.headers,
                auth=self.auth,
                ssl=self.ssl_context,
            ) as response:
                _LOGGER.info(f"Received response status code: {response.status}")
                return response.status == 200
