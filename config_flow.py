import voluptuous as vol
from homeassistant import config_entries

class CustomAmbilightConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Custom Ambilight."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Custom Ambilight", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                    vol.Required("ip_address"): str,
                }
            ),
            errors=errors,
        )
