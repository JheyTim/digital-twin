# Digital Twin

A Python chatbot that represents your professional background, skills, and experience through a customized Gradio interface. It uses OpenAI with context from a LinkedIn profile PDF and a personal summary, and sends contact requests and unanswered questions to Pushover.

## Features

- Career-focused conversations grounded in your profile and summary.
- Conversation history included in follow-up responses.
- Tools for sending visitor contact details and unanswered questions as notifications.
- Custom interface styling and starter questions.

## Requirements

- Python 3 with `pip` and `venv` support, compatible with the packages in `requirements.txt`.
- An OpenAI API key with access to the model configured in `app.py` (currently `gpt-5.4-mini`).
- A Pushover user key and application token for notifications.
- A LinkedIn profile PDF with extractable text and a UTF-8 personal summary.

Dependencies are listed without version pins in `requirements.txt`: `openai`, `gradio`, `pypdf`, `python-dotenv`, and `requests`.

## Setup

Run the following commands from the project directory.

### 1. Create a virtual environment and install dependencies

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

These commands use the environment's Python directly, so activation is not required.

### 2. Configure credentials

Create or update `.env` in the project root with your credentials:

```dotenv
OPENAI_API_KEY=your_openai_api_key
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_application_token
```

The app loads `.env` with `override=True`, so these values take precedence over existing environment variables. The file is ignored by Git.

### 3. Add your profile

- Place your LinkedIn profile PDF at `linkedin.pdf` in the project root. This file is ignored by Git and must be supplied separately after cloning.
- Edit `summary.txt` with the background, experience, skills, and professional details you want the twin to use. This file is tracked by Git.

Both files are required at startup. PDF pages without extractable text are skipped; the app does not perform OCR. Restart the app after changing either file because the context is loaded at import time.

### 4. Start the app

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe app.py
```

macOS / Linux:

```bash
.venv/bin/python app.py
```

Open the local URL printed by Gradio in your browser. Keep the terminal running while using the app, and press `Ctrl+C` to stop it. Launch from the project root so the relative profile paths resolve correctly.

## Usage

Try a starter question such as “Tell me about your background and experience” or “What are your strongest technical skills?”

The system prompt instructs the twin to stay on professional topics, identify itself as AI when asked, and acknowledge gaps in its knowledge. When a visitor provides an email for follow-up, the model can call `record_user_details`. For questions it cannot answer, it is instructed to call `record_unknown_question`.

Both tools send Pushover notifications. They do not write a local contact list or question log. The current implementation does not check the Pushover response, so a tool result of `OK` does not confirm delivery.

## How it works

1. `context.py` extracts text from `linkedin.pdf`, reads `summary.txt`, and builds the system prompt.
2. `app.py` sends the prompt, conversation history, current message, and tool definitions to OpenAI Chat Completions.
3. If the model requests a tool, `tools.py` executes it and returns its result to the conversation.
4. The app continues requesting completions until the model supplies an answer, which Gradio displays.

The profile context and conversation messages are sent to OpenAI. Contact details and unanswered questions selected for tool calls are sent to Pushover.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Model configuration, chat loop, and Gradio entry point. |
| `context.py` | Profile loading and system instructions. |
| `tools.py` | Tool schemas, dispatch, and Pushover notifications. |
| `styles.py` | CSS, JavaScript, and starter prompts. |
| `summary.txt` | Personal background included in the prompt. |
| `linkedin.pdf` | Local LinkedIn profile source; ignored by Git. |
| `requirements.txt` | Python dependencies. |
| `.env` | Local credentials; ignored by Git. |

## Customization

- Change `MODEL_NAME` in `app.py` to select a model available to your API account that supports the tool calls used here.
- Edit `TWIN_SYSTEM_PROMPT` in `context.py` to change the twin's instructions.
- Update `CSS`, `JS`, and `EXAMPLES` in `styles.py` to adjust appearance and starter prompts.
- Update functions, schemas, and `tool_map` together in `tools.py` when changing tools.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Missing profile file at startup | Supply both `linkedin.pdf` and `summary.txt`, and run from the project root. |
| Missing API key or authentication error | Set `OPENAI_API_KEY` in `.env` and restart the app. |
| Model access error | Check access to the model specified by `MODEL_NAME` in `app.py`. |
| Profile changes do not appear | Restart the app to reload the source files. |
| PDF details are missing | Confirm the PDF contains selectable text; image-only pages need OCR before use. |
| Notifications do not arrive | Check both Pushover credentials and connectivity. Tool success does not verify delivery. |
| Interface changes after reinstalling packages | Dependencies are unpinned, and custom styling may need updates for a different Gradio version. |
