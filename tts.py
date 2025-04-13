"""Support for Baidu TTS."""
import logging
import asyncio
from aip import AipSpeech
import voluptuous as vol

from homeassistant.components.tts import Provider, PLATFORM_SCHEMA
from homeassistant.const import CONF_API_KEY
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_APP_ID,
    CONF_API_KEY,
    CONF_SECRET_KEY,
    DEFAULT_SPEED,
    DEFAULT_PITCH,
    DEFAULT_VOLUME,
    DEFAULT_PERSON,
)

_LOGGER = logging.getLogger(__name__)

SUPPORT_LANGUAGES = ["zh", "en"]
DEFAULT_LANG = "zh"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_APP_ID): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_SECRET_KEY): cv.string,
    }
)

async def async_get_engine(hass, config, discovery_info=None):
    """Set up Baidu TTS component."""
    return BaiduTTSProvider(hass)

class BaiduTTSProvider(Provider):
    """Baidu TTS api provider."""

    def __init__(self, hass):
        """Initialize Baidu TTS provider."""
        self.hass = hass
        self._app_id = hass.data[DOMAIN][CONF_APP_ID]
        self._api_key = hass.data[DOMAIN][CONF_API_KEY]
        self._secret_key = hass.data[DOMAIN][CONF_SECRET_KEY]
        self._client = AipSpeech(self._app_id, self._api_key, self._secret_key)
        self.name = "Baidu TTS"

    @property
    def default_language(self):
        """Return the default language."""
        return DEFAULT_LANG

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    async def async_get_tts_audio(self, message, language, options=None):
        """Load TTS from Baidu."""
        options = options or {}
        speed = options.get("speed", DEFAULT_SPEED)
        pitch = options.get("pitch", DEFAULT_PITCH)
        volume = options.get("volume", DEFAULT_VOLUME)
        person = options.get("person", DEFAULT_PERSON)

        def _get_tts():
            result = self._client.synthesis(
                message,
                language,
                1,  # 1: mp3
                {
                    "spd": speed,
                    "pit": pitch,
                    "vol": volume,
                    "per": person,
                },
            )
            if isinstance(result, dict):
                _LOGGER.error("Baidu TTS error: %s", result)
                return None, None
            return "mp3", result

        try:
            audio_type, audio_data = await self.hass.async_add_executor_job(_get_tts)
            return audio_type, audio_data
        except Exception as ex:
            _LOGGER.error("Error during Baidu TTS: %s", ex)
            return None, None 