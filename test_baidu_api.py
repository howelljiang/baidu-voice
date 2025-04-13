"""测试百度语音API."""
import asyncio
import logging
from aip import AipSpeech

# 配置日志
logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

# 百度API配置
APP_ID = "118461597"
API_KEY = "BZk7p3B0DurJuRLrN1cx9iHF"
SECRET_KEY = "sn0i6jtJNPcGI2V13P3MKiGCQYoz9xzf"

# 测试音频文件路径
TEST_AUDIO_PATH = "text2audio.pcm"  # 修正文件名

async def test_tts():
    """测试语音合成."""
    try:
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        
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
        
        # 保存音频文件
        with open('tts_test.mp3', 'wb') as f:
            f.write(result)
        
        _LOGGER.info("TTS测试成功")
        return True
        
    except Exception as ex:
        _LOGGER.error("TTS测试异常: %s", ex)
        return False

async def test_stt():
    """测试语音识别."""
    try:
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        
        # 读取测试音频
        with open(TEST_AUDIO_PATH, 'rb') as f:
            audio_data = f.read()
        
        # 测试STT
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
        
        # 验证识别结果
        recognized_text = result.get("result", [""])[0]
        _LOGGER.info("STT识别结果: %s", recognized_text)
        
        if not recognized_text or "测试" not in recognized_text:
            _LOGGER.error("STT识别结果不准确: %s", recognized_text)
            return False
        
        _LOGGER.info("STT测试成功")
        return True
        
    except Exception as ex:
        _LOGGER.error("STT测试异常: %s", ex)
        return False

async def main():
    """主测试函数."""
    _LOGGER.info("开始测试百度语音API...")
    
    # 测试TTS
    tts_result = await test_tts()
    _LOGGER.info("TTS测试结果: %s", "成功" if tts_result else "失败")
    
    # 等待1秒
    await asyncio.sleep(1)
    
    # 测试STT
    stt_result = await test_stt()
    _LOGGER.info("STT测试结果: %s", "成功" if stt_result else "失败")
    
    _LOGGER.info("测试完成")

if __name__ == "__main__":
    asyncio.run(main()) 