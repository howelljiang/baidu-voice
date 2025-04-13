"""Baidu Speech-to-Text integration."""
import logging
from typing import Any

from aip import AipSpeech
from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechToTextEntity,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Baidu STT from a config entry."""
    async_add_entities([BaiduSTTEntity(hass, config_entry)])
    return True

class BaiduSTTEntity(SpeechToTextEntity):
    """Baidu Speech-to-Text entity."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize Baidu STT entity."""
        self.hass = hass
        self._config_entry = config_entry
        self._attr_name = "Baidu STT"
        self._attr_unique_id = f"{DOMAIN}_stt"
        
        # 初始化百度语音识别客户端
        self._client = AipSpeech(
            config_entry.data["app_id"],
            config_entry.data["api_key"],
            config_entry.data["secret_key"]
        )

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return ["zh-CN"]

    @property
    def supported_formats(self) -> list[AudioFormats]:
        """Return a list of supported formats."""
        return [AudioFormats.WAV, AudioFormats.OGG]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        """Return a list of supported codecs."""
        return [AudioCodecs.PCM, AudioCodecs.OPUS]

    @property
    def supported_bit_rates(self) -> list[AudioBitRates]:
        """Return a list of supported bit rates."""
        return [AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]:
        """Return a list of supported sample rates."""
        return [AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[AudioChannels]:
        """Return a list of supported channels."""
        return [AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream: Any
    ) -> SpeechResult:
        """Process an audio stream to STT service."""
        try:
            # 读取音频数据
            audio_data = b""
            async for chunk in stream:
                audio_data += chunk

            if not audio_data:
                _LOGGER.warning("No audio data received")
                return SpeechResult("", SpeechResultState.ERROR)
            
            _LOGGER.debug("Processing audio stream with metadata: %s", metadata)
            _LOGGER.debug("Total audio data size: %d bytes", len(audio_data))
            
            # 使用百度语音识别API
            result = await self.hass.async_add_executor_job(
                self._client.asr,
                audio_data,
                'pcm',
                16000,
                {
                    'dev_pid': 1537,  # 普通话(支持简单的英文识别)
                }
            )
            
            _LOGGER.debug("Baidu STT response: %s", result)
            
            if result.get('err_no') == 0:
                text = result.get('result', [""])[0]
                return SpeechResult(text, SpeechResultState.SUCCESS)
            else:
                _LOGGER.error("Baidu STT error: %s", result.get('err_msg'))
                return SpeechResult("", SpeechResultState.ERROR)
                
        except Exception as ex:
            _LOGGER.error("Error during Baidu STT: %s", ex, exc_info=True)
            return SpeechResult("", SpeechResultState.ERROR) 