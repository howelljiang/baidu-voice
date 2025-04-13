"""Support for Baidu Wake Word Detection."""
import logging
import asyncio
from aip import AipSpeech
import voluptuous as vol

from homeassistant.components.wake_word import (
    WakeWordDetectionResult,
    WakeWordDetectionResultState,
    WakeWordProvider,
)
from homeassistant.const import CONF_API_KEY
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_APP_ID,
    CONF_API_KEY,
    CONF_SECRET_KEY,
    CONF_WAKE_WORD,
    DEFAULT_WAKE_WORD,
)

_LOGGER = logging.getLogger(__name__)

SUPPORT_LANGUAGES = ["zh", "en"]
DEFAULT_LANG = "zh"

async def async_get_engine(hass, config, discovery_info=None):
    """Set up Baidu Wake Word component."""
    _LOGGER.debug("Setting up Baidu Wake Word engine")
    return BaiduWakeWordProvider(hass)

class BaiduWakeWordProvider(WakeWordProvider):
    """Baidu Wake Word api provider."""

    def __init__(self, hass):
        """Initialize Baidu Wake Word provider."""
        self.hass = hass
        self._app_id = hass.data[DOMAIN][CONF_APP_ID]
        self._api_key = hass.data[DOMAIN][CONF_API_KEY]
        self._secret_key = hass.data[DOMAIN][CONF_SECRET_KEY]
        self._wake_word = hass.data[DOMAIN][CONF_WAKE_WORD]
        self._client = AipSpeech(self._app_id, self._api_key, self._secret_key)
        self.name = "Baidu Wake Word"
        self._language = hass.config.language or DEFAULT_LANG
        _LOGGER.debug("Initialized Baidu Wake Word provider with language: %s", self._language)

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    @property
    def supported_formats(self):
        """Return list of supported formats."""
        return ["wav", "pcm"]

    @property
    def supported_sample_rates(self):
        """Return list of supported sample rates."""
        return [16000]

    @property
    def supported_channels(self):
        """Return list of supported channels."""
        return [1]

    async def async_process_audio_stream(self, stream, options=None):
        """Process an audio stream to wake word service."""
        _LOGGER.debug("Processing audio stream for wake word detection")
        options = options or {}
        language = options.get("language", self._language)
        _LOGGER.debug("Using language: %s", language)

        try:
            # 读取音频流
            audio_data = b""
            async for chunk in stream:
                if chunk:
                    audio_data += chunk
                    _LOGGER.debug("Received audio chunk of size: %d", len(chunk))

            if not audio_data:
                _LOGGER.warning("No audio data received")
                return WakeWordDetectionResult(
                    state=WakeWordDetectionResultState.ERROR,
                    wake_word=None,
                )

            _LOGGER.debug("Total audio data size: %d bytes", len(audio_data))

            def _process_audio():
                try:
                    # 使用百度语音识别API进行唤醒词检测
                    result = self._client.asr(audio_data, 'pcm', 16000, {
                        'dev_pid': 1536 if language == 'zh' else 1737,  # 1536: 普通话, 1737: 英语
                    })
                    
                    _LOGGER.debug("ASR result: %s", result)
                    
                    if result.get('err_no') == 0:
                        text = result.get('result')[0]
                        _LOGGER.debug("Recognized text: %s", text)
                        # 检查是否包含唤醒词
                        if self._wake_word in text:
                            _LOGGER.debug("Wake word detected: %s", self._wake_word)
                            return self._wake_word
                        _LOGGER.debug("No wake word detected")
                        return None
                    _LOGGER.warning("ASR error: %s", result)
                    return None
                except Exception as ex:
                    _LOGGER.error("Error during Baidu Wake Word processing: %s", ex, exc_info=True)
                    return None

            wake_word = await self.hass.async_add_executor_job(_process_audio)
            if wake_word is None:
                _LOGGER.debug("No wake word detected")
                return WakeWordDetectionResult(
                    state=WakeWordDetectionResultState.ERROR,
                    wake_word=None,
                )
            _LOGGER.debug("Successfully detected wake word: %s", wake_word)
            return WakeWordDetectionResult(
                state=WakeWordDetectionResultState.SUCCESS,
                wake_word=wake_word,
            )
        except Exception as ex:
            _LOGGER.error("Error during Baidu Wake Word: %s", ex, exc_info=True)
            return WakeWordDetectionResult(
                state=WakeWordDetectionResultState.ERROR,
                wake_word=None,
            ) 