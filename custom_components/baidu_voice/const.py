"""百度语音常量定义."""

from typing import Final

DOMAIN: Final = "baidu_voice"
ENDPOINT: Final = "http://vop.baidu.com/server_api"
# 配置项
CONF_APP_ID: Final = "app_id"
CONF_API_KEY: Final = "api_key"
CONF_SECRET_KEY: Final = "secret_key"

# 通用选项
TTS_CONF_LANGUAGE: Final = "language"
TTS_CONF_VOICE: Final = "voice"
TTS_CONF_VOLUME: Final = "volume"
TTS_CONF_SPEED: Final = "speed"
TTS_CONF_PITCH: Final = "pitch"
TTS_CONF_FILEFORMAT: Final = "fileformat"

# TTS语言选项
TTS_LANGUAGES: Final = {"zh": "简体中文", "en": "English"}
TTS_DEFAULT_LANGUAGE: Final = "zh"

# TTS格式映射
TTS_FILEFORMAT_MAP: Final = {
    3: "mp3",  # mp3-16k/24k
    4: "pcm",  # pcm-16k/24k
    5: "pcm8k",  # pcm-8k
    6: "wav",  # wav(同pcm-16k/24k)
}

# 定义支持的语音选项
TTS_SUPPORTED_VOICES = {
    0: "度小美-标准女主播",
    1: "度小宇-亲切男声",
    3: "度逍遥-情感男声",
    4: "度丫丫-童声",
    5: "度小娇-成熟女主播",
    5003: "度逍遥-情感男声",
    5118: "度小鹿-甜美女声",
    106: "度博文-专业男主播",
    103: "度米朵-可爱童声",
    110: "度小童-童声主播",
    111: "度小萌-软萌妹子",
    4003: "度逍遥-情感男声",
    4106: "度博文-专业男主播",
    4115: "度小贤-电台男主播",
    5147: "度常盈-电台女主播",
    5976: "度小皮-萌娃童声",
    5971: "度皮特-老外男声",
    4164: "度阿肯-主播男声",
    4176: "度有为-磁性男声",
    4259: "度小新-播音女声",
    4119: "度小鹿-甜美女声",
    4105: "度灵儿-清激女声",
    4117: "度小乔-活泼女声",
    4288: "度晴岚-甜美女声",
    4192: "度青川-温柔男声",
    4100: "度小雯-活力女主播",
    4103: "度米朵-可爱女声",
    4144: "度姗姗-娱乐女声",
    4278: "度小贝-知识女主播",
    4143: "度清风-配音男声",
    4140: "度小新-专业女主播",
    4129: "度小彦-知识男主播",
    4149: "度星河-广告男声",
    4254: "度小清-广告女声",
    4206: "度博文-综艺男声",
    4147: "度云朵-可爱童声",
    4141: "度婉婉-甜美女声",
    4226: "南方-电台女主播",
    6205: "度悠然-旁白男声",
    6221: "度云萱-旁白女声",
    6546: "度清豪-逍遥侠客",
    6602: "度清柔-温柔男神",
    6562: "度雨楠-元气少女",
    6543: "度雨萌-邻家女孩",
    6747: "度书古-情感男声",
    6748: "度书严-沉稳男声",
    6746: "度书道-沉稳男声",
    6644: "度书宁-亲和女声",
    4148: "度小夏-甜美女声",
    4277: "西贝-脱口秀女声",
    4114: "阿龙-说书男声",
    4179: "度泽言-温暖男声",
    4146: "度禧禧-阳光女声",
    6567: "度小柔-温柔女声",
    4156: "度言浩-年轻男声",
    4189: "度涵竹-开朗女声",
    4194: "度嫣然-活泼女声",
    4193: "度泽言-开朗男声",
    4195: "度怀安-磁性男声",
    4196: "度清影-甜美女声",
    4197: "度沁遥-知性女声",
    20100: "度小粤-粤语女声",
    20101: "度晓芸-粤语女声",
    4257: "四川小哥-四川男声",
    4132: "度阿闽-闽南男声",
    4139: "度小蓉-四川女声",
    5977: "台媒女声-台湾女声",
    4007: "度小台-台湾女声",
    4150: "度湘玉-陕西女声",
    4134: "度阿锦-东北女声",
    4172: "度筱林-天津女声",
    5980: "度阿花-上海女声",
    4154: "度老崔-北京男声",
}

# 默认值
TTS_DEFAULT_VOLUME: Final = 5
TTS_DEFAULT_SPEED: Final = 5
TTS_DEFAULT_PITCH: Final = 5
TTS_DEFAULT_VOICE: Final = 0
TTS_DEFAULT_FILEFORMAT: Final = 3  # 默认音频格式 MP3

# 范围限制
TTS_VOLUME_RANGE: Final = (0, 15)
TTS_SPEED_RANGE: Final = (0, 9)
TTS_PITCH_RANGE: Final = (0, 9)

# 语言选项
STT_LANGUAGES: Final = {
    "zh-CN": "普通话",
    "en-US": "英语",
    "zh-HK": "粤语",
    "zh-TW": "四川话",
}
STT_LANGUAGES_CODE_MAP: Final = {
    "zh-CN": 1537,
    "en-US": 1737,
    "zh-HK": 1637,
    "zh-TW": 1837,
}
# STT配置项
STT_CONF_LANGUAGE: Final = "stt_language"

# STT语言选项
STT_DEFAULT_LANGUAGE: Final = "zh-CN"  # 默认使用普通话

# 错误码
ERROR_INVALID_AUTH: Final = "invalid_auth"
