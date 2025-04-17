"""Config flow for Baidu TTS integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback

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
        vol.Optional(STT_CONF_LANGUAGE, default=STT_DEFAULT_LANGUAGE): vol.In(
            STT_LANGUAGES
        ),
    }
)


class BaiduTTSConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Baidu TTS."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            # Provide unique ID to prevent duplicate entries
            app_id = user_input[CONF_APP_ID]
            await self.async_set_unique_id(f"baidu_tts_{app_id}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title="百度语音合成", data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

    @classmethod
    @callback
    def async_get_options_flow(cls, config_entry: ConfigEntry) -> BaiduTTSOptionsFlow:
        """Get the options flow for this handler."""
        return BaiduTTSOptionsFlow()


class BaiduTTSOptionsFlow(OptionsFlow):
    """Baidu TTS integration options handler."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        data = self.config_entry.data

        schema = {
            vol.Required(
                CONF_APP_ID,
                default=options.get(CONF_APP_ID, data.get(CONF_APP_ID)),
            ): str,
            vol.Required(
                CONF_API_KEY,
                default=options.get(CONF_API_KEY, data.get(CONF_API_KEY)),
            ): str,
            vol.Required(
                CONF_SECRET_KEY,
                default=options.get(CONF_SECRET_KEY, data.get(CONF_SECRET_KEY)),
            ): str,
            vol.Required(
                TTS_CONF_LANGUAGE,
                default=options.get(TTS_CONF_LANGUAGE, data.get(TTS_CONF_LANGUAGE)),
            ): vol.In(TTS_LANGUAGES),
            vol.Optional(
                TTS_CONF_SPEED,
                default=options.get(
                    TTS_CONF_SPEED, data.get(TTS_CONF_SPEED, TTS_DEFAULT_SPEED)
                ),
            ): vol.All(vol.Coerce(int), vol.Range(min=0, max=9)),
            vol.Optional(
                TTS_CONF_PITCH,
                default=options.get(
                    TTS_CONF_PITCH, data.get(TTS_CONF_PITCH, TTS_DEFAULT_PITCH)
                ),
            ): vol.All(vol.Coerce(int), vol.Range(min=0, max=9)),
            vol.Optional(
                TTS_CONF_VOLUME,
                default=options.get(
                    TTS_CONF_VOLUME, data.get(TTS_CONF_VOLUME, TTS_DEFAULT_VOLUME)
                ),
            ): vol.All(vol.Coerce(int), vol.Range(min=0, max=15)),
            vol.Optional(
                TTS_CONF_VOICE,
                default=options.get(
                    TTS_CONF_VOICE, data.get(TTS_CONF_VOICE, TTS_DEFAULT_VOICE)
                ),
            ): vol.In(TTS_SUPPORTED_VOICES),
            vol.Optional(
                TTS_CONF_FILEFORMAT,
                default=options.get(
                    TTS_CONF_FILEFORMAT,
                    data.get(TTS_CONF_FILEFORMAT, TTS_DEFAULT_FILEFORMAT),
                ),
            ): vol.In(TTS_FILEFORMAT_MAP),
            vol.Optional(
                STT_CONF_LANGUAGE,
                default=options.get(
                    STT_CONF_LANGUAGE, data.get(STT_CONF_LANGUAGE, STT_DEFAULT_LANGUAGE)
                ),
            ): vol.In(STT_LANGUAGES),
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema),
        )
