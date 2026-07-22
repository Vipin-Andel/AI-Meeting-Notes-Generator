from utils.config import (
    client,
    WHISPER_MODEL
)


def transcribe_audio(audio_path):
    """
    Transcribes an audio file using
    OpenAI Whisper and returns
    the transcript text.
    """

    with open(audio_path, "rb") as audio_file:

        response = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=audio_file
        )

    return response.text