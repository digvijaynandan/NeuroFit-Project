import os
import tempfile
import streamlit as st
import requests

st.set_page_config(
    page_title="NeuroFit Voice Dashboard",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 NeuroFit Voice Dashboard")
st.markdown("Upload a WAV audio file and analyze your mood.")

uploaded_file = st.file_uploader("Upload WAV audio", type=["wav"])
if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    if st.button("Analyze Mood"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_input:
            temp_input.write(uploaded_file.read())
            temp_path = temp_input.name

        try:
            with open(temp_path, "rb") as f:
                response = requests.post("http://127.0.0.1:5000/analyze", files={"file": f})

            if response.status_code == 200:
                result = response.json()
                st.subheader("📝 Transcription")
                st.write(result.get("transcription", ""))

                st.subheader("📊 Sentiment Analysis")
                st.write(f"**Sentiment:** {result.get('sentiment', 'unknown')}\n**Confidence:** {result.get('confidence', 0)}")

                st.subheader("🎶 Suggested Playlist")
                playlist = result.get("spotify_playlist")
                if playlist:
                    st.markdown(f"[Open Playlist 🎵]({playlist})")
            else:
                st.error(f"Backend error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Unable to reach backend: {e}")
        finally:
            try:
                os.remove(temp_path)
            except OSError:
                pass
