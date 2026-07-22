import streamlit as st
from streamlit_mic_recorder import mic_recorder
from PIL import Image

from utils.config import (
    TEMP_AUDIO_FILE,
    TEMP_PDF_FILE
)
from utils.transcription import transcribe_audio
from utils.sample_data import (
    SAMPLE_TRANSCRIPT,
    SAMPLE_MEETING_NOTES,
    SAMPLE_INSIGHTS
)
from utils.summarizer import summarize_meeting
from utils.file_handler import (
    save_audio,
    delete_file,
    get_temp_audio_path
)
from utils.session import initialize_session
from utils.error_handler import show_error
from utils.pdf_export import create_pdf
from utils.insights import (
    generate_insights,
    parse_insights
)
from utils.analytics import calculate_statistics
from utils.ui import show_footer

# Application icon
icon = Image.open("assets/icons8-microphone-50.png")


# Configure Streamlit page
st.set_page_config(
    page_title="AI Meeting Notes Generator",
    page_icon=icon,
    layout="wide"
)

# Sidebar settings
with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown("---")

    st.subheader("Meeting Language")

    language = st.selectbox(
        "Choose Language",
        [
            "English",
            "Hindi",
            "Spanish"
        ]
    )

    st.markdown("---")

    st.subheader("Summary Type")

    summary_type = st.selectbox(
        "Choose Summary Style",
        [
            "Detailed",
            "Short",
            "Bullet Points"
        ]
    )

    st.markdown("---")

    developer_mode = st.checkbox(
        "🛠 Developer Mode",
        value=st.session_state.get(
            "developer_mode",
            False
        ),
        help="Run the application without OpenAI API using sample meeting data."
    )
    st.session_state.developer_mode = developer_mode

# Main application header
st.title("🎙️ AI Meeting Notes Generator")

if st.session_state.developer_mode:

    st.info(
        "🛠 Developer Mode is enabled. Sample meeting data is being used instead of OpenAI APIs."
    )

st.caption(
    "Transform meeting audio into structured transcripts, AI-powered summaries, actionable insights, and analytics."
)

st.markdown(
    """
Upload or record your meeting audio to automatically generate:

- 🎤 Accurate Speech-to-Text Transcript
- 📝 AI Meeting Notes
- 💡 AI Insights
- 📊 Meeting Analytics
- 📄 Export to PDF, TXT & Markdown
"""
)

# Meeting information
meeting_title = st.text_input(
    "Meeting Title",
    placeholder="e.g. Weekly Sales Review"
)

meeting_date = str(
    st.date_input(
        "Meeting Date"
    )
)

# Initialize session state
initialize_session()
temp_filename = TEMP_AUDIO_FILE

# Main application layout
layout_col1, layout_col2 = st.columns([1, 2])

# Left panel - Audio capture
with layout_col1:

    st.header("1. Capture Audio")

    st.write(
        "Click the button below to start recording your meeting audio. "
        "When you're finished, click it again to stop recording."
    )

    audio_data = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop and Process",
        key="recorder"
    )

    st.divider()

    st.write("### OR")

    uploaded_file = st.file_uploader(
        "Upload an audio recording",
        type=["wav", "mp3", "m4a"]
    )

    if uploaded_file:

        temp_filename = get_temp_audio_path(uploaded_file.name)

        st.session_state.audio_bytes = uploaded_file.read()

        st.success("Audio uploaded successfully!")

        st.audio(st.session_state.audio_bytes)

    if audio_data:

        temp_filename = TEMP_AUDIO_FILE

        st.session_state.audio_bytes = audio_data.get("bytes")

        st.success(
            "Audio recorded successfully! You can now generate the transcript and meeting notes."
        )

        st.audio(
            st.session_state.audio_bytes,
            format="audio/wav"
        )

    if st.button("Generate AI Transcript and Notes"):

        if not st.session_state.developer_mode and not st.session_state.audio_bytes:

            st.warning(
                "Please record or upload an audio file first."
            )

            st.stop()

        if st.session_state.developer_mode:

            spinner_text = "Loading sample meeting data..."

        else:

            spinner_text = "Transcribing audio using Whisper AI..."

        with st.spinner(spinner_text):

            if not st.session_state.developer_mode:

                save_audio(
                    st.session_state.audio_bytes,
                    temp_filename
                )

            try:

                if st.session_state.developer_mode:

                    st.session_state.transcript = SAMPLE_TRANSCRIPT

                else:

                    st.session_state.transcript = transcribe_audio(
                        temp_filename
                    )

                with st.spinner(
                    "Summarizing notes and assigning tasks..."
                ):

                    if st.session_state.developer_mode:

                        st.session_state.meeting_notes = SAMPLE_MEETING_NOTES

                    else:

                        st.session_state.meeting_notes = summarize_meeting(
                            st.session_state.transcript,
                            meeting_title,
                            meeting_date,
                            language,
                            summary_type
                        )

                    if st.session_state.developer_mode:

                        st.session_state.meeting_insights = SAMPLE_INSIGHTS

                    else:

                        st.session_state.meeting_insights = generate_insights(
                            st.session_state.transcript
                        )

            except Exception as e:

                show_error(e)

            finally:

                if not st.session_state.developer_mode:

                    delete_file(temp_filename)

# Right panel - Results and analytics
with layout_col2:

    st.header("2. Live Transcript and AI Insights")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Raw Transcript",
            "Structured Meeting Notes",
            "AI Insights",
            "Meeting Analytics"
        ]
    )

    with tab1:

        if st.session_state.transcript:

            st.text_area(
                "Live Transcription Output",
                st.session_state.transcript,
                height=400
            )

        else:

            st.info(
                "Your raw transcript will appear here after processing."
            )

    with tab2:

        if st.session_state.meeting_notes:

            st.markdown(
                st.session_state.meeting_notes
            )

        else:

            st.info(
                "Your structured meeting notes will appear here after processing."
            )

    with tab3:

        if st.session_state.meeting_insights:

            insights = parse_insights(
                st.session_state.meeting_insights
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "😊 Sentiment",
                    insights.get(
                        "Meeting Sentiment",
                        "-"
                    )
                )

                st.metric(
                    "💼 Category",
                    insights.get(
                        "Meeting Category",
                        "-"
                    )
                )

            with col2:

                st.metric(
                    "🔥 Priority",
                    insights.get(
                        "Meeting Priority",
                        "-"
                    )
                )

                st.metric(
                    "⏱ Duration",
                    insights.get(
                        "Estimated Duration",
                        "-"
                    )
                )

        else:

            st.info(
                "AI meeting insights will appear here after processing."
            )

    with tab4:

        if st.session_state.transcript:

            stats = calculate_statistics(
                st.session_state.transcript
            )

            st.subheader("📊 Basic Statistics")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "📝 Word Count",
                    stats["Word Count"]
                )

                st.metric(
                    "📄 Character Count",
                    stats["Character Count"]
                )

            with col2:

                st.metric(
                    "📚 Line Count",
                    stats["Line Count"]
                )

                st.metric(
                    "⏱ Reading Time",
                    f'{stats["Reading Time"]} min'
                )

            st.divider()

            st.subheader("🧠 Meeting Quality")

            col3, col4 = st.columns(2)

            with col3:

                st.metric(
                    "📑 Total Sentences",
                    stats["Sentence Count"]
                )

                st.metric(
                    "📖 Longest Sentence",
                    f'{stats["Longest Sentence"]} words'
                )

            with col4:

                st.metric(
                    "📝 Avg Words / Sentence",
                    stats["Average Words"]
                )

                st.metric(
                    "💡 Vocabulary Richness",
                    f'{stats["Vocabulary"]}%'
                )

        else:

            st.info(
                "Meeting analytics will appear here after transcription."
            )

st.markdown("---")

# Export and download section
st.header("3. Download and Save Center")

down_col1, down_col2, down_col3, down_col4 = st.columns(4)

with down_col1:

    if st.session_state.audio_bytes:

        st.download_button(
            label="Save Raw Audio Recording (.wav)",
            data=st.session_state.audio_bytes,
            file_name="meeting_recording.wav",
            mime="audio/wav"
        )

    else:

        st.button(
            "Save Raw Audio Recording (.wav)",
            disabled=True
        )

with down_col2:

    if st.session_state.transcript:

        st.download_button(
            label="Save Transcript (.txt)",
            data=st.session_state.transcript,
            file_name="meeting_transcript.txt",
            mime="text/plain"
        )

    else:

        st.button(
            "Save Transcript (.txt)",
            disabled=True
        )

with down_col3:

    if st.session_state.meeting_notes:

        st.download_button(
            label="Save AI Meeting Notes (.md)",
            data=st.session_state.meeting_notes,
            file_name="ai_meeting_notes.md",
            mime="text/markdown"
        )

    else:

        st.button(
            "Save AI Meeting Notes (.md)",
            disabled=True
        )

with down_col4:

    if st.session_state.meeting_notes:

        create_pdf(
            TEMP_PDF_FILE,
            meeting_title,
            meeting_date,
            language,
            summary_type,
            st.session_state.meeting_notes
        )

        with open(TEMP_PDF_FILE, "rb") as pdf:
            pdf_bytes = pdf.read()

        st.download_button(
            label="Save PDF Report (.pdf)",
            data=pdf_bytes,
            file_name="meeting_notes.pdf",
            mime="application/pdf"
        )

    else:

        st.button(
            "Save PDF Report (.pdf)",
            disabled=True
        )

# Application footer
show_footer()
