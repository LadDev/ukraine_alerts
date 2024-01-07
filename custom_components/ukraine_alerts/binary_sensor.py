from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import (
    ALERT_TYPE_AIR,
    ATTRIBUTION,
    DOMAIN,
    MANUFACTURER,
)

from . import alerts

import logging

_LOGGER = logging.getLogger(__name__)

BINARY_SENSOR_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key=ALERT_TYPE_AIR,
        translation_key="air",
        device_class=BinarySensorDeviceClass.SAFETY,
        icon="mdi:cloud",
    ),
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    air_alerts = hass.data[DOMAIN][config_entry.entry_id]
    new_devices = []

    for binary_sensor_type in BINARY_SENSOR_TYPES:
        new_devices.append(AirDangerousBinarySensor(air_alerts.device, binary_sensor_type))

    if new_devices:
        async_add_entities(new_devices)

class AirDangerousBinarySensor(BinarySensorEntity):

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    
    def __init__(self, module: alerts.AlertRegion, sensor_type: BinarySensorEntityDescription):
        self._module = module
        self._sensor_type = sensor_type
        
        self._attr_unique_id = f"{self._module.get_region_id}-danger-{sensor_type.key}".lower()

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"{self._module.get_region_id}-danger")},
            manufacturer=MANUFACTURER,
            name="Air",
            configuration_url="https://alerts.com.ua/",
        )

        self._attr_name = f"Air"
        self._state = self._module.get_region_alert

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        translations = await self.hass.helpers.translation.async_get_translations(
            self.hass.config.language,
            "binary_sensor"
        )

        _LOGGER.error("Translations: %s", translations)
        _LOGGER.debug("Translations: %s", translations)
        self._state_on = translations["component.ukraine_alerts.binary_sensor.state.on"]
        self._state_off = translations["component.ukraine_alerts.binary_sensor.state.off"]

    @property
    def unique_id(self):
        return f"{self._module.get_region_id}_{self._sensor_type.key}"

    @property
    def name(self):
        return f"{self._sensor_type.key}"

    @property
    def device_class(self):
        return self._sensor_type.device_class

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._module.get_region_id)}}

    @property
    def icon(self):
        return self._sensor_type.icon

    @property
    def is_on(self):
        return self._module.get_region_alert

    @property
    def state(self):
        return self._state_on if self.is_on else self._state_off
