import streamlit as st


def show_error(error):
    """
    Displays application errors
    in a consistent format.
    """

    error_message = str(error)

    if "insufficient_quota" in error_message:

        st.error(
            """
❌ OpenAI API quota exceeded.

Please check your billing or enable Developer Mode.
"""
        )

    elif "API Key" in error_message:

        st.error(
            """
❌ OpenAI API Key not found.

Please verify your .env file.
"""
        )

    else:

        st.error(
            f"""
❌ An unexpected error occurred.

Error Details:
{error_message}
"""
        )