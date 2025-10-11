"""Config flow for Custom Ambilight integration."""

from __future__ import annotations

import logging
from typing import Any
import random
import string
from base64 import b64decode
from Crypto.Hash import HMAC, SHA

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .api import MyApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_TYPE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_TYPE, default="https"): vol.In(["http", "https"]),
    }
)

STEP_HTTP_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
    }
)

STEP_HTTPS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

# Helper function to create a device ID
def create_device_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Helper function to create a signature
def create_signature(secret_key: str, to_sign: bytes) -> str:
    sign = HMAC.new(b64decode(secret_key), to_sign, SHA)
    return sign.hexdigest()

SECRET_KEY = "ZmVay1EQVFOaZhwQ4Kv81ypLAZNczV9sG4KkseXWn1NEk6cXmPKO/MCa9sryslvLCFMnNe4Z4CPXzToowvhHvA=="

async def pair_device(host: str) -> dict:
    """Pair with the Philips TV and retrieve credentials."""
    import aiohttp

    device_id = create_device_id()
    device_spec = {
        "device_name": "CustomAmbilight",
        "device_os": "Android",
        "app_name": "HomeAssistant",
        "type": "native",
        "id": device_id,
        "app_id": "app.id",
    }

    async with aiohttp.ClientSession() as session:
        # Step 1: Send pairing request
        pair_url = f"https://{host}:1926/6/pair/request"
        pair_data = {"scope": ["read", "write", "control"], "device": device_spec}
        async with session.post(pair_url, json=pair_data, ssl=False) as response:
            if response.status != 200:
                raise CannotConnect
            pair_response = await response.json()

        # Step 2: Prompt user for PIN
        pin = input("Enter the PIN displayed on the TV: ")

        # Step 3: Send grant request
        grant_url = f"https://{host}:1926/6/pair/grant"
        auth_timestamp = pair_response["timestamp"]
        auth_signature = create_signature(SECRET_KEY, f"{auth_timestamp}{pin}".encode())
        grant_data = {
            "auth_AppId": "1",
            "pin": pin,
            "auth_timestamp": auth_timestamp,
            "auth_signature": auth_signature,
        }
        async with session.post(grant_url, json=grant_data, ssl=False) as response:
            if response.status != 200:
                raise InvalidAuth
            grant_response = await response.json()

    return {
        CONF_USERNAME: device_id,
        CONF_PASSWORD: grant_response["auth_key"],
    }


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_HTTP_SCHEMA or STEP_HTTPS_SCHEMA with values provided by the user.
    """
    # Create API instance
    api = MyApi(
        data[CONF_HOST],
        data.get(CONF_TYPE),
        data.get(CONF_USERNAME),
        data.get(CONF_PASSWORD),
    )

    # Validate the API connection (and authentication)
    if not await api.validate_connection():
        raise InvalidAuth

    # Return info that you want to store in the config entry.
    return {"title": "Custom Ambilight"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Custom Ambilight."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            self.connection_type = user_input[CONF_TYPE]
            if self.connection_type == "https":
                return await self.async_step_https()
            else:
                return await self.async_step_http()

        return self.async_show_form(step_id="user", data_schema=STEP_TYPE_SCHEMA)

    async def async_step_http(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the HTTP step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            user_input[CONF_TYPE] = "http"
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="http", data_schema=STEP_HTTP_SCHEMA, errors=errors
        )

    async def async_step_https(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the HTTPS step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            user_input[CONF_TYPE] = "https"
            try:
                # Automatically pair and retrieve credentials
                credentials = await pair_device(user_input[CONF_HOST])
                user_input.update(credentials)

                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="https", data_schema=STEP_HTTPS_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
