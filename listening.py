# import streamlit as st
# import pyttsx3
# import os
# import time  # Import time module for delay
# import re  # Import regular expressions module

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Function to generate an MP3 file from a text sentence
# def generate_audio(sentence, filename):
#     engine.save_to_file(sentence, filename)
#     engine.runAndWait()

# # Function to get the sentence from the text file based on TV show and index
# def get_sentence(tv_show, sentence_index):
#     with open("listening_sen.txt", "r") as f:
#         lines = f.readlines()
#         sentences = [line.strip() for line in lines if line.startswith(tv_show)]
#         if sentence_index < len(sentences):
#             return sentences[sentence_index].split(":")[1].strip()
#     return None

# # Function to clean and normalize text by removing punctuation and converting to lowercase
# def clean_text(text):
#     # Remove all non-alphanumeric characters using regular expressions
#     cleaned_text = re.sub(r'[^A-Za-z0-9]', '', text)
#     return cleaned_text.lower()

# # App UI
# st.title("Learning English with Your Favorite TV Show")

# # Select TV show
# tv_show = st.selectbox("Choose a TV Show", ["SpongeBob", "PJ Mask", "Winx"])

# # Initialize session state to keep track of the sentence index and user input
# if 'sentence_index' not in st.session_state:
#     st.session_state.sentence_index = 0
# if 'input_key' not in st.session_state:
#     st.session_state.input_key = 0  # Initialize input key

# if tv_show:
#     # Get the current sentence from the file
#     sentence = get_sentence(tv_show, st.session_state.sentence_index)
    
#     if sentence:
#         audio_file = f"{tv_show}_{st.session_state.sentence_index}.mp3"
        
#         # Generate the audio file if it doesn't already exist
#         if not os.path.exists(audio_file):
#             generate_audio(sentence, audio_file)

#         # Play the audio file
#         st.audio(audio_file)

#         # Input box for the user's answer
#         user_input = st.text_input(
#             "What did you hear?",
#             key=f"user_input_box_{st.session_state.input_key}"  # Dynamic key for input box
#         )

#         # Check the user's answer
#         if st.button("Submit"):
#             # Clean both the user input and the expected sentence
#             cleaned_user_input = clean_text(user_input)
#             cleaned_sentence = clean_text(sentence)

#             if cleaned_user_input == cleaned_sentence:
#                 st.success("Correct! Moving to the next sentence.")
#                 time.sleep(2)  # Pause for 2 seconds before moving to the next sentence
#                 st.session_state.sentence_index += 1
#                 st.session_state.input_key += 1  # Change key to reset input box

#                 # Check if there are more sentences
#                 if get_sentence(tv_show, st.session_state.sentence_index) is None:
#                     st.write("Congratulations! You've completed all the sentences.")
#                 else:
#                     # Reset the input box for the next sentence
#                     st.experimental_rerun()
#             else:
#                 st.error("Incorrect, please try again.")
#                 time.sleep(2)  # Pause for 2 seconds before showing the input box again
#                 st.session_state.input_key += 1  # Change key to reset input box
#                 st.experimental_rerun()

#         # Reset button to start over
#         if st.button("Start Over"):
#             st.session_state.sentence_index = 0
#             st.session_state.input_key += 1  # Change key to reset input box
#             st.experimental_rerun()
#     else:
#         st.write("No more sentences available for this show.")

import streamlit as st
import os
import time  # Import time module for delay
import re  # Import regular expressions module

# Function to get the sentence from the text file based on TV show and index
def get_sentence(tv_show, sentence_index):
    with open("listening_sen.txt", "r") as f:
        lines = f.readlines()
        sentences = [line.strip() for line in lines if line.startswith(tv_show)]
        if sentence_index < len(sentences):
            return sentences[sentence_index].split(":")[1].strip()
    return None

# Function to clean and normalize text by removing punctuation and converting to lowercase
def clean_text(text):
    # Remove all non-alphanumeric characters using regular expressions
    cleaned_text = re.sub(r'[^A-Za-z0-9]', '', text)
    return cleaned_text.lower()

# App UI
st.title("Learning English with Your Favorite TV Show")

# Select TV show
tv_show = st.selectbox("Choose a TV Show", ["SpongeBob", "PJ Masks", "Winx Club", "Spidey And His Amazing Friends"])

# Initialize session state to keep track of the sentence index and user input
if 'sentence_index' not in st.session_state:
    st.session_state.sentence_index = 0
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0  # Initialize input key

if tv_show:
    # Get the current sentence from the file
    sentence = get_sentence(tv_show, st.session_state.sentence_index)
    
    if sentence:
        # Prepare the audio file path based on the selected TV show and sentence index
        # Now the path includes the 'audio' folder
        audio_file = f"audio/{tv_show}_{st.session_state.sentence_index}.mp3"

        # Check if the MP3 file exists
        if os.path.exists(audio_file):
            # Play the audio file
            st.audio(audio_file)
        else:
            st.error(f"Audio file {audio_file} not found.")

        # Input box for the user's answer
        user_input = st.text_input(
            "What did you hear?",
            key=f"user_input_box_{st.session_state.input_key}"  # Dynamic key for input box
        )

        # Check the user's answer
        if st.button("Submit"):
            # Clean both the user input and the expected sentence
            cleaned_user_input = clean_text(user_input)
            cleaned_sentence = clean_text(sentence)

            if cleaned_user_input == cleaned_sentence:
                st.success("Correct! Moving to the next sentence.")
                time.sleep(2)  # Pause for 2 seconds before moving to the next sentence
                st.session_state.sentence_index += 1
                st.session_state.input_key += 1  # Change key to reset input box

                # Check if there are more sentences
                if get_sentence(tv_show, st.session_state.sentence_index) is None:
                    st.write("Congratulations! You've completed all the sentences.")
                else:
                    # Reset the input box for the next sentence
                    st.experimental_rerun()
            else:
                st.error("Incorrect, please try again.")
                time.sleep(2)  # Pause for 2 seconds before showing the input box again
                st.session_state.input_key += 1  # Change key to reset input box
                st.experimental_rerun()

        # Reset button to start over
        if st.button("Start Over"):
            st.session_state.sentence_index = 0
            st.session_state.input_key += 1  # Change key to reset input box
            st.experimental_rerun()
    else:
        st.write("No more sentences available for this show.")
