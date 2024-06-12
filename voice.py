
import openai
import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

openai.api_key = 'sk-proj-5EFH4cZPnydPbqte06PQT3BlbkFJytQlGYnhClqkCuEmqjsI'

# Function to generate sentence based on show
def generate_sentence(show):
    if show == "Spongebob":
        return "Spongebob traveled on a trip to Bikini Bottom for a long time."
    elif show == "Cocomelon":
        return "Cocomelon traveled on a trip to the park for a long time."
    elif show == "PJ Masks":
        return "PJ Masks traveled on a trip to the city for a long time."

# Function to recognize and verify speech using OpenAI Whisper API
def recognize_speech(expected_sentence):
    samplerate = 44100  # Sample rate of the recording
    duration = 5  # Duration of the recording

    st.write(f"Please read the sentence: {expected_sentence}")
    st.text("Press 'Start Recording' to begin recording...")

    if st.button("Start Recording"):
        st.write("Recording...")
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()  # Wait until the recording is finished

        audio_data = np.squeeze(audio_data)

        # Save the recording to a WAV file
        wav_file = "speech.wav"
        wav.write(wav_file, samplerate, audio_data)

        with open(wav_file, "rb") as f:
            result = openai.Audio.transcribe("whisper-1", f, language="en")

        transcription = result['text']
        st.write("You said: ", transcription)
        return transcription.strip().lower() == expected_sentence.strip().lower()
    return None

def main():
    st.title("Voice Recognition App")

    show = st.selectbox("Select one of the following TV shows:", ["Spongebob", "Cocomelon", "PJ Masks"])
    sentence = generate_sentence(show)
    attempts = st.session_state.get('attempts', 3)
    
    if 'success' not in st.session_state:
        st.session_state.success = False

    if attempts > 0 and not st.session_state.success:
        result = recognize_speech(sentence)
        if result is not None:
            if result:
                st.success("Great job! You read the sentence correctly.")
                st.session_state.success = True
            else:
                attempts -= 1
                st.error(f"Let's try again. You have {attempts} attempts left.")
                st.session_state.attempts = attempts
    elif not st.session_state.success:
        st.warning("Better luck next time!")

if __name__ == "__main__":
    main()
