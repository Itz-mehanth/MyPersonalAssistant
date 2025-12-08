# Aura - AI Personal Assistant

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AI](https://img.shields.io/badge/AI-Powered-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Introduction

**Aura** is a powerful, voice-activated AI personal assistant designed to automate your daily tasks, control your system, and provide intelligent responses. Built with Python, Aura leverages advanced Machine Learning models (like Whisper for speech recognition and Hugging Face Transformers for intelligence) to understand and execute complex commands. 

Whether you need to manage your windows, study with a split-screen setup, send WhatsApp messages, or just have a chat, Aura is ready to help. It features a futuristic, reliable voice interface and a stunning visualizer.

## 🚀 Features

### 🎙️ Voice & Intelligence
- **Wake Word Detection**: Activates when you call its name ("Aura").
- **Speech Recognition**: Utilizes OpenAI's **Whisper** model for highly accurate speech-to-text.
- **Natural Language Understanding**: Powered by **Hugging Face Inference API** (supporting models like Llama-3, GPT-2, Qwen) to understand context and intent.
- **Text-to-Speech**: customizable voice responses using **ElevenLabs** or pyttsx3.

### 💻 System Control
- **Window Management**: Close specific windows, minimize distractions by closing all except one, or close everything.
- **Screen Analysis**: Analyze the content of open windows using OCR and LLM to answer questions about what's on your screen.
- **Function Automation**:
  - **Split Screen**: Automatically arranges windows for a "Study Mode".
  - **Volume & Brightness**: Control system settings with voice commands.
  - **File Access**: Search and open files instantly.

### 🌐 Web & Social
- **WhatsApp Automation**: Send messages, camera images, or screenshots to contacts automatically.
- **Web Search**: Play songs on Spotify, find videos on YouTube, or search the web.
- **ChatGPT Integration**: content generation and answering queries via ChatGPT automation.

### 🎨 Visual & UI
- **Interactive Visualizer**: A beautiful, sci-fi inspired spherical audio visualizer built with **Pygame** that reacts to voice activity.
- **Code Generation**: Can automate development workflows by generating code and creating projects in VS Code.

## 🛠️ Tech Stack

- **Core**: Python
- **AI/ML**: `openai-whisper`, `transformers`, `huggingface_hub`, `torch`
- **Audio**: `pyaudio`, `pyttsx3`, `speechrecognition`, `scipy`
- **Web Automation**: `selenium`, `requests`
- **GUI**: `pygame`, `tkinter` (via `mss` or `pyautogui`)
- **System**: `ctypes`, `os`, `sys`

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Itz-mehanth/Aura-AI-Agent.git
   cd Aura-Assistant
   ```

2. **Install Dependencies**
   Ensure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If requirements.txt is empty, install the key libraries manually:*
   ```bash
   pip install openai-whisper transformers torch pyaudio pygame speechrecognition pyttsx3 requests selenium mss pydub
   ```

3. **FFmpeg**
   Aura requires FFmpeg for audio processing. Download and add it to your system PATH.

## 🔑 Configuration

1. **API Keys**
   Create a file named `API_KEY.py` in the root directory (if not exists) and add your keys:
   ```python
   API_TOKEN = "your_hugging_face_api_token"
   ```
   *Note: For ElevenLabs voice, update the `API_KEY` variable in `voice_commands.py`.*

2. **WhatsApp Setup**
   Ensure you are logged into WhatsApp Web for automation features to work.

## 🏃 Usage

Run the main voice command script to start Aura:

```bash
python voice_commands.py
```

- **Say "Aura"** to wake it up.
- **Speak your command** (e.g., "Play some lofi music", "Open VS Code", "Send a message to John").

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or optimizations:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built with ❤️ by [Mehanth]*
