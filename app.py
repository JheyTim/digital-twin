from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES
from dotenv import load_dotenv
import gradio as gr

# Load local .env settings before creating the client; they override existing values.
load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

# The client reads OPENAI_API_KEY from the environment.
openai = OpenAI()

# Keep the twin's identity and background at the start of every conversation.
system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


def chat(message, history):
    # Gradio supplies earlier messages; build a fresh list for this turn.
    messages = system + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    # A response can request tools instead of answering. Keep going until it answers.
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        # Include the assistant's tool requests before their matching results so
        # the next model call can use the outcome of each requested action.
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content


if __name__ == "__main__":
    # Start the web UI only when running this file directly (python app.py).
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Digital Twin",
        description="Talk to my AI twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())
