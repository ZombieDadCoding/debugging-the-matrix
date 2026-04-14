import html
import json
import os
from datetime import datetime, timezone
from huggingface_hub import HfApi, hf_hub_download

from dotenv import load_dotenv
from openai import OpenAI
import requests
from pypdf import PdfReader
import gradio as gr


custom_head = """
<meta property="og:title" content="My Career Digital Twin - AI Agent representing Nikhil">
<meta property="og:description" content="Ask me anything about my skills, experience, projects, and career journey. Built in Udemy Agent & MCP course.">
<meta property="og:image" content="https://YOUR-IMAGE-URL-HERE.jpg">
<meta property="og:url" content="https://huggingface.co/spaces/ZombieDadCoding/career_conversation">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
"""

load_dotenv(override=True)

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_HF_SPACE_FILE = os.path.join(_SCRIPT_DIR, "all_questions.jsonl")
_HF_DATASET_FILE = "dataset_questions.jsonl"

_ui_screenshot_path = os.path.join(_SCRIPT_DIR, "me", "ui_screenshot.png")

def get_entry_count(file_path):
    if not os.path.exists(file_path):
        return 0
    with open(file_path, "r") as f:
        # Summing 1 for every line
        return sum(1 for _ in f)

def append_to_hf_dataset():
    api = HfApi(token=os.getenv("HF_API_KEY"))

    try:
        # We download to a temporary path to avoid overwriting your live local log
        remote_file_temp = hf_hub_download(
            repo_id=os.getenv("HF_DATASET_REPO"), 
            filename=_HF_DATASET_FILE, 
            repo_type="dataset",
            token=os.getenv("HF_API_KEY")
        )
    except Exception:
        # If no remote file exists yet, we just start with our local content
        remote_file_temp = None

    # 2. Open local file and read new content
    with open(_HF_SPACE_FILE, "r") as f:
        new_lines = f.readlines()

    # 3. Append to remote content (or create new)
    # Here, we create a new file that combines remote history + new local lines
    combined_file = "combined_logs.jsonl"
    with open(combined_file, "w") as out:
        if remote_file_temp:
            with open(remote_file_temp, "r") as remote:
                out.write(remote.read())
        out.writelines(new_lines)

    # 4. Push the combined file to the Hub
    api.upload_file(
        path_or_fileobj=combined_file,
        path_in_repo=_HF_DATASET_FILE,
        repo_id=os.getenv("HF_DATASET_REPO"),
        repo_type="dataset",
        commit_message="Sync local log to remote dataset"
    )

    push(f"Huggingface Dataset updated. Total questions: {get_entry_count(combined_file)}")
    
    if os.path.exists(_HF_SPACE_FILE):
        os.remove(_HF_SPACE_FILE)

def log_and_check(user_input, bot_response):
    # 1. Append the new entry
    record_question(user_input, bot_response)
    
    # 2. Check the count
    count = get_entry_count(_HF_SPACE_FILE)
    
    # 3. Trigger API if count is > 10
    if count >= 10:
        print(f"Log limit reached ({count}). Triggering external API...")
        append_to_hf_dataset()


def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

def record_user_details(linkedin_name, name="not provided", notes="not provided"):
    push(f"New contact: LinkedIn name {linkedin_name}. Preferred name: {name}. Notes: {notes}")
    return {"recorded": "ok"}


def record_question(question, answer):
    rec = {
        "question": question,
        "answer": answer,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(_HF_SPACE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided their LinkedIn profile name (the name shown on their LinkedIn)",
    "parameters": {
        "type": "object",
        "properties": {
            "linkedin_name": {
                "type": "string",
                "description": "The user's name as it appears on their LinkedIn profile (or the LinkedIn name they give you so you can find them)"
            },
            "name": {
                "type": "string",
                "description": "How they introduced themselves in chat, if different from their LinkedIn name or if you want to note a preferred name"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["linkedin_name"],
        "additionalProperties": False
    }
}


tools = [
    {"type": "function", "function": record_user_details_json}
]


class Me:

    def __init__(self):
        self.gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", \
            api_key=os.getenv("GOOGLE_API_KEY"))
        self.name = "Nikhil Shelke"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If the user wants to connect or is engaging in discussion, ask for their name on LinkedIn profile and record it. \
using your record_user_details tool."

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        user_message = message
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": user_message}]
        done = False
        while not done:
            response = self.gemini.chat.completions.create(model="gemini-2.5-flash-lite", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                assistant_message = response.choices[0].message
                tool_calls = assistant_message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(assistant_message.model_dump(exclude_none=True))
                messages.extend(results)
            else:
                done = True
        content = response.choices[0].message.content
        log_and_check(user_message, content)
        # Gradio ChatInterface expects a string; Gemini sometimes returns null content.
        if content is not None:
            return content
        return "Apologies. I couldn't produce a reply just then — please try again."


if __name__ == "__main__":
    me = Me()
    _avatar_path = os.path.join(_SCRIPT_DIR, "me", "avatar.png")
    _twin_theme = (
        gr.themes.Soft(
            primary_hue=gr.themes.colors.blue,
            secondary_hue=gr.themes.colors.slate,
            neutral_hue=gr.themes.colors.slate,
            radius_size=gr.themes.sizes.radius_sm,
            font=(
                gr.themes.GoogleFont("Source Sans 3"),
                "ui-sans-serif",
                "system-ui",
                "sans-serif",
            ),
        ).set(
            body_background_fill="transparent",
            body_background_fill_dark="transparent",
        )
    )
    _twin_css = """
html, body { min-height: 100%; }
body {
  background-color: #f1f5f9;
  background-image:
    radial-gradient(900px 520px at 12% -8%, rgba(37, 99, 235, 0.14), transparent 58%),
    radial-gradient(700px 420px at 92% 0%, rgba(51, 65, 85, 0.10), transparent 55%),
    linear-gradient(180deg, #f8fafc 0%, #eef2f7 55%, #e2e8f0 100%);
  background-attachment: fixed;
}
.gradio-container { background: transparent !important; }
footer { background: transparent !important; }
.twin-header-row {
  justify-content: center !important;
  align-items: center !important;
  gap: 1rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}
.twin-header-row .twin-header-text { text-align: center; max-width: 40rem; }
.twin-title-avatar img, .twin-title-avatar video {
  border-radius: 9999px !important;
  object-fit: cover !important;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.15);
}
"""
    _twin_chatbot = gr.Chatbot(
        type="messages",
        avatar_images=(None, _avatar_path),
        show_copy_button=True,
    )
    _twin_description = (
        "Ask about background, skills, and experience. This assistant is AI-powered and "
        "speaks in my voice; answers may be imperfect—for anything important, connect on LinkedIn."
    )
    _twin_examples = [
        "Introduce yourself or in about one minute.",
        "What kinds of roles or projects are you most excited about next?",
        "What does your day-to-day stack look like?",
        "What's the best way to follow up after this conversation?",
    ]
    with gr.Blocks(
        theme=_twin_theme,
        css=_twin_css,
        title=f"Chat with {me.name}",
        head=custom_head
    ) as _twin_demo:
        with gr.Row(equal_height=True, elem_classes=["twin-header-row"]):
            gr.Image(
                value=_avatar_path,
                width=80,
                height=80,
                interactive=False,
                show_label=False,
                show_download_button=False,
                show_share_button=False,
                container=False,
                elem_classes=["twin-title-avatar"],
            )
            with gr.Column(scale=1, min_width=0, elem_classes=["twin-header-text"]):
                gr.Markdown(f"## Chat with {html.escape(me.name)}", container=False)
                gr.Markdown(_twin_description, container=False)

        gr.ChatInterface(
            me.chat,
            type="messages",
            chatbot=_twin_chatbot,
            title=None,
            description=None,
            examples=_twin_examples,
            theme=_twin_theme,
            css=None,
            flagging_mode="never",
            fill_height=True,
        )

    _twin_demo.launch()
