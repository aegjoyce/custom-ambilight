"""Light module for Custom Ambilight integration."""

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class CustomAmbilightLight(CoordinatorEntity, LightEntity):
    """Representation of a Custom Ambilight light."""

    def __init__(self, coordinator, entry_id) -> None:
        """Initialize the Custom Ambilight light."""
        super().__init__(coordinator)
        self.entry_id = entry_id
        self.api = coordinator.api
        self._attr_supported_features = LightEntityFeature.EFFECT
        self._attr_supported_color_modes = {ColorMode.HS}
        self._attr_color_mode = ColorMode.HS

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self.api.username

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.api.get_is_on()

    @property
    def brightness(self):
        """Return the brightness of the light."""
        # You need to implement how to get the brightness from the API
        return self.api.get_brightness()

    @property
    def hs_color(self):
        """Return the hue and saturation color value [float, float]."""
        # You need to implement how to get the color from the API
        return self.api.get_hs_color()

    @property
    def effect_list(self):
        """Return the list of supported effects."""
        return [effect["friendly_name"] for effect in self.api.EFFECTS.values()]

    @property
    def effect(self):
        """Return the current effect."""
        # You need to implement how to get the effect from the API
        return self.api.get_effect()

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        await self.coordinator.async_refresh()
        await self.api.turn_on(**kwargs)
        await self.coordinator.async_refresh()

    async def async_turn_off(self):
        """Turn the light off."""
        await self.coordinator.async_refresh()
        await self.api.turn_off()
        await self.coordinator.async_refresh()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up Custom Ambilight light based on a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [CustomAmbilightLight(api, entry.entry_id)], update_before_add=True
    )
