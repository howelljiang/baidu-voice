"""百度语音常量."""
from typing import Final

DOMAIN: Final = "baidu_voice"

# 配置项
CONF_APP_ID: Final = "app_id"
CONF_API_KEY: Final = "api_key"
CONF_SECRET_KEY: Final = "secret_key"

# 服务
SERVICE_TTS: Final = "tts"
SERVICE_STT: Final = "stt"

# 服务属性
ATTR_MESSAGE: Final = "message"
ATTR_LANGUAGE: Final = "language"
ATTR_VOLUME: Final = "volume"
ATTR_SPEED: Final = "speed"
ATTR_PITCH: Final = "pitch"
ATTR_PERSON: Final = "person"
ATTR_AUDIO: Final = "audio"
ATTR_FORMAT: Final = "format"
ATTR_SAMPLE_RATE: Final = "sample_rate"

# 语音参数
DEFAULT_SPEED: Final = 5
DEFAULT_PITCH: Final = 5
DEFAULT_VOLUME: Final = 5
DEFAULT_PERSON: Final = 0  # 0: 女声, 1: 男声, 3: 情感男声, 4: 情感女声

# 音频格式
SUPPORTED_AUDIO_FORMATS: Final = ["mp3", "wav", "pcm"]
SUPPORTED_SAMPLE_RATES: Final = [8000, 16000]
SUPPORTED_CHANNELS: Final = [1]  # 单声道
SUPPORTED_CODECS: Final = ["pcm", "mp3", "wav"]

# 语言支持
SUPPORTED_LANGUAGES: Final = ["zh"]  # 目前只支持中文

# 错误码
ERROR_INVALID_AUTH: Final = "invalid_auth"
ERROR_UNKNOWN: Final = "unknown"
ERROR_NOT_SUPPORTED: Final = "not_supported"
ERROR_SERVICE_UNAVAILABLE: Final = "service_unavailable" 