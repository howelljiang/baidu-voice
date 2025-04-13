"""百度语音集成."""
import logging
from typing import Any, Dict, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from aip import AipSpeech

from .const import (
    DOMAIN,
    CONF_APP_ID,
    CONF_API_KEY,
    CONF_SECRET_KEY,
    SERVICE_TTS,
    SERVICE_STT,
    ATTR_MESSAGE,
    ATTR_LANGUAGE,
    ATTR_VOLUME,
    ATTR_SPEED,
    ATTR_PITCH,
    ATTR_PERSON,
    ATTR_AUDIO,
    ATTR_FORMAT,
    ATTR_SAMPLE_RATE,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.deprecated(DOMAIN)

async def async_setup(hass: HomeAssistant, config: Dict[str, Any]) -> bool:
    """设置百度语音集成."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置百度语音配置项."""
    # 存储配置数据
    hass.data[DOMAIN] = {
        CONF_APP_ID: entry.data[CONF_APP_ID],
        CONF_API_KEY: entry.data[CONF_API_KEY],
        CONF_SECRET_KEY: entry.data[CONF_SECRET_KEY],
    }
    
    # 创建语音识别客户端
    client = AipSpeech(
        entry.data[CONF_APP_ID],
        entry.data[CONF_API_KEY],
        entry.data[CONF_SECRET_KEY],
    )
    
    # 加载TTS平台
    await async_load_platform(hass, "tts", DOMAIN, {}, entry.data)
    
    # 加载STT平台
    await async_load_platform(hass, "stt", DOMAIN, {}, entry.data)
    
    # 注册服务
    async def async_tts_service(service):
        """处理TTS服务调用."""
        message = service.data.get(ATTR_MESSAGE)
        language = service.data.get(ATTR_LANGUAGE, "zh")
        volume = service.data.get(ATTR_VOLUME, 5)
        speed = service.data.get(ATTR_SPEED, 5)
        pitch = service.data.get(ATTR_PITCH, 5)
        person = service.data.get(ATTR_PERSON, 0)
        
        try:
            result = await hass.async_add_executor_job(
                client.synthesis,
                message,
                language,
                1,  # 1表示mp3格式
                {
                    "vol": volume,
                    "per": person,
                    "spd": speed,
                    "pit": pitch,
                }
            )
            
            if isinstance(result, dict):
                _LOGGER.error("TTS失败: %s", result.get('err_msg'))
                return
            
            # 保存音频文件
            with open('tts_output.mp3', 'wb') as f:
                f.write(result)
                
            _LOGGER.info("TTS成功")
            
        except Exception as ex:
            _LOGGER.error("TTS异常: %s", ex)
    
    async def async_stt_service(service):
        """处理STT服务调用."""
        audio = service.data.get(ATTR_AUDIO)
        format = service.data.get(ATTR_FORMAT, "pcm")
        sample_rate = service.data.get(ATTR_SAMPLE_RATE, 16000)
        
        try:
            result = await hass.async_add_executor_job(
                client.asr,
                audio,
                format,
                sample_rate,
                {
                    "dev_pid": 1537,  # 普通话(支持简单的英文识别)
                }
            )
            
            if result.get("err_no") != 0:
                _LOGGER.error("STT失败: %s", result.get('err_msg'))
                return
            
            # 返回识别结果
            recognized_text = result.get("result", [""])[0]
            _LOGGER.info("STT识别结果: %s", recognized_text)
            
        except Exception as ex:
            _LOGGER.error("STT异常: %s", ex)
    
    # 注册服务
    hass.services.async_register(
        DOMAIN,
        SERVICE_TTS,
        async_tts_service,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_STT,
        async_stt_service,
    )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载百度语音配置项."""
    hass.services.async_remove(DOMAIN, SERVICE_TTS)
    hass.services.async_remove(DOMAIN, SERVICE_STT)
    hass.data.pop(DOMAIN)
    
    return True 