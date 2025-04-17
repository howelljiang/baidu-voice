"""Integration for Baidu Voice services."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["stt", "tts"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """设置百度语音集成."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置百度语音配置项."""
    # 存储配置数据
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN] = entry.data.copy()  # 保存所有配置数据

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
