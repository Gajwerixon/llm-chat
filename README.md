# My LLM Chat
A local ChatGPT-like application built with Python, Gradio and a local LLM.

## Requirements
* Python
* Ollama
* A local LLM model, for example `gemma3:4b`

## Run the project

### 1. Start Ollama
Make sure Ollama is installed and running on your computer.

Pull the model:

```bash
ollama pull gemma3:4b
```

You can check that the model is available with:

```bash
ollama list
```

You should see `gemma3:4b` in the list.

### 2. Activate the Python virtual environment

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Gradio will start the local web interface. Open the address shown in the terminal.

## Project Roadmap
* [x] **1. Demo** — Gradio chat interface with a bot returning random messages.
* [x] **2. App** — Connect the Gradio chat interface to Ollama.
* [ ] **3. Streaming model answers** — Display the local LLM response token by token as it is generated.
* [ ] **4. Save one conversation history** — Store and restore a single conversation.
* [ ] **5. Multiple conversations** — Add the ability to create and switch between conversations.
* [ ] **6. System prompt** — Add and manage the model's system prompt.
* [ ] **7. Conversation management** — Clear, rename and delete conversations.

## Project Goal
The goal of this project is to understand how a ChatGPT-like application works under the hood:

```text
User
  ↓
Gradio GUI
  ↓
Python application
  ↓
Ollama API
  ↓
Local LLM
  ↓
Python application
  ↓
Gradio GUI
```

The project is built as a learning exercise, with a focus on understanding the communication between the GUI, Python backend, Ollama and the local language model.