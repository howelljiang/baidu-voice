"""Support for Baidu TTS."""

from __future__ import annotations

import logging
from typing import Any

from aip import AipSpeech

from homeassistant.components.tts import (
    TextToSpeechEntity,
    TtsAudioType,
    Voice,
    callback,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_API_KEY,
    CONF_APP_ID,
    CONF_SECRET_KEY,
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


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities,
) -> None:
    """Set up Baidu TTS from a config entry."""
    _LOGGER.debug("Setting up Baidu TTS")
    entity = BaiduTTSEntity(hass, config_entry)
    async_add_entities([entity])


class BaiduTTSEntity(TextToSpeechEntity):
    """Represent a Baidu TTS entity."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the Baidu TTS entity."""

        self._config_entry = config_entry
        # Generate unique ID and set name
        app_id = config_entry.data[CONF_APP_ID]
        self._attr_unique_id = f"baidu_tts_{app_id}"
        self._attr_name = "Baidu TTS"

        # Initialize the TTS client
        self._client = AipSpeech(
            app_id,
            config_entry.data[CONF_API_KEY],
            config_entry.data[CONF_SECRET_KEY],
        )

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return TTS_DEFAULT_LANGUAGE

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return list(TTS_LANGUAGES.keys())

    @property
    def supported_options(self) -> list[str]:
        """Return list of supported options."""
        return ["speed", "pitch", "volume", "voice", "fileformat"]

    @property
    def default_options(self) -> dict[str, Any]:
        """Return a dict of default options."""
        # Get current values from config_entry.options first, then data, then fall back to defaults
        return {
            "speed": self._config_entry.options.get(
                "speed", self._config_entry.data.get("speed", TTS_DEFAULT_SPEED)
            ),
            "pitch": self._config_entry.options.get(
                "pitch", self._config_entry.data.get("pitch", TTS_DEFAULT_PITCH)
            ),
            "volume": self._config_entry.options.get(
                "volume", self._config_entry.data.get("volume", TTS_DEFAULT_VOLUME)
            ),
            "voice": self._config_entry.options.get(
                "voice", self._config_entry.data.get("voice", TTS_DEFAULT_VOICE)
            ),
            "fileformat": self._config_entry.options.get(
                "fileformat",
                self._config_entry.data.get("fileformat", TTS_DEFAULT_FILEFORMAT),
            ),
        }

    @callback
    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        """Return a list of supported voices for a language."""
        voices = []
        for voice_id, voice_name in TTS_SUPPORTED_VOICES.items():
            voices.append(Voice(str(voice_id), voice_name))
        return voices

    def get_tts_audio(
        self, message: str, language: str, options: dict[str, Any]
    ) -> TtsAudioType:
        """Get TTS audio from Baidu."""

        # options > config_entry.data > default
        try:
            speed = int(
                options.get("speed")
                or self._config_entry.data.get("speed")
                or TTS_DEFAULT_SPEED
            )
            pitch = int(
                options.get("pitch")
                or self._config_entry.data.get("pitch")
                or TTS_DEFAULT_PITCH
            )
            volume = int(
                options.get("volume")
                or self._config_entry.data.get("volume")
                or TTS_DEFAULT_VOLUME
            )
            voice = int(
                options.get("voice")
                or self._config_entry.data.get("voice")
                or TTS_DEFAULT_VOICE
            )
            fileformat = int(
                options.get("fileformat")
                or self._config_entry.data.get("fileformat")
                or TTS_DEFAULT_FILEFORMAT
            )

        except ValueError as ex:
            _LOGGER.error("Error parsing options: %s", ex)
            raise HomeAssistantError(f"Invalid option value: {ex}") from ex

        format_config = TTS_FILEFORMAT_MAP.get(fileformat, TTS_FILEFORMAT_MAP[6])
        _LOGGER.debug("Using audio format: %s", format_config)

        api_params = {
            "spd": speed,
            "pit": pitch,
            "vol": volume,
            "per": voice,
            "aue": fileformat,
        }
        _LOGGER.debug("API parameters: %s", api_params)

        try:
            result = self._client.synthesis(
                message,
                language,
                1,  # Use standard voice synthesis
                api_params,
            )

            if isinstance(result, dict):
                error_msg = result.get("err_msg", "Unknown error")
                error_no = result.get("err_no", "Unknown")
                _LOGGER.error(
                    "Baidu TTS API error - error_no: %s, error_msg: %s, full_result: %s",
                    error_no,
                    error_msg,
                    result,
                )
                return None, None

            _LOGGER.debug("Successfully generated audio, size: %d bytes", len(result))

        except Exception as ex:
            _LOGGER.error(
                "Error during TTS generation: %s, type: %s",
                str(ex),
                type(ex).__name__,
            )
            raise HomeAssistantError("Failed to generate TTS audio") from ex
        return format_config, result
