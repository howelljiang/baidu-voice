"""Support for Baidu TTS."""
import logging
from typing import Any

from aip import AipSpeech
from homeassistant.components.tts import (
    TextToSpeechEntity,
    PLATFORM_SCHEMA,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    DEFAULT_SPEED,
    DEFAULT_PITCH,
    DEFAULT_VOLUME,
    DEFAULT_PERSON,
)

_LOGGER = logging.getLogger(__name__)

SUPPORT_LANGUAGES = ["zh", "en"]
DEFAULT_LANG = "zh"

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Baidu TTS from a config entry."""
    async_add_entities([BaiduTTSEntity(hass, config_entry)])
    return True

class BaiduTTSEntity(TextToSpeechEntity):
    """Baidu TTS Entity."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize Baidu TTS entity."""
        self.hass = hass
        self._config_entry = config_entry
        self._attr_name = "Baidu TTS"
        self._attr_unique_id = f"{DOMAIN}_tts"
        
        # 初始化百度语音合成客户端
        self._client = AipSpeech(
            config_entry.data["app_id"],
            config_entry.data["api_key"],
            config_entry.data["secret_key"]
        )

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return DEFAULT_LANG

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    async def async_get_tts_audio(self, message: str, language: str, options: dict = None) -> tuple[str, bytes]:
        """Load TTS from Baidu."""
        options = options or {}
        speed = options.get("speed", DEFAULT_SPEED)
        pitch = options.get("pitch", DEFAULT_PITCH)
        volume = options.get("volume", DEFAULT_VOLUME)
        person = options.get("person", DEFAULT_PERSON)

        try:
            result = await self.hass.async_add_executor_job(
                self._client.synthesis,
                message,
                language,
                1,  # 1: mp3
                {
                    "spd": speed,
                    "pit": pitch,
                    "vol": volume,
                    "per": person,
                }
            )
            
            if isinstance(result, dict):
                _LOGGER.error("Baidu TTS error: %s", result)
                return None, None
                
            return "mp3", result
            
        except Exception as ex:
            _LOGGER.error("Error during Baidu TTS: %s", ex)
            return None, None 