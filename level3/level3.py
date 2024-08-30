# import streamlit as st
# import os
# import time  # Import time module for delay
# import re  # Import regular expressions module

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
# tv_show = st.selectbox("Choose a TV Show", ["SpongeBob", "PJ Masks", "Winx Club", "Spidey And His Amazing Friends"])

# # Initialize session state to keep track of the sentence index and user input
# if 'sentence_index' not in st.session_state:
#     st.session_state.sentence_index = 0
# if 'input_key' not in st.session_state:
#     st.session_state.input_key = 0  # Initialize input key

# if tv_show:
#     # Get the current sentence from the file
#     sentence = get_sentence(tv_show, st.session_state.sentence_index)
    
#     if sentence:
#         # Prepare the audio file path based on the selected TV show and sentence index
#         # Now the path includes the 'audio' folder
#         audio_file = f"audio/{tv_show}_{st.session_state.sentence_index}.mp3"

#         # Check if the MP3 file exists
#         if os.path.exists(audio_file):
#             # Play the audio file
#             st.audio(audio_file)
#         else:
#             st.error(f"Audio file {audio_file} not found.")

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
import time
import re

# Function to get the sentence from the text file based on TV show and index
def get_sentence(tv_show, sentence_index):
    with open("level3/listening_sen.txt", "r") as f:
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

def calculate_and_store_score(mistakes):
    score = 0
    if mistakes <= 1:
        score = 3  # 3 stars
    elif mistakes <= 3:
        score = 2  # 2 stars
    else:
        score = 1  # 1 star

    points = score * 100
    st.session_state['level3_score'] = score
    st.session_state['level3_points'] = points

def main():
    # Page styles and design
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
    st.markdown(f'<div class="text-container"><div class="level-heading">Level 3</div>', unsafe_allow_html=True)

    # Retrieve TV show from query params
    query_params = st.experimental_get_query_params()
    if "tv_show" in query_params:
        st.session_state["selected_tv_show"] = query_params["tv_show"][0]  # Adjusted to use the first item

    # Check if the TV show is already selected and stored
    if "selected_tv_show" not in st.session_state:
        st.session_state["selected_tv_show"] = "PJ Masks"  # Default to PJ Masks

    # Get the selected TV show
    show = st.session_state["selected_tv_show"]

    # Get the sentences from the selected TV show
    sentence = get_sentence(show, st.session_state.sentence_index)

    # Ensure the selected TV show is valid
    if sentence is None:
        st.error(f"No sentences available for TV show: {show}")
        st.stop()

    # Initialize session state
    if 'sentence_index' not in st.session_state:
        st.session_state.sentence_index = 0
    if 'mistakes' not in st.session_state:
        st.session_state.mistakes = 0
    if "final_congratulations" not in st.session_state:
        st.session_state.final_congratulations = False

    # Display "Return to Home Page" button as a red arrow
    st.markdown(
        """
        <div class="return-arrow">
            <a href="http://localhost:8000/index.html" target="_self">
                <i class="fas fa-arrow-left" style="color: red; font-size: 24px;"></i>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.sentence_index < len(sentence):
        st.markdown(f'<div class="text-container"><p>Listen to the sentence:</p>', unsafe_allow_html=True)

        # Prepare the audio file path based on the selected TV show and sentence index
        audio_file = f"level3/audio/{show}_{st.session_state.sentence_index}.mp3"

        # Check if the MP3 file exists
        if os.path.exists(audio_file):
            # Play the audio file
            st.audio(audio_file)
        else:
            st.error(f"Audio file {audio_file} not found.")

        # Input box for the user's answer
        user_input = st.text_input("What did you hear?")

        # Check the user's answer
        if st.button("Submit"):
            # Clean both the user input and the expected sentence
            cleaned_user_input = clean_text(user_input)
            cleaned_sentence = clean_text(sentence)

            if cleaned_user_input == cleaned_sentence:
                st.success("Correct! Moving to the next sentence.")
                time.sleep(2)  # Pause for 2 seconds before moving to the next sentence
                st.session_state.sentence_index += 1
                st.experimental_rerun()
            else:
                st.error("Incorrect, please try again.")
                time.sleep(2)  # Pause for 2 seconds before showing the input box again

    else:
        calculate_and_store_score(st.session_state.mistakes)

        # Display final score and stars
        st.session_state.final_congratulations = True
        st.markdown('<div class="final-congratulations">Congratulations! You\'ve completed the level.</div>', unsafe_allow_html=True)
        points = st.session_state['level3_points']
        st.markdown(f'<div class="final-score">Your score: {points} points</div>', unsafe_allow_html=True)

        stars_container = '<div class="final-stars">'
        for i in range(1, 4):
            star_class = 'star' if i <= st.session_state['level3_score'] else ''
            stars_container += f'<i class="fa fa-star {star_class}"></i>'
        stars_container += '</div>'
        st.markdown(stars_container, unsafe_allow_html=True)

        # Return to Home Page Button
        if st.button("Return to Home Page"):
            st.session_state.sentence_index = 0
            st.session_state.mistakes = 0
            
            # Append score and points to the URL
            home_url = f"http://localhost:8000/index.html?level3_score={st.session_state['level3_score']}&level3_points={st.session_state['level3_points']}"
            st.write(f'<meta http-equiv="refresh" content="0; url={home_url}">', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
