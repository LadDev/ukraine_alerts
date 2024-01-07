from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from .const import DOMAIN  

_LOGGER = logging.getLogger(__name__)

REGION_OPTIONS = {
    1: "Vinnytsia oblast",
    2: "Volyn oblast",
    3: "Dnipropetrovsk oblast",
    4: "Donetsk oblast",
    5: "Zhytomyr oblast",
    6: "Zakarpattia oblast",
    7: "Zaporizhzhia oblast",
    8: "Ivano-Frankivsk oblast",
    9: "Kyiv oblast",
    10: "Kirovohrad oblast",
    11: "Luhansk oblast",
    12: "Lviv oblast",
    13: "Mykolaiv oblast",
    14: "Odesa oblast",
    15: "Poltava oblast",
    16: "Rivne oblast",
    17: "Sumy oblast",
    18: "Ternopil oblast",
    19: "Kharkiv oblast",
    20: "Kherson oblast",
    21: "Khmelnytskyi oblast",
    22: "Cherkasy oblast",
    23: "Chernivtsi oblast",
    24: "Chernihiv oblast",
    25: "Kyiv"
}

DATA_SCHEMA = vol.Schema({
    "api_key": str,
    "region": vol.All(vol.Coerce(int), vol.In(REGION_OPTIONS)),
})

async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    if len(data["api_key"]) < 3:
        raise InvalidApiKey
    if data["region"] not in REGION_OPTIONS:
        raise InvalidRegion

    region_name = REGION_OPTIONS.get(data["region"], "Unknown Region")

    return {"title": region_name}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):

        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except InvalidApiKey:
                errors["api_key"] = "invalid_api_key"
            except InvalidRegion:
                errors["region"] = "invalid_region"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class InvalidApiKey(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid api key."""


class InvalidRegion(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid region."""