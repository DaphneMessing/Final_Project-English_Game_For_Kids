import openai
import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import re
from streamlit_javascript import st_javascript

openai.api_key = 'sk-proj-SRGCSAzogrcsQIu2kwiZT3BlbkFJp02fsLG6iUdA7G5kEfKg'

sentences = {
    "Spongebob": [
        "Squidward, Spongebob's neighbor, loves to play the clarinet.",
        "Spongebob enjoys flipping Krabby Patties at the Krusty Krab.",
        "Patrick often joins Spongebob on his jellyfishing adventures.",
        "Spongebob and Sandy Cheeks often practice karate together.",
        "Plankton constantly schemes to steal the Krabby Patty secret formula."
    ],
    "PJ Masks": [
        "Catboy uses his super speed to chase down the Night Ninja.",
        "Owlette flies high above the city to spot trouble below.",
        "Gekko uses his super strength to lift heavy objects effortlessly.",
        "The PJ Masks use their Owl-Glider, Cat-Car, and Gekko-Mobile to fight crime.",
        "Together, the PJ Masks foil Romeo's plans to take over the world."
    ],
    "Winx Club": [
        "Bloom learns to control the Dragon Flame, her powerful magical ability.",
        "The Winx Club often battles evil witches like Icy, Darcy, and Stormy.",
        "Stella creates dazzling light shields to protect her friends in battle.",
        "Tecna uses her technological gadgets to solve tricky problems.",
        "Musa’s songs and melodies can enchant and calm fierce creatures."
    ],
    "Spidey And His Amazing Friends": [
        "Spidey and his friends collaborate to outsmart the tricky Green Goblin.",
        "Ghost-Spider uses her acrobatic skills to dodge enemy attacks.",
        "Miles Morales, also known as Spin, has the power of invisibility.",
        "Teamwork and friendship help Spidey’s team overcome the toughest villains.",
        "They use their web shooters and quick reflexes to save the city."
    ]
}

# Function to clean text by removing punctuation and converting to lowercase
def clean_text(text):
    # Remove punctuation and convert to lowercase
    return re.sub(r'[^\w\s]', '', text).lower()

# Function to recognize and verify speech using OpenAI Whisper API
def recognize_speech(expected_sentence):
    samplerate = 44100  # Sample rate of the recording
    duration = 5  # Duration of the recording

    recording_placeholder = st.empty()
    recording_placeholder.markdown('<p style="text-align: center;">Recording...</p>', unsafe_allow_html=True)

    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished

    audio_data = np.squeeze(audio_data)

    # Save the recording to a WAV file
    wav_file = "speech.wav"
    wav.write(wav_file, samplerate, audio_data)

    with open(wav_file, "rb") as f:
        result = openai.Audio.transcribe("whisper-1", f, language="en")

    transcription = result['text']
    recording_placeholder.empty()  # Clears the "Recording..." message
    st.markdown(f'<div style="text-align: center;"><p>You said: {transcription}</p></div>', unsafe_allow_html=True)
    return clean_text(transcription) == clean_text(expected_sentence)

# Function to calculate score based on mistakes
def calculate_and_store_score(mistakes):
    score = 0
    if mistakes <= 1:
        score = 3  # 3 stars
    elif mistakes <= 3:
        score = 2  # 2 stars
    else:
        score = 1  # 1 star

    points = score * 100
    st.session_state['level5_score'] = score
    st.session_state['level5_points'] = points

def main():
    st.markdown(
        """
        <style>
            .container {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            .text-container {
                text-align: center;
            }
            .final-congratulations, .final-score, .final-stars {
                text-align: center;
            }
            .level-heading {
                font-size: 2rem;
                color: #0071e3;
                margin-bottom: 30px;
            }
            .final-congratulations {
                font-size: 2rem;
                color: #0071e3;
                margin-top: 20px;
            }
            .final-score {
                font-size: 1.5rem;
                color: #333333;
                margin-top: 10px;
            }
            .final-stars {
                margin-top: 15px;
                font-size: 2rem;
            }
            .final-stars i {
                color: grey;
                margin: 0 5px;
            }
            .final-stars .star {
                color: yellow;
            }
            .stButton button {
                display: block;
                margin: 20px auto;
                border-radius: 8px;
                padding: 12px 18px;
                font-size: 1.1rem;
            }
            .success-fail {
                text-align: center;
            }
            .return-arrow {
                position: absolute;
                top: 10px;
                left: 10px;
                cursor: pointer;
            }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        """, unsafe_allow_html=True
    )
        
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown(f'<div class="text-container"><div class="level-heading">Level 5</div>', unsafe_allow_html=True)

    # Retrieve TV show from query params
    query_params = st.query_params
    if "tv_show" in query_params:
        st.session_state["selected_tv_show"] = query_params["tv_show"]

    # Check if the TV show is already selected and stored
    if "selected_tv_show" not in st.session_state:
        st.session_state["selected_tv_show"] = "PJ Masks"  # Default to PJ Masks

    # Get the selected TV show
    show = st.session_state["selected_tv_show"]

    # Ensure the selected TV show is valid
    if show not in sentences:
        st.error(f"Invalid TV show selected: {show}")
        st.stop()

    sentence_list = sentences[show]

    # Initialize session state
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "mistakes" not in st.session_state:
        st.session_state.mistakes = 0
    if "start_button_pressed" not in st.session_state:
        st.session_state.start_button_pressed = False
    if "next_sentence" not in st.session_state:
        st.session_state.next_sentence = False
    if "final_congratulations" not in st.session_state:
        st.session_state.final_congratulations = False

    if st.session_state.index < len(sentence_list):
        # Display "Return to Home Page" button as a red arrow
        st.markdown(
            """
            <div class="return-arrow" style="position: absolute; top: -120px; left: 10px; cursor: pointer;">
                <a href="http://localhost:8000/index.html" target="_self">
                    <i class="fas fa-arrow-left" style="color: red; font-size: 24px;"></i>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        sentence = sentence_list[st.session_state.index]

        st.markdown(f'<div class="text-container"><p>Read the sentence: {sentence}</p>', unsafe_allow_html=True)

        # Check if the "Start Recording" button was pressed
        if st.session_state.start_button_pressed:
            result = recognize_speech(sentence)
            if result:
                st.session_state.success = True
                st.session_state.start_button_pressed = False
                st.session_state.next_sentence = True
                st.markdown('<div class="success-fail"><p style="color: green; font-size: 1.2rem;">Correct</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-fail"><p style="color: red;">Incorrect! Try again.</p></div>', unsafe_allow_html=True)
                st.session_state.start_button_pressed = False
                st.session_state.mistakes += 1

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
        calculate_and_store_score(st.session_state.mistakes)

        # Display final score and stars
        st.session_state.final_congratulations = True
        st.markdown('<div class="final-congratulations">Congratulations! You\'ve completed this level.</div>', unsafe_allow_html=True)
        points = st.session_state['level5_points']
        st.markdown(f'<div class="final-score">Your score: {points} points</div>', unsafe_allow_html=True)

        stars_container = '<div class="final-stars">'
        for i in range(1, 4):
            star_class = 'star' if i <= st.session_state['level5_score'] else ''
            stars_container += f'<i class="fa fa-star {star_class}"></i>'
        stars_container += '</div>'
        st.markdown(stars_container, unsafe_allow_html=True)

        # Return to Home Page Button
        if st.button("Return to Home Page"):
            st.session_state.index = 0  # Reset the index for future plays
            st.session_state.mistakes = 0
            st.session_state.success = False
            st.session_state.start_button_pressed = False
            st.session_state.next_sentence = False
            st.session_state.final_congratulations = False
            
            # Append score and points to the URL
            home_url = f"http://localhost:8000/index.html?level5_score={st.session_state['level5_score']}&level5_points={st.session_state['level5_points']}"
            st.write(f'<meta http-equiv="refresh" content="0; url={home_url}">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()