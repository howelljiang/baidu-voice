# 百度语音服务集成

这是一个 Home Assistant 集成，用于接入百度语音服务，提供文本转语音(TTS)和语音转文本(STT)功能。

## 配置要求

1. 需要在百度云创建应用
2. 开通以下服务：
   - 短语音识别服务
   - 短文本在线合成服务

## 配置步骤

1. 在百度云控制台创建应用并获取 API Key 和 Secret Key
2. 在 Home Assistant 中添加 baidu_voice 集成
3. 输入您的 API Key 和 Secret Key

## 配置截图

![百度tts语音服务配置](baidu1.png)
![百度stt语音服务配置](baidu2.png)

## 注意事项

- 本集成需要互联网连接
- 使用百度语音服务可能会产生费用，请参考百度云官方计费标准
