import streamlit as st
import pyttsx3
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to generate an MP3 file from a text sentence
def generate_audio(sentence, filename):
    engine.save_to_file(sentence, filename)
    engine.runAndWait()

# Function to get the sentence from the text file based on TV show and index
def get_sentence(tv_show, sentence_index):
    with open("listening_sen.txt", "r") as f:
        lines = f.readlines()
        sentences = [line.strip() for line in lines if line.startswith(tv_show)]
        if sentence_index < len(sentences):
            return sentences[sentence_index].split(":")[1].strip()
    return None

# App UI
st.title("Learning English with Your Favorite TV Show")

# Select TV show
tv_show = st.selectbox("Choose a TV Show", ["SpongeBob", "PJ Mask", "Winx"])

# Initialize session state to keep track of the sentence index
if 'sentence_index' not in st.session_state:
    st.session_state.sentence_index = 0

if tv_show:
    # Get the current sentence from the file
    sentence = get_sentence(tv_show, st.session_state.sentence_index)
    
    if sentence:
        audio_file = f"{tv_show}_{st.session_state.sentence_index}.mp3"
        
        # Generate the audio file if it doesn't already exist
        if not os.path.exists(audio_file):
            generate_audio(sentence, audio_file)

        # Play the audio file
        st.audio(audio_file)

        # Input box for the user's answer
        user_input = st.text_input("What did you hear?")

        # Check the user's answer
        if st.button("Submit"):
            if user_input.lower() == sentence.lower():
                st.success("Correct! Moving to the next sentence.")
                st.session_state.sentence_index += 1

                # Check if there are more sentences
                if get_sentence(tv_show, st.session_state.sentence_index) is None:
                    st.write("Congratulations! You've completed all the sentences.")
                else:
                    # Reset the input box for the next sentence
                    st.experimental_rerun()
            else:
                st.error("Incorrect, please try again.")

        # Reset button to start over
        if st.button("Start Over"):
            st.session_state.sentence_index = 0
            st.experimental_rerun()
    else:
        st.write("No more sentences available for this show.")
