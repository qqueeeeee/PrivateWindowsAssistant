
> **Note**: This project is a **proof of concept** to demonstrate how you can run your own local LLM assistant to perform useful tasks. Performance depends on your hardware.

# Windows Assistant 🤖

A powerful Windows assistant with a modern desktop interface that can help you open applications, take notes, and search through your documents using natural language.

## Features

- **🚀 Application Launcher**: Open any installed Windows application with simple commands
- **📝 Note Taking**: Save and manage notes in a persistent text file
- **📚 Document Search**: Search through PDF documents using AI-powered semantic search
- **💬 Natural Language Interface**: Chat naturally with the assistant
- **🎨 Modern Desktop UI**: Clean, native Windows interface built with tkinter
- **📊 Request Tracking**: Monitor your API usage and request statistics

## Prerequisites

1. **Ollama**: Make sure you have Ollama installed and running
   - Download from: https://ollama.ai/
   - Pull the required model: `ollama pull qwen3:4b`

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment** (optional):
   - Create a `.env` file if you want to use Groq instead of Ollama
   - Add your Groq API key: `GROQ_API_KEY=your_api_key_here`

4. **Prepare your documents** (optional):
   - Place any PDF files you want to search in the `data/College_PDFs/` directory
   - The system will automatically index them on first run

## Usage

### Running the Application

1. **Start the Windows Assistant**:
   ```bash
   python main.py
   ```

2. **The modern desktop application will open**

3. **Start chatting** with your assistant!

### Command Line Interface (Optional)

If you prefer the command line interface:

```bash
python main_cli.py
```

## Example Commands

- **Open Applications**: "Open Discord", "Open Chrome", "Open Notepad"
- **Take Notes**: "Save this note: Meeting tomorrow at 3 PM"
- **Search Documents**: "What is machine learning?", "Tell me about cloud computing"
- **General Chat**: Ask questions, have conversations, get help

## File Structure

```
Windows Assistant/
├── main.py                # Modern Windows desktop application (PRIMARY)
├── main_cli.py            # Command line interface (optional)
├── prompts.py             # Agent prompts and instructions
├── requirements.txt       # Python dependencies
├── engines/               # Core functionality
│   ├── app_engine.py      # Application launcher
│   ├── document_engine.py # PDF document search
│   └── note_engine.py     # Note taking system
├── data/                  # Data storage
│   ├── College_PDFs/      # PDF documents (add your PDFs here)
│   └── notes.txt          # Your saved notes
└── tracker/               # Request tracking
    ├── tracker.py         # Request tracker implementation
    └── tracker_data/      # Usage statistics
```

## Customization

### Adding More PDFs
- Simply drop PDF files into the `data/College_PDFs/` directory
- The system will automatically detect and index new files

### Changing the LLM
- Edit `main.py` or `main_cli.py` to use different models
- Uncomment the Groq configuration if you prefer cloud-based inference

### Modifying Prompts
- Edit `prompts.py` to customize how the assistant behaves
- Adjust the instructions for different use cases

## Troubleshooting

### Common Issues

1. **"Agent not initialized" / Response Very Slow**
   - The speed of the response depends on your GPU and the model you are running, by default it runs the model qwen3:4b from Ollama.
   - Make sure Ollama is running: `ollama serve`
   - Verify the model is installed: `ollama pull qwen3:4b`

2. **"Could not find app"**
   - The app name might not match exactly
   - Try variations like "discord" vs "Discord"

3. **Slow document search**
   - First-time indexing can take a while for large PDFs
   - Subsequent searches will be much faster

4. **Import errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Consider using a virtual environment


