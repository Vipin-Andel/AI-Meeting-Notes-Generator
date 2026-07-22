from utils.config import (
    client,
    CHAT_MODEL,
    TEMPERATURE
)

from utils.prompts import build_prompt


def summarize_meeting(
    transcript,
    meeting_title,
    meeting_date,
    language,
    summary_type
):
    """
    Generates structured AI meeting notes
    from the provided transcript.
    """

    system_prompt = build_prompt(
        meeting_title,
        meeting_date,
        language,
        summary_type
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    )

    return response.choices[0].message.content