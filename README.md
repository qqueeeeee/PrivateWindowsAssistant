# PrivateWindowsAssistant

![MIT License](https://img.shields.io/github/license/qqueeeeee/PrivateWindowsAssistant)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Last Commit](https://img.shields.io/github/last-commit/qqueeeeee/PrivateWindowsAssistant)

**A modern, privacy-focused personal assistant for Windows—open apps, take notes, and search documents using natural language and local AI.**

> **Note:** This project is a **proof of concept** to demonstrate how a fully local AI-powered Windows assistant could work.  
> _Performance and capabilities depend on your device hardware and chosen LLM model._

Note: This project is a proof of concept to demonstrate how a fully local AI-powered Windows assistant could work. You can open apps, search documents, and take notes using natural language, all without sending data to the cloud.

Performance and capabilities depend on your device hardware and chosen LLM model. Future improvements could bring deeper integration, more features, and expanded platform support.

## Features

- **Application Launcher:** Open any installed Windows app using natural language.
- **Note Taking:** Save and manage notes easily, with persistent local storage.
- **Document Search:** Search through local PDF documents with AI-powered semantic search.
- **Natural Language Interface:** Simple, conversational chat with the assistant.

## Quick Start
```
git clone https://github.com/qqueeeeee/PrivateWindowsAssistant.git
cd PrivateWindowsAssistant
pip install -r requirements.txt
python main.py
```

---

## Backend Model Options

| Backend | How to Use |
|---------|------------|
| **Ollama** | Install and run Ollama, pull `qwen3:4b` model, run as is |
| **Groq**   | Set your `GROQ_API_KEY` in `.env`, edit `main.py`/`main_cli.py` for cloud inference |

---

## Example Commands

- **Open Apps:** `Open Discord`, `Open Notepad`
- **Notes:** `Save this note: Buy groceries tomorrow`
- **Search PDFs:** `Find all references to AI in my papers`
- **General Chat:** `What is machine learning?`, `Who is Alan Turing?`

---

## Customization

- **Add PDFs:** Drop your PDF files into `data/College_PDFs/`, they’ll be indexed automatically.
- **Switch Models:** Edit `main.py` or `main_cli.py` to change backend (Ollama, Groq, etc.).
- **Modify Prompts:** Customize assistant response style via `prompts.py`.
- **Track Usage:** Stats saved under `tracker/tracker_data/`.

---

## Troubleshooting

- **Agent Not Initialized / Slow Response:**  
  Make sure Ollama is running: `ollama serve`  
  Pull the correct model: `ollama pull qwen3:4b`
- **App Not Found:**  
  Try variations on app name: “discord” vs “Discord”
- **Import Errors:**  
  Install all dependencies: `pip install -r requirements.txt`
- **Slow PDF Search:**  
  Large files take longer the first time; future queries will be faster.

---

## License

Licensed under the [MIT License](LICENSE).

---



