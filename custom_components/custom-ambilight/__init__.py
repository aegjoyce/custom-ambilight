import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from .light import CustomAmbilight

DOMAIN = "CustomAmbilight"

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: cv.schema_with_slug_keys(vol.Any(cv.boolean, cv.string))},
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the Custom Ambilight integration."""
    hass.config_entries.async_register_flow(DOMAIN, CustomAmbilight)
    return True
