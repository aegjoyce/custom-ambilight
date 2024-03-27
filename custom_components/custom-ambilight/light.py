from __future__ import annotations
import logging
import voluptuous as vol
import aiohttp

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    SUPPORT_BRIGHTNESS,
    LightEntity,
    PLATFORM_SCHEMA
)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

def setup_platform(hass: HomeAssistant, config: ConfigType, add_entities: AddEntitiesCallback, discovery_info: DiscoveryInfoType = None) -> None:
    """Set up the Custom Ambilight platform."""
    # Get configuration data
    host = config[CONF_HOST]
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]

    # Create our custom light
    light = CustomAmbilight('Custom Ambilight', username, password, host)

    # Add entities
    add_entities([light])

class CustomAmbilight(LightEntity):
    """Representation of a Custom Ambilight."""

    def __init__(self, name, username, password, host):
        """Initialize a Custom Ambilight."""
        self._name = name
        self._state = False
        self._brightness = 255
        self._username = username
        self._password = password
        self._host = host

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._username

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://{self._host}:1926/6/ambilight/power",
                auth=aiohttp.BasicAuth(self._username, self._password),
                data='{"power":"on"}'
            ) as response:
                if response.status == 200:
                    self._state = True
                    if ATTR_BRIGHTNESS in kwargs:
                        self._brightness = kwargs[ATTR_BRIGHTNESS]

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://{self._host}:1926/6/ambilight/power",
                auth=aiohttp.BasicAuth(self._username, self._password),
                data='{"power":"off"}'
            ) as response:
                if response.status == 200:
                    self._state = False

    async def async_update(self):
        """Fetch new state data for this light."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://{self._host}:1926/6/ambilight/currentconfiguration", auth=aiohttp.BasicAuth(self._username, self._password)) as response:
                if response.status == 200:
                    state_data = await response.json()
                    self._state = state_data["state"] == "on"
                    self._brightness = state_data["brightness"]
