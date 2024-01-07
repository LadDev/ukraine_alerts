from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta
import asyncio
from .const import DOMAIN
from . import alerts
import logging

from .const import ALERT_TYPES, DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    air_alerts = alerts.ALERTS(hass, entry.data["api_key"], entry.data["region"])
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = air_alerts
    
    air_alerts.update_task = async_track_time_interval(hass, air_alerts.update_data, timedelta(seconds=15))

    await asyncio.to_thread(air_alerts.pull_data)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    air_alerts = hass.data[DOMAIN][config.entry_id]
    new_devices = []
    
    for binary_sensor_type in BINARY_SENSOR_TYPES:
        new_devices.append(AirDangerousBinarySensor(air_alerts, binary_sensor_type))

    if new_devices:
        async_add_entities(new_devices)
        return True

    return False

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        air_alerts = hass.data[DOMAIN][entry.entry_id]
        air_alerts.update_task()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok