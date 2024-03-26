class CustomAmbilightConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Custom Ambilight."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Test the connection
            connection_successful = await self.test_connection(user_input)
            if connection_successful:
                return self.async_create_entry(title="Custom Ambilight", data=user_input)
            else:
                errors["base"] = "cannot_connect"

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

    async def test_connection(self, user_input):
        """Test the connection to the device."""
        url = f"https://{user_input['ip_address']}:1926/6/ambilight/currentconfiguration"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, auth=aiohttp.BasicAuth(user_input['username'], user_input['password'])) as response:
                    return response.status == 200
            except Exception as e:
                self._LOGGER.error("Error connecting to device at %s: %s", url, e)
                return False
