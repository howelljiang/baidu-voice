"""百度语音配置流程."""
import logging
import os
import asyncio
import voluptuous as vol
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv
from aip import AipSpeech

from .const import (
    DOMAIN,
    CONF_APP_ID,
    CONF_API_KEY,
    CONF_SECRET_KEY,
)

_LOGGER = logging.getLogger(__name__)

# 测试音频文件路径
TEST_AUDIO_PATH = os.path.join(os.path.dirname(__file__), "text2audio.pcm")

async def async_read_file(file_path: str) -> bytes:
    """异步读取文件内容."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: open(file_path, "rb").read())

async def async_validate_api(
    app_id: str,
    api_key: str,
    secret_key: str,
) -> bool:
    """验证百度API配置."""
    try:
        # 创建语音识别客户端
        client = AipSpeech(app_id, api_key, secret_key)
        
        # 测试TTS
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            client.synthesis,
            "测试语音合成",
            "zh",
            1,  # 1表示mp3格式
            {
                "vol": 5,  # 音量，取值0-15，默认为5中音量
                "per": 0,  # 发音人选择，0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫
                "spd": 5,  # 语速，取值0-9，默认为5中语速
                "pit": 5,  # 音调，取值0-9，默认为5中语调
            }
        )
        
        if isinstance(result, dict):
            _LOGGER.error("TTS测试失败: %s", result.get('err_msg'))
            return False
            
        # 测试STT
        try:
            audio_data = await async_read_file(TEST_AUDIO_PATH)
        except Exception as ex:
            _LOGGER.error("无法读取测试音频文件: %s", ex)
            return False
            
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            client.asr,
            audio_data,
            "pcm",  # PCM格式
            16000,  # 采样率
            {
                "dev_pid": 1537,  # 普通话(支持简单的英文识别)
            }
        )
        
        if result.get("err_no") != 0:
            _LOGGER.error("STT测试失败: %s", result.get('err_msg'))
            return False
            
        return True
        
    except Exception as ex:
        _LOGGER.error("API验证异常: %s", ex)
        return False

class BaiduVoiceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理百度语音配置流程."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_PUSH

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """处理用户初始步骤."""
        errors: Dict[str, str] = {}
        
        if user_input is not None:
            # 验证API配置
            if await async_validate_api(
                user_input[CONF_APP_ID],
                user_input[CONF_API_KEY],
                user_input[CONF_SECRET_KEY],
            ):
                return self.async_create_entry(
                    title="百度语音",
                    data=user_input,
                )
            errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_APP_ID): str,
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_SECRET_KEY): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """创建选项流."""
        return BaiduVoiceOptionsFlow(config_entry)

class BaiduVoiceOptionsFlow(config_entries.OptionsFlow):
    """处理百度语音选项."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """初始化选项流."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """管理百度语音选项."""
        errors: Dict[str, str] = {}
        
        if user_input is not None:
            # 验证API配置
            if await async_validate_api(
                user_input[CONF_APP_ID],
                user_input[CONF_API_KEY],
                user_input[CONF_SECRET_KEY],
            ):
                return self.async_create_entry(
                    title="",
                    data=user_input,
                )
            errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_APP_ID,
                        default=self._config_entry.data.get(CONF_APP_ID),
                    ): str,
                    vol.Required(
                        CONF_API_KEY,
                        default=self._config_entry.data.get(CONF_API_KEY),
                    ): str,
                    vol.Required(
                        CONF_SECRET_KEY,
                        default=self._config_entry.data.get(CONF_SECRET_KEY),
                    ): str,
                }
            ),
            errors=errors,
        ) 