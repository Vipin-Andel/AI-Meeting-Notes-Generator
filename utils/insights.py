from utils.config import (
    client,
    CHAT_MODEL,
    TEMPERATURE
)


def generate_insights(transcript):
    """
    Generates AI-powered meeting insights.
    Returns the raw AI response.
    """

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": """
You are an AI Meeting Analyst.

Analyze the meeting transcript and provide:

Meeting Sentiment:
Meeting Priority:
Meeting Category:
Estimated Duration:

Return ONLY in this exact format.

Meeting Sentiment: Positive
Meeting Priority: High
Meeting Category: Sales
Estimated Duration: 30 Minutes
"""
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    )

    return response.choices[0].message.content


def parse_insights(insights_text):
    """
    Converts AI insights text into a dictionary.
    """

    insights = {}

    for line in insights_text.split("\n"):

        if ":" in line:

            key, value = line.split(":", 1)

            insights[key.strip()] = value.strip()

    return insights