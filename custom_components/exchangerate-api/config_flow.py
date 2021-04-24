import logging
import voluptuous as vol

from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv # pylint: disable=import-error
from homeassistant.const import ( # pylint: disable=import-error
    CONF_BASE,
    CONF_API_KEY,
    CONF_QUOTE,
)
from .const import (
    DOMAIN,
    DEFAULT_BASE,
    AVAILABLE_CURRENCIES
)

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_BASE, default=DEFAULT_BASE): vol.In(AVAILABLE_CURRENCIES),
        vol.Required(CONF_QUOTE): vol.In(AVAILABLE_CURRENCIES),
    }
)

class ExchangerateApiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Exchangerateio config flow."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return await self.async_step_import(user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    async def async_step_import(self, user_input=None):
        """Handle import."""
        title = f"{user_input[CONF_BASE]} in {user_input[CONF_QUOTE]}"
        await self.async_set_unique_id(title)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=title, data=user_input)

