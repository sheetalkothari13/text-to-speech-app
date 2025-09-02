import streamlit as st
import asyncio
import edge_tts
import time
from io import BytesIO

st.set_page_config(page_title="Text → Speech", page_icon="🔊", layout="centered")

# Map (Language/Accent, Gender) -> Voice
VOICE_MAP = {
    ("English (India)", "Female"): "en-IN-NeerjaNeural",
    ("English (India)", "Male"):   "en-IN-PrabhatNeural",
    ("English (US)",    "Female"): "en-US-JennyNeural",
    ("English (US)",    "Male"):   "en-US-GuyNeural",
    ("Hindi",           "Female"): "hi-IN-SwaraNeural",
    ("Hindi",           "Male"):   "hi-IN-MadhurNeural",
}

async def synth_to_bytes(text: str, voice: str) -> bytes:
    """Synthesize to bytes with edge-tts."""
    communicate = edge_tts.Communicate(text, voice)
    audio_bytes = BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes.write(chunk["data"])
    return audio_bytes.getvalue()

st.title("🔊 Text → Speech")
st.caption("Type your message, pick a voice, and get an MP3.")

text = st.text_area(
    "Enter your text",
    height=160,
    placeholder="Type something nice…"
)

col1, col2 = st.columns(2)
with col1:
    lang_group = st.selectbox(
        "Language / Accent",
        ["English (India)", "English (US)", "Hindi"]
    )
with col2:
    gender = st.radio("Voice", ["Female", "Male"], horizontal=True)

generate = st.button("Generate Audio", type="primary", use_container_width=True, disabled=not text.strip())

if generate:
    voice = VOICE_MAP[(lang_group, gender)]
    with st.spinner("Synthesizing…"):
        # Streamlit runs sync code by default; run the coroutine
        audio_data = asyncio.run(synth_to_bytes(text.strip(), voice))

    st.success("Done! Preview below.")
    st.audio(audio_data, format="audio/mp3")

    filename = "Output.mp3"
    st.download_button("Download MP3", data=audio_data, file_name=filename, mime="audio/mpeg")

st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.9em;'>Made with ❤️ by Sheetal</p>",
    unsafe_allow_html=True
)