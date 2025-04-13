"""百度语音集成."""
import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from aip import AipSpeech

from .const import (
    DOMAIN,
    CONF_APP_ID,
    CONF_API_KEY,
    CONF_SECRET_KEY,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.deprecated(DOMAIN)

PLATFORMS = ["tts", "stt"]

async def async_setup(hass: HomeAssistant, config: Dict[str, Any]) -> bool:
    """设置百度语音集成."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置百度语音配置项."""
    # 存储配置数据
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN] = {
        CONF_APP_ID: entry.data[CONF_APP_ID],
        CONF_API_KEY: entry.data[CONF_API_KEY],
        CONF_SECRET_KEY: entry.data[CONF_SECRET_KEY],
    }
    
    # 加载平台
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载百度语音配置项."""
    # 卸载平台
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data.pop(DOMAIN)
    
    return unload_ok 