
from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "ukraine_alerts"
ALERTS_API_URL = "https://alerts.com.ua/api/states"
ATTRIBUTION = "Data provided by Ukraine Alerts"
MANUFACTURER = "Ukraine Alerts"
ALERT_TYPE_UNKNOWN = "UNKNOWN"
ALERT_TYPE_AIR = "AIR"
ALERT_TYPES = {
    ALERT_TYPE_AIR,
}
PLATFORMS = [Platform.BINARY_SENSOR]