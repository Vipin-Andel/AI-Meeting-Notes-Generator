import re


def calculate_statistics(transcript):
    """
    Calculates transcript statistics
    and meeting quality metrics.
    """

    words = transcript.split()

    lines = transcript.split("\n")

    # Sentence detection
    sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", transcript)
        if sentence.strip()
    ]

    # Average words per sentence
    if sentences:

        average_words = round(
            len(words) / len(sentences),
            1
        )

    else:

        average_words = 0

    # Longest sentence
    if sentences:

        longest_sentence = max(
            len(sentence.split())
            for sentence in sentences
        )

    else:

        longest_sentence = 0

    # Vocabulary richness
    unique_words = set(
        word.lower()
        for word in words
    )

    if words:

        vocabulary = round(
            len(unique_words) / len(words) * 100,
            1
        )

    else:

        vocabulary = 0

    statistics = {

        "Word Count": len(words),

        "Character Count": len(transcript),

        "Line Count": len(lines),

        "Reading Time": max(
            1,
            round(len(words) / 200)
        ),

        "Sentence Count": len(sentences),

        "Average Words": average_words,

        "Longest Sentence": longest_sentence,

        "Vocabulary": vocabulary
    }

    return statistics