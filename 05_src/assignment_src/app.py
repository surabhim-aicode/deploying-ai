from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI
import os
import sys

from services.api_service import ApiService
from services.semantic_service import SemanticService
from services.tool_service import ToolService
from memory.memory_manager import MemoryManager

sys.path.append('../../05_src/')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, "../.secrets")
load_dotenv('../.secrets')
API_GATEWAY_KEY = os.getenv("API_GATEWAY_KEY")


client = OpenAI(base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1', 
                api_key='any value',
                default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')})

api_service = ApiService()
semantic_service = SemanticService()
tool_service = ToolService()
memory = MemoryManager()

THREAD_ID = "user-session-1"

SYSTEM_PROMPT = """
You are a smart  AI assistant.
You help users using tools when needed.
Keep responses friendly and helpful.
"""



def chat(user_input, history):

    guard = check_guardrails(user_input)
    if guard:
        return guard

    # -----------------------------
    # Store + retrieve memory
    # -----------------------------
    memory.invoke(user_input, THREAD_ID)

    messages = memory.get_messages(THREAD_ID)

    # Add system prompt
    full_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + messages

    # -----------------------------
    # SERVICE ROUTING
    # -----------------------------
    if "weather" in user_input:
        words = user_input.split()
        city = words[-1]  

        reply = api_service.get_weather(city)
        

    elif "internal" in user_input or "custom" in user_input:
        reply = semantic_service.query(user_input)

    else:
        reply = tool_service.handle(full_messages)

    # -----------------------------
    # Save assistant response
    # -----------------------------
    memory.invoke(reply, THREAD_ID)

    return reply

RESTRICTED_TOPICS = ["cats", "dogs", "horoscope", "zodiac", "taylor swift"]

def check_guardrails(user_input):
    lower = user_input.lower()

    if any(topic in lower for topic in RESTRICTED_TOPICS):
        return "Sorry, I can't discuss that topic."

    if "system prompt" in lower or "reveal prompt" in lower:
        return "I’m not allowed to share system-level instructions."

    return None

def respond(message, history):

    reply = chat(message, history)

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply}
    ]

    return "", history


with gr.Blocks() as demo:
    gr.Markdown("#  Welcome to Surabhi-AI Assistant Magic🪄 Chat 💬 ")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask me anything...")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()