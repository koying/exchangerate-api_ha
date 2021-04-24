"""The exchangeratesapi component."""
import asyncio
from datetime import timedelta
import logging
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import aiohttp_client, entity_registry, update_coordinator

from .const import DOMAIN
PLATFORMS = ["sensor"]
MAIN_URL = "https://v6.exchangerate-api.com/v6/{apikey}/latest/{base}"

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the exchangeratesapi component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up exchangeratesapi from a config entry."""
    if not entry.unique_id:
        hass.config_entries.async_update_entry(entry, unique_id=entry.title)

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    return unload_ok


async def get_coordinator(hass, key, base):
    """Get the data update coordinator."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    
    if base in hass.data[DOMAIN]:
        return hass.data[DOMAIN][base]

    async def async_get_base():
        with async_timeout.timeout(10):
            session = aiohttp_client.async_get_clientsession(hass)
            result = await session.get(MAIN_URL.format(apikey=key, base=base))
            data = await result.json()
            return data["conversion_rates"]

    hass.data[DOMAIN][base] = update_coordinator.DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name=DOMAIN,
        update_method=async_get_base,
        update_interval=timedelta(hours=24),
    )
    await hass.data[DOMAIN][base].async_refresh()
    return hass.data[DOMAIN][base]
