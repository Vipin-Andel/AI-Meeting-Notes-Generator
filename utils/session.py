import streamlit as st


def initialize_session():
    """
    Initializes all required Streamlit
    session state variables.
    """

    defaults = {
        "transcript": "",
        "meeting_notes": "",
        "meeting_insights": "",
        "meeting_analytics": {},
        "audio_bytes": None,
        "developer_mode": False
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value