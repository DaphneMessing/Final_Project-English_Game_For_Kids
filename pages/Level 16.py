import streamlit as st
import os
import re
import base64
import time
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import openai

openai.api_key = 'sk-proj-SRGCSAzogrcsQIu2kwiZT3BlbkFJp02fsLG6iUdA7G5kEfKg'

# Sentences for speech recognition
sentences_speech = {
    "PJ Masks": [
        "Romeo builds a robot that can duplicate itself.",
        "The PJ Masks build a secret hideout to prepare for their next mission against Romeo."
    ],
    "Spongebob": [
        "Spongebob and Patrick accidentally release a jellyfish in the Krusty Krab.",
        "Mr. Krabs hides the secret formula inside a giant clam."
    ],
    "Winx Club": [
        "The Winx use their powers to protect the enchanted forest from evil creatures.",
        "Flora creates a potion to restore the magic of the ancient tree."
    ],
    "Spidey And His Amazing Friends": [
        "Miles swings across the city to stop Electro from causing a blackout.",
        "Spidey and Ghost-Spider team up to stop Doctor Octopus from robbing a bank."
    ]
}

# Function to get the text input sentence from the text file based on TV show and index
def get_expected_sentence(tv_show, sentence_index):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'sentences_level16.txt')  # Updated for Level 16
    with open(file_path, "r") as f:
        lines = f.readlines()
        sentences = [line.strip() for line in lines if line.startswith(tv_show)]
        if sentence_index < len(sentences):
            return sentences[sentence_index].split(":")[1].strip()
    return None

# Function to clean and normalize text by removing punctuation and converting to lowercase
def clean_text(text):
    if text is None:
        return ""
    return re.sub(r'[^\w\s]', '', text).lower()

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
    st.session_state['level16_score'] = score
    st.session_state['level16_points'] = points

# Function to play audio automatically without displaying controls
def play_audio_autoplay(file_path):
    if os.path.exists(file_path):
        audio_file = open(file_path, 'rb')
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f'''
            <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        '''
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.error(f"Audio file {file_path} not found.")

# Function to play audio using base64 encoding with updated style
def play_audio(file_path):
    if os.path.exists(file_path):
        audio_file = open(file_path, 'rb')
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f'''
            <div class="text-container">
                <audio controls style="margin: 20px auto; display: block;">
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            </div>
        '''
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.error(f"Audio file {file_path} not found.")

# Function to recognize and verify speech using OpenAI Whisper API
def recognize_speech(expected_sentence):
    samplerate = 44100  # Sample rate of the recording
    duration = 8  # Duration of the recording

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
    
    cleaned_transcription = clean_text(transcription)
    cleaned_expected_sentence = clean_text(expected_sentence)

    # Debugging information
    print("Debug - Speech Recognition:", {'Raw transcription': transcription, 'Cleaned transcription': cleaned_transcription, 'Cleaned expected sentence': cleaned_expected_sentence})

    return cleaned_transcription == cleaned_expected_sentence

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
    st.markdown(f'<div class="text-container"><div class="level-heading">Level 16</div>', unsafe_allow_html=True)

    # Retrieve TV show from query params
    query_params = st.query_params
    if "tv_show" in query_params:
        st.session_state["selected_tv_show"] = query_params["tv_show"]

    # Check if the TV show is already selected and stored
    if "selected_tv_show" not in st.session_state:
        st.session_state["selected_tv_show"] = "PJ Masks"  # Default to PJ Masks

    # Get the selected TV show
    show = st.session_state["selected_tv_show"]

    # Initialize session state
    if 'index' not in st.session_state:
        st.session_state.index = 0
    if 'mistakes' not in st.session_state:
        st.session_state.mistakes = 0
    if 'show_message' not in st.session_state:
        st.session_state.show_message = False
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0

    if st.session_state.index < 4:
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

    # Check if all sentences have been completed
    if st.session_state.index >= 4:
        calculate_and_store_score(st.session_state.mistakes)

        # Play completion audio automatically without display
        show_no_spaces = show.replace(" ", "")
        completion_audio_file = os.path.join(os.path.dirname(__file__), '..', f"{show_no_spaces}_won.mp3")
        play_audio_autoplay(completion_audio_file)

        st.markdown('<div class="final-congratulations">Well done! YOU WON THE GAME! </div>', unsafe_allow_html=True)
        points = st.session_state['level16_points']
        st.markdown(f'<div class="final-score">Your score: {points} points</div>', unsafe_allow_html=True)

        stars_container = '<div class="final-stars">'
        for i in range(1, 4):
            star_class = 'star' if i <= st.session_state['level16_score'] else ''
            stars_container += f'<i class="fa fa-star {star_class}"></i>'
        stars_container += '</div>'
        st.markdown(stars_container, unsafe_allow_html=True)

        # Return to Home Page Button
        if st.button("Return to Home Page"):
            st.session_state.index = 0
            st.session_state.mistakes = 0
            st.session_state.show_message = False
            st.session_state.input_key = 0  # Reset input key
            home_url = f"http://localhost:8000/index.html?level16_score={st.session_state['level16_score']}&level16_points={st.session_state['level16_points']}"
            st.write(f'<meta http-equiv="refresh" content="0; url={home_url}">', unsafe_allow_html=True)
        return

    # Determine if it's a speech or text input sentence
    if st.session_state.index % 2 == 0:
        # **Updated Logic for Sentence at Index 0 and 2**
        if st.session_state.index in [0, 2]:
            # Implement the Level 2 logic and design
            sentence = sentences_speech[show][st.session_state.index // 2]
            st.markdown(f'<div class="text-container"><p>Read the sentence: {sentence}</p>', unsafe_allow_html=True)

            if "start_button_pressed" not in st.session_state:
                st.session_state.start_button_pressed = False
            if "next_sentence" not in st.session_state:
                st.session_state.next_sentence = False

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
            # Original logic for other sentences
            sentence = sentences_speech[show][st.session_state.index // 2]
            st.markdown(f'<div class="text-container"><p>Read the sentence: {sentence}</p>', unsafe_allow_html=True)

            if st.button("Start Recording"):
                result = recognize_speech(sentence)
                if result:
                    st.markdown('<div class="success-fail" style="color: green;">Correct! Moving to the next sentence.</div>', unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.index += 1
                    st.experimental_rerun()
                else:
                    st.markdown('<div class="success-fail" style="color: red;">Incorrect! Try again.</div>', unsafe_allow_html=True)

    elif st.session_state.index % 2 == 1:
        # Text input sentence
        expected_sentence = get_expected_sentence(show, (st.session_state.index - 1) // 2)

        if expected_sentence:
            # Display "Listen to the sentence:"
            st.markdown('<div class="text-container"><p>Listen to the sentence:</p></div>', unsafe_allow_html=True)
            
            # Prepare the audio file path for the text input level
            show_no_spaces = show.replace(" ", "")
            audio_file = os.path.join(os.path.dirname(__file__), '..', 'audio_level16', f"{show_no_spaces}_{(st.session_state.index - 1) // 2}.mp3")
            play_audio(audio_file)  # Display styled audio control for user to click play
            
            # Display the input field with an explanation
            st.markdown('<div class="text-container"><p>What did you hear?</p>', unsafe_allow_html=True)

            # Form to handle Enter key as submission
            with st.form(key='user_input_form'):
                # Input box for the user's answer
                user_input = st.text_input(
                    "Type your answer here",  # Non-empty label for accessibility
                    key=f"user_input_key_{st.session_state.input_key}",  # Dynamic key to reset input
                    label_visibility="collapsed"
                )
                
                # Submit button within the form
                submit_button = st.form_submit_button("Submit")
            
            # Placeholder for the message
            message_placeholder = st.empty()

            # Check if the "Submit" button was pressed
            if submit_button:
                cleaned_user_input = clean_text(user_input)
                cleaned_expected_sentence = clean_text(expected_sentence)

                # Debugging information for text input
                print("Debug - Text Input:", {'Raw user input': user_input, 'Cleaned user input': cleaned_user_input, 'Cleaned expected sentence': cleaned_expected_sentence})

                if cleaned_user_input == cleaned_expected_sentence:
                    message_placeholder.markdown('<div class="success-fail" style="color: green;">Correct! Moving to the next sentence.</div>', unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.index += 1
                    st.experimental_rerun()
                else:
                    message_placeholder.markdown('<div class="success-fail" style="color: red;">Incorrect! Try again.</div>', unsafe_allow_html=True)
                    time.sleep(2)  # Pause for 2 seconds before clearing the input and message
                    st.session_state.input_key += 1  # Change key to reset input box
                    st.session_state.show_message = False  # Reset message visibility
                    st.experimental_rerun()
        else:
            st.error("Expected sentence not found. Please check the text file.")

if __name__ == "__main__":
    main()
