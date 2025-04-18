"""Config flow for Baidu Voice integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_API_KEY,
    CONF_APP_ID,
    CONF_SECRET_KEY,
    DOMAIN,
    STT_CONF_LANGUAGE,
    STT_DEFAULT_LANGUAGE,
    STT_LANGUAGES,
    TTS_CONF_FILEFORMAT,
    TTS_CONF_LANGUAGE,
    TTS_CONF_PITCH,
    TTS_CONF_SPEED,
    TTS_CONF_VOICE,
    TTS_CONF_VOLUME,
    TTS_DEFAULT_FILEFORMAT,
    TTS_DEFAULT_LANGUAGE,
    TTS_DEFAULT_PITCH,
    TTS_DEFAULT_SPEED,
    TTS_DEFAULT_VOICE,
    TTS_DEFAULT_VOLUME,
    TTS_FILEFORMAT_MAP,
    TTS_LANGUAGES,
    TTS_SUPPORTED_VOICES,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_APP_ID): str,
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_SECRET_KEY): str,
        vol.Required(TTS_CONF_LANGUAGE, default=TTS_DEFAULT_LANGUAGE): vol.In(
            TTS_LANGUAGES
        ),
        vol.Optional(TTS_CONF_SPEED, default=TTS_DEFAULT_SPEED): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=9)
        ),
        vol.Optional(TTS_CONF_PITCH, default=TTS_DEFAULT_PITCH): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=9)
        ),
        vol.Optional(TTS_CONF_VOLUME, default=TTS_DEFAULT_VOLUME): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=15)
        ),
        vol.Optional(TTS_CONF_VOICE, default=TTS_DEFAULT_VOICE): vol.In(
            TTS_SUPPORTED_VOICES
        ),
        vol.Optional(TTS_CONF_FILEFORMAT, default=TTS_DEFAULT_FILEFORMAT): vol.In(
            TTS_FILEFORMAT_MAP
        ),
        vol.Optional(STT_CONF_LANGUAGE, default=STT_DEFAULT_LANGUAGE): vol.In(
            STT_LANGUAGES
        ),
    }
)


class BaiduVoiceConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Baidu Voice."""

    VERSION = 1

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Handle reconfiguration of the integration."""
        if user_input is not None:
            return self.async_update_reload_and_abort(
                self._get_reconfigure_entry(),
                data_updates=user_input,
            )

        schema = self.add_suggested_values_to_schema(
            STEP_USER_DATA_SCHEMA, self._get_reconfigure_entry().data
        )
        schema = schema.extend(
            {
                vol.Required(CONF_APP_ID): SelectSelector(
                    SelectSelectorConfig(
                        options=[self._get_reconfigure_entry().data[CONF_APP_ID]],
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=schema,
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            app_id = user_input[CONF_APP_ID]
            await self.async_set_unique_id(f"baidu_voice_{app_id}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Baidu Voice", data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)
