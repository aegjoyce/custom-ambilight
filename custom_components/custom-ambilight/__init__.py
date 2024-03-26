import homeassistant.helpers.config_validation as cv
import voluptuous as vol

DOMAIN = "CustomAmbilight"

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: cv.schema_with_slug_keys(vol.Any(cv.boolean, cv.string))},
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the Custom Ambilight integration."""
    return True
