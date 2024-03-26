import aiohttp
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    SUPPORT_BRIGHTNESS,
    LightEntity,
)

class CustomAmbilight(LightEntity):
    """Representation of a Custom Ambilight."""

    def __init__(self, name, value, username, password, ip_address):
        """Initialize a Custom Ambilight."""
        self._name = name
        self._state = False
        self._brightness = 255
        self._username = username
        self._password = password
        self._ip_address = ip_address

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
            async with session.post(f"https://{self._ip_address}:1926/6/ambilight", auth=aiohttp.BasicAuth(self._username, self._password)) as response:
                if response.status == 200:
                    self._state = True
                    if ATTR_BRIGHTNESS in kwargs:
                        self._brightness = kwargs[ATTR_BRIGHTNESS]

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://{self._ip_address}:1926/6/ambilight", auth=aiohttp.BasicAuth(self._username, self._password)) as response:
                if response.status == 200:
                    self._state = False

    async def async_update(self):
        """Fetch new state data for this light."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://{self._ip_address}:1926/6/ambilight/currentconfiguration", auth=aiohttp.BasicAuth(self._username, self._password)) as response:
                if response.status == 200:
                    state_data = await response.json()
                    self._state = state_data["state"] == "on"
                    self._brightness = state_data["brightness"]
