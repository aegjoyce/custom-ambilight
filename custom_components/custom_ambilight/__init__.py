"""The Custom Ambilight integration."""
import voluptuous as vol
from homeassistant import config_entries, core
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import config_validation as cv

from .light import setup_platform

DOMAIN = "custom_ambilight"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: core.HomeAssistant, config: dict):
    """Set up the Custom Ambilight component."""
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["config"] = config.get(DOMAIN) or {}
    return True

async def async_setup_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up Custom Ambilight from a config entry."""
    setup_platform(hass, hass.data[DOMAIN]["config"], add_entities=None)
    return True
