import requests
import json
import asyncio
import logging
import time
from homeassistant.core import HomeAssistant

from .const import ALERTS_API_URL

_LOGGER = logging.getLogger(__name__)

class ALERTS:
    def __init__(self, hass: HomeAssistant, api_key: str, region: int) -> None:
        self._api_key = api_key
        self._region = region
        self.hass:HomeAssistant = hass
        self.device = None

    def pull_data(self):
        try:
            response = requests.get(f"{ALERTS_API_URL}/{self._region}",headers={'Content-Type': 'application/json', "x-api-key": self._api_key})
            self._states = json.loads(response.text)["state"]
            self.device = AlertRegion(self._states, self)
        except Exception as e:
            _LOGGER.error(f"Error pull data data: {e}")

    async def update_data(self, now=None):
        try:
            response = await self.hass.async_add_executor_job(
                self.fetch_data
            )

            self._states = json.loads(response.text)["state"]

            if self.device is None:
                self.device = AlertRegion(self._states, self)
            else:
                self.device.set_region_alert(self._states["alert"])

        except Exception as e:
            _LOGGER.error(f"Error updating data: {e}")
    
    def fetch_data(self):
        return requests.get(f"{ALERTS_API_URL}/{self._region}", headers={'Content-Type': 'application/json', "x-api-key": self._api_key})

class AlertRegion:
    def __init__(self,moduleDescription: json, alerts: ALERTS):
        self._alerts = alerts
        self.model_name = "AUA001"
        self._hass:HomeAssistant = alerts.hass
        self._id = moduleDescription["id"]
        self._name = moduleDescription["name"]
        self._name_en = moduleDescription["name_en"]
        self._alert = moduleDescription["alert"]
        self._change = moduleDescription["changed"]

    def set_region_alert(self,alert):
        self._alert = alert

    @property
    def get_region_id(self) -> int:
        return self._id

    @property
    def get_region_name(self) -> str:
        return self._name

    @property
    def get_region_name_en(self) -> str:
        return self._name_en

    @property
    def get_region_alert(self) -> bool:
        return self._alert