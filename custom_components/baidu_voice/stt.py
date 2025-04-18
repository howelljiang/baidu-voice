"""Support for Baidu speech recognition."""

from __future__ import annotations

import logging
from typing import Any

from aip import AipSpeech

from homeassistant.components import stt
from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    CONF_API_KEY,
    CONF_APP_ID,
    CONF_SECRET_KEY,
    STT_DEFAULT_LANGUAGE,
    STT_LANGUAGES_CODE_MAP,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Baidu STT platform via config entry."""
    async_add_entities(
        [
            BaiduSTTEntity(hass, config_entry.data),
        ]
    )


class BaiduSTTEntity(stt.SpeechToTextEntity):
    """Baidu speech-to-text entity."""

    def __init__(self, hass: HomeAssistant, config: dict[str, Any]) -> None:
        """Initialize Baidu speech-to-text entity."""
        self.hass = hass
        self._config = config
        self._client = AipSpeech(
            config[CONF_APP_ID],
            config[CONF_API_KEY],
            config[CONF_SECRET_KEY],
        )
        self._attr_name = "Baidu STT"
        self._attr_unique_id = f"baidu_stt_{config[CONF_APP_ID]}"

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return ["zh-CN", "en-US", "zh-HK", "zh-TW"]

    @property
    def supported_formats(self) -> list[str]:
        """Return list of supported formats."""
        return [AudioFormats.WAV, "pcm"]

    @property
    def supported_codecs(self) -> list[str]:
        """Return list of supported codecs."""
        return [AudioCodecs.PCM]

    @property
    def supported_bit_rates(self) -> list[int]:
        """Return list of supported bit rates."""
        return [AudioBitRates.BITRATE_8, AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[int]:
        """Return list of supported sample rates."""
        return [AudioSampleRates.SAMPLERATE_8000, AudioSampleRates.SAMPLERATE_16000]

    @property
    def supported_channels(self) -> list[int]:
        """Return list of supported channels."""
        return [AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
        self, metadata: stt.SpeechMetadata, stream: stt.AudioStream
    ) -> stt.SpeechResult:
        """Process an audio stream for speech recognition."""
        try:
            audio_data = b""
            async for chunk in stream:
                audio_data += chunk
            _LOGGER.debug("Metadata: %s", metadata)
            result = await self.hass.async_add_executor_job(
                self._client.asr,
                audio_data,
                metadata.format,
                metadata.sample_rate,
                {
                    "dev_pid": STT_LANGUAGES_CODE_MAP.get(
                        metadata.language, STT_DEFAULT_LANGUAGE
                    ),
                    "channel": metadata.channel,
                },
            )

            if not isinstance(result, dict):
                return stt.SpeechResult(
                    text=None,
                    result=stt.SpeechResultState.ERROR,
                )

            if "err_no" in result and result["err_no"] != 0:
                _LOGGER.error(
                    "Error from Baidu API: %s - %s",
                    result.get("err_msg", "Unknown error"),
                    result.get("err_detail", "No details"),
                )
                return stt.SpeechResult(
                    text=None,
                    result=stt.SpeechResultState.ERROR,
                )

            if "result" not in result or not result["result"]:
                return stt.SpeechResult(
                    text=None,
                    result=stt.SpeechResultState.SUCCESS,
                )

            return stt.SpeechResult(
                text=result["result"][0],
                result=stt.SpeechResultState.SUCCESS,
            )

        except Exception:
            _LOGGER.exception("Error processing Baidu STT")
            return stt.SpeechResult(
                text=None,
                result=stt.SpeechResultState.ERROR,
            )
