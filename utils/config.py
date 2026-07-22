import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# OpenAI API Key
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError(
        "OpenAI API Key not found. Please add it to your .env file."
    )

# AI Models
WHISPER_MODEL = "whisper-1"
CHAT_MODEL = "gpt-4o-mini"

# Model Settings
TEMPERATURE = 0.3

# Temporary File Configuration
TEMP_FOLDER = "temp"
TEMP_AUDIO_FILE = os.path.join(
    TEMP_FOLDER,
    "temp_meeting_audio.wav"
)

TEMP_PDF_FILE = os.path.join(
    TEMP_FOLDER,
    "meeting_notes.pdf"
)

# Create temp folder if it doesn't exist
os.makedirs(TEMP_FOLDER, exist_ok=True)

# OpenAI Client
client = OpenAI(api_key=API_KEY)