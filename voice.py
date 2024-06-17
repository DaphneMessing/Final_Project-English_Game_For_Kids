import openai
import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os

openai.api_key = 'sk-proj-5EFH4cZPnydPbqte06PQT3BlbkFJytQlGYnhClqkCuEmqjsI'

# Function to load sentences from file
def load_sentences(filename="sentences.txt"):
    sentences = {}
    current_show = None
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                current_show = line[2:]
                sentences[current_show] = []
            elif current_show:
                sentences[current_show].append(line)
    return sentences

# Function to recognize and verify speech using OpenAI Whisper API
def recognize_speech(expected_sentence):
    samplerate = 44100  # Sample rate of the recording
    duration = 5  # Duration of the recording

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

def main():
    st.title("Voice Recognition App")

    # Load sentences
    sentences = load_sentences()

    # Initialize session state
    if "show" not in st.session_state:
        st.session_state.show = None
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "success" not in st.session_state:
        st.session_state.success = False
    if "start_button_pressed" not in st.session_state:
        st.session_state.start_button_pressed = False
    if "next_sentence" not in st.session_state:
        st.session_state.next_sentence = False

    # Select TV show
    if st.session_state.show is None:
        show = st.selectbox("Select one of the following TV shows:", ["Spongebob", "Cocomelon", "PJ Masks"])
        if st.button("Confirm"):
            st.session_state.show = show
            st.experimental_rerun()
    else:
        show = st.session_state.show
        sentence_list = sentences[show]

        if st.session_state.index < len(sentence_list):
            sentence = sentence_list[st.session_state.index]

            # Display the sentence
            st.write(f"Please read the sentence: {sentence}")

            # Display the corresponding image
            image_path = f"{show}_VoiceImg/voice{st.session_state.index + 1}.jpeg"
            if os.path.exists(image_path):
                st.image(image_path, caption=f"Sentence {st.session_state.index + 1}", width=550)
            else:
                st.warning("Image not found.")

            # Check if the "Start Recording" button was pressed
            if st.session_state.start_button_pressed:
                result = recognize_speech(sentence)
                if result:
                    st.session_state.success = True
                    st.session_state.start_button_pressed = False
                    st.session_state.next_sentence = True
                    st.success("Great job! You read the sentence correctly.")
                else:
                    st.error("Let's try again.")
                    st.session_state.start_button_pressed = False

            # Show the "Start Recording" button or the "Continue" button
            if st.session_state.next_sentence:
                if st.button("Continue"):
                    st.session_state.next_sentence = False
                    st.session_state.index += 1
                    st.experimental_rerun()
            else:
                if st.button("Start Recording"):
                    st.session_state.start_button_pressed = True
                    st.experimental_rerun()
        else:
            st.success("You've completed all the sentences for this show!")
            st.balloons()  # Show balloons to celebrate completion

if __name__ == "__main__":
    main()