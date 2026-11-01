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

- Place your LinkedIn profile PDF at `linkedin.pdf` in the project root. Committing it is optional. To keep it out of your repository, add `linkedin.pdf` to `.gitignore` before staging files and supply it separately after cloning. If you commit it to a public repository, its contents will be public.
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

## Deploy to Render

### 1. Push the project to GitHub

Commit and push the application files, `requirements.txt`, and your updated `summary.txt` to a GitHub repository. These deployment steps assume `linkedin.pdf` is also committed at the project root. Keep `.env` excluded by `.gitignore` and configure credentials in Render.

### 2. Create a web service

In the Render dashboard, select **New > Web Service**, connect GitHub, and select your repository. Configure these settings:

| Setting | Value |
| --- | --- |
| Name | digital-twin |
| Language | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | python app.py |

Choose a region near you, then under **Compute**, select **Free ($0/month)**.

The start command assigns Render's `PORT` to Gradio. Together with `GRADIO_SERVER_NAME=0.0.0.0` in the next step, it configures the app to receive public requests.

### 3. Set environment variables

Add these in the **Environment Variables** section during creation, or on the service's **Environment** page:

| Key | Value |
| --- | --- |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `PUSHOVER_USER` | Your Pushover user key |
| `PUSHOVER_TOKEN` | Your Pushover application token |
| `GRADIO_SERVER_NAME` | `0.0.0.0` |
| `GRADIO_SERVER_PORT` | `10000` |


Once the settings are ready, click **Deploy web service**. Watch the deployment logs until the service is live.

### 4. Verify and link your portfolio

Open the service's `https://<your-service-name>.onrender.com` URL and ask a career question. Test a contact request with your own email and confirm the notification arrives in Pushover. Use the actual Render URL for your portfolio's **Live Demo** or **Talk to my AI Twin** link.

Free Render web services sleep after 15 minutes without inbound traffic and can take about a minute to wake up.

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
| `linkedin.pdf` | Required LinkedIn profile source; committing it to Git is optional. |
| `requirements.txt` | Python dependencies. |
| `.env` | Local credentials; ignored by Git. |
