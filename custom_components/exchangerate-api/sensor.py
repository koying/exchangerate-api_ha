"""Support for ExchangerateApi.org exchange rates service."""
import logging
import voluptuous as vol  # pylint: disable=import-error

import homeassistant.helpers.config_validation as cv # pylint: disable=import-error
from homeassistant.const import ( # pylint: disable=import-error
    ATTR_ATTRIBUTION,
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_API_KEY,
    CONF_BASE,
    CONF_NAME,
    CONF_QUOTE,
)
from homeassistant.helpers.entity import Entity # pylint: disable=import-error
from homeassistant.components.sensor import PLATFORM_SCHEMA # pylint: disable=import-error

from . import get_coordinator
from .const import (
    DOMAIN,
    DEFAULT_BASE,
    DEFAULT_NAME,
    ATTRIBUTION
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_QUOTE): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_BASE, default=DEFAULT_BASE): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor."""
    name = config.get(CONF_NAME)
    key = config.get(CONF_API_KEY)
    base = config.get(CONF_BASE)
    quote = config.get(CONF_QUOTE)

    coordinator = await get_coordinator(hass, key, base)

    async_add_entities(
        [ExchangerateApiSensor(coordinator, name, base, quote)]
    )

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Defer sensor setup to the shared sensor module."""
    name = config_entry.title
    key = config_entry.data[CONF_API_KEY]
    base = config_entry.data[CONF_BASE]
    quote = config_entry.data[CONF_QUOTE]

    coordinator = await get_coordinator(hass, key, base)

    async_add_entities(
        [ExchangerateApiSensor(coordinator, name, base, quote)]
    )
class ExchangerateApiSensor(Entity):
    """Representation of an Open Exchange Rates sensor."""
    name = None
    unique_id = None

    def __init__(self, coordinator, name, base, quote):
        """Initialize the sensor."""

        self._base = base
        self._quote = quote
        self.name = name
        self.unique_id = f"{self._base}-{self._quote}"
        self.coordinator = coordinator

    @property
    def available(self):
        """Return if sensor is available."""
        return self.coordinator.last_update_success and (
            self._quote in self.coordinator.data
        )

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return "mdi:currency-" + self._base.lower()

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self._quote]

    @property
    def device_state_attributes(self):
        """Return other attributes of the sensor."""
        return {ATTR_ATTRIBUTION: ATTRIBUTION, ATTR_UNIT_OF_MEASUREMENT: self._quote}

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """When entity will be removed from hass."""
        self.coordinator.async_remove_listener(self.async_write_ha_state)
