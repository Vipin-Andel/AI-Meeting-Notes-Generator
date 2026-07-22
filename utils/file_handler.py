import os

from utils.config import TEMP_FOLDER


def save_audio(audio_bytes, file_path):
    """
    Saves audio data to the specified file path.
    """

    if audio_bytes is None:
        return

    with open(file_path, "wb") as file:
        file.write(audio_bytes)


def delete_file(file_path):
    """
    Deletes a file if it exists.
    """

    if file_path and os.path.exists(file_path):
        os.remove(file_path)


def get_temp_audio_path(filename):
    """
    Returns a temporary file path while
    preserving the original file extension.
    """

    _, extension = os.path.splitext(filename)

    return os.path.join(
        TEMP_FOLDER,
        f"temp_meeting_audio{extension}"
    )