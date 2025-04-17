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
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from .const import (
    CONF_API_KEY,
    CONF_APP_ID,
    CONF_SECRET_KEY,
    DOMAIN,
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
        self.hass = hass
        self._config_entry = config_entry

        # Generate unique ID and set name
        app_id = config_entry.data[CONF_APP_ID]
        self._attr_unique_id = f"baidu_tts_{app_id}"
        self._attr_name = "百度语音合成"

        # Add device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, app_id)},
            name="百度语音",
            manufacturer="百度",
            model="语音合成服务",
            entry_type=DeviceEntryType.SERVICE,
        )

        _LOGGER.debug(
            "Initializing Baidu TTS entity with app_id: %s, unique_id: %s, name: %s",
            app_id,
            self._attr_unique_id,
            self._attr_name,
        )

        # Initialize the TTS client
        self._client = AipSpeech(
            app_id,
            config_entry.data[CONF_API_KEY],
            config_entry.data[CONF_SECRET_KEY],
        )

    @property
    def default_language(self) -> str:
        """Return the default language."""
        _LOGGER.debug("Getting default language: %s", TTS_DEFAULT_LANGUAGE)
        return TTS_DEFAULT_LANGUAGE

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        languages = list(TTS_LANGUAGES.keys())
        _LOGGER.debug("Getting supported languages: %s", languages)
        return languages

    @property
    def supported_options(self) -> list[str]:
        """Return list of supported options."""
        options = ["speed", "pitch", "volume", "voice", "fileformat"]
        _LOGGER.debug("Getting supported options: %s", options)
        return options

    @property
    def default_options(self) -> dict[str, Any]:
        """Return a dict of default options."""
        # Get current values from config_entry.options first, then data, then fall back to defaults
        options = {
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
        _LOGGER.debug("Getting default options: %s", options)
        return options

    @callback
    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        """Return a list of supported voices for a language."""
        voices = []
        for voice_id, voice_name in TTS_SUPPORTED_VOICES.items():
            voices.append(Voice(str(voice_id), voice_name))
        _LOGGER.debug("Getting supported voices for language %s: %s", language, voices)
        return voices

    def get_tts_audio(
        self, message: str, language: str, options: dict[str, Any]
    ) -> TtsAudioType:
        """Get TTS audio from Baidu."""
        _LOGGER.debug("=================== TTS Debug Info Start ===================")
        _LOGGER.debug("Message: %s", message)
        _LOGGER.debug("Language: %s", language)
        _LOGGER.debug("Raw options dict: %s", options)
        _LOGGER.debug("Config entry data: %s", self._config_entry.data)
        _LOGGER.debug("Config entry options: %s", self._config_entry.options)

        # 获取配置值，优先级：options > config_entry.options > config_entry.data > 默认值
        try:
            speed = int(
                options.get("speed")
                or self._config_entry.options.get("speed")
                or self._config_entry.data.get("speed")
                or TTS_DEFAULT_SPEED
            )
            pitch = int(
                options.get("pitch")
                or self._config_entry.options.get("pitch")
                or self._config_entry.data.get("pitch")
                or TTS_DEFAULT_PITCH
            )
            volume = int(
                options.get("volume")
                or self._config_entry.options.get("volume")
                or self._config_entry.data.get("volume")
                or TTS_DEFAULT_VOLUME
            )
            voice = int(
                options.get("voice")
                or self._config_entry.options.get("voice")
                or self._config_entry.data.get("voice")
                or TTS_DEFAULT_VOICE
            )
            fileformat = int(
                options.get("fileformat")
                or self._config_entry.options.get("fileformat")
                or self._config_entry.data.get("fileformat")
                or TTS_DEFAULT_FILEFORMAT
            )

            _LOGGER.debug(
                "Parsed values - speed: %s(%s), pitch: %s(%s), volume: %s(%s), "
                "voice: %s(%s), fileformat: %s(%s)",
                speed,
                type(speed),
                pitch,
                type(pitch),
                volume,
                type(volume),
                voice,
                type(voice),
                fileformat,
                type(fileformat),
            )

        except ValueError as ex:
            _LOGGER.error("Error parsing options: %s", ex)
            raise HomeAssistantError(f"Invalid option value: {ex}") from ex

        # 获取音频格式
        format_config = TTS_FILEFORMAT_MAP.get(fileformat, TTS_FILEFORMAT_MAP[6])
        _LOGGER.debug("Using audio format: %s", format_config)

        # 准备API参数
        api_params = {
            "spd": speed,
            "pit": pitch,
            "vol": volume,
            "per": voice,
            "aue": fileformat,
        }
        _LOGGER.debug("API parameters: %s", api_params)

        try:
            _LOGGER.debug("Calling Baidu TTS API")
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

        _LOGGER.debug("=================== TTS Debug Info End ===================")
        return format_config, result
