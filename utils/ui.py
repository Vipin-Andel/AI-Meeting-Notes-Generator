import streamlit as st


def show_footer():
    """
    Displays the application footer.
    """

    st.markdown("---")

    st.success("🟢 Application Ready")

    st.caption(
        "Version 1.0 | Built with ❤️ using Streamlit • OpenAI • Whisper • Python"
    )