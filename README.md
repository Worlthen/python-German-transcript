# 德语字幕生成器

基于 Whisper + Ollama 的智能德语字幕生成工具，支持本地化处理，保护隐私安全。

## 功能特点

- 🎬 支持多种视频格式（MP4, WebM, AVI, MOV, MKV）
- 🎤 使用 OpenAI Whisper 进行高精度语音识别
- 🌍 使用 Ollama 本地大语言模型进行翻译
- ✏️ 可视化字幕编辑器
- 📄 支持导出 SRT、VTT、JSON 格式
- 🔒 完全本地化处理，保护隐私

## 环境要求

### 1. Whisper 服务

安装 OpenAI Whisper：
```bash
pip install -U openai-whisper
```

启动 Whisper API 服务（需要安装 whisper-api）：
```bash
pip install whisper-api
whisper-api --host 0.0.0.0 --port 9000
```

或者使用 Docker：
```bash
docker run -d -p 9000:9000 onerahmet/openai-whisper-asr-webservice:latest
```

### 2. Ollama 服务

下载并安装 Ollama：
- 访问 [https://ollama.ai](https://ollama.ai) 下载安装包
- 安装完成后，下载推荐的模型：

```bash
# 下载推荐模型（选择其中一个）
ollama pull llama3.2
ollama pull qwen2.5
ollama pull gemma2
```

启动 Ollama 服务：
```bash
ollama serve
```

## 使用方法

1. **启动服务**
   - 确保 Whisper 服务运行在 `http://localhost:9000`
   - 确保 Ollama 服务运行在 `http://localhost:11434`

2. **打开应用**
   - 在浏览器中打开 `german-subtitle-generator.html`

3. **上传视频**
   - 拖拽视频文件到上传区域，或点击选择文件
   - 支持最大 500MB 的视频文件

4. **配置设置**
   - 选择源语言（支持自动检测）
   - 选择 Ollama 模型
   - 调整服务地址（如果不是默认地址）
   - 设置最大处理时长

5. **生成字幕**
   - 点击"开始生成字幕"按钮
   - 等待处理完成（进度条会显示当前状态）

6. **编辑和导出**
   - 在字幕编辑器中修改字幕内容
   - 选择导出格式（SRT、VTT、JSON）

## 技术架构

```
视频文件 → 音频提取 → Whisper语音识别 → Ollama翻译 → 字幕生成
```

### 处理流程

1. **音频提取**：使用 Web Audio API 从视频中提取音频
2. **语音识别**：调用 Whisper API 进行语音转文字
3. **文本翻译**：使用 Ollama 本地模型翻译成德语
4. **字幕生成**：格式化为标准字幕格式

## 故障排除

### 常见问题

1. **Whisper 服务连接失败**
   - 检查 Whisper 服务是否正在运行
   - 确认端口 9000 没有被占用
   - 尝试重启 Whisper 服务

2. **Ollama 翻译失败**
   - 检查 Ollama 服务状态：`ollama list`
   - 确认已下载所选模型
   - 检查网络连接和防火墙设置

3. **视频处理失败**
   - 确认视频格式受支持
   - 检查视频文件是否损坏
   - 尝试转换为 MP4 格式

4. **音频质量问题**
   - 使用清晰音质的视频文件
   - 避免背景噪音过大的视频
   - 确保语音清晰可辨

### 性能优化

- **GPU 加速**：如有 NVIDIA 显卡，安装 CUDA 版本的 Whisper 以提升处理速度
- **模型选择**：较小的模型处理速度更快，但精度可能略低
- **批量处理**：应用已支持批量翻译，可提高效率

## 开发说明

### 文件结构
```
自动字幕/
├── german-subtitle-generator.html  # 主应用文件
├── README.md                      # 说明文档
└── examples/                      # 示例文件（可选）
```

### 自定义配置

可以修改 HTML 文件中的默认配置：
- Whisper 服务地址
- Ollama 服务地址
- 支持的视频格式
- 最大文件大小限制
- 处理时长限制

## 许可证

本项目基于开源技术构建，仅供学习和个人使用。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具！

---

**注意**：首次使用时，Whisper 和 Ollama 可能需要下载模型文件，请确保网络连接稳定。