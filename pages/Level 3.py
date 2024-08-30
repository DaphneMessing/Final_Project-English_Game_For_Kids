import streamlit as st
import os
import re

# Function to get the sentence from the text file based on TV show and index
def get_sentence(tv_show, sentence_index):
    # Construct the correct relative path to the file from the pages folder to the root folder
    file_path = os.path.join(os.path.dirname(__file__), '..', 'listening_sen.txt')
    
    with open(file_path, "r") as f:
        lines = f.readlines()
        sentences = [line.strip() for line in lines if line.startswith(tv_show)]
        if sentence_index < len(sentences):
            return sentences[sentence_index].split(":")[1].strip()
    return None

# Function to clean and normalize text by removing punctuation and converting to lowercase
def clean_text(text):
    cleaned_text = re.sub(r'[^A-Za-z0-9]', '', text)
    return cleaned_text.lower()

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
    st.session_state['level3_score'] = score
    st.session_state['level3_points'] = points

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
                margin-top: 10px;
                font-size: 1.2rem;
            }
            .success-message {
                color: green;
            }
            .error-message {
                color: red;
            }
            .return-arrow {
                position: absolute;
                top: 10px;  /* Same positioning as Level 2 */
                left: 10px;   /* Same positioning as Level 2 */
                cursor: pointer;
            }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        """, unsafe_allow_html=True
    )

    # Display "Return to Home Page" button as a red arrow in the upper part of the page
    st.markdown(
        """
        <div class="return-arrow" style="position: absolute; top: 10px; left: 10px; cursor: pointer;">
            <a href="http://localhost:8000/index.html" target="_self">
                <i class="fas fa-arrow-left" style="color: red; font-size: 24px;"></i>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown(f'<div class="text-container"><div class="level-heading">Level 3</div>', unsafe_allow_html=True)

    # Retrieve TV show from query params
    query_params = st.query_params
    if "tv_show" in query_params:
        st.session_state["selected_tv_show"] = query_params["tv_show"]

    # Check if the TV show is already selected and stored
    if "selected_tv_show" not in st.session_state:
        st.session_state["selected_tv_show"] = "PJ Masks"  # Default to PJ Masks

    # Get the selected TV show
    show = st.session_state["selected_tv_show"]

    # Remove spaces from the TV show name for file path
    show_no_spaces = show.replace(" ", "")

    # Initialize session state to keep track of the sentence index, user input, mistakes, and button visibility
    if 'sentence_index' not in st.session_state:
        st.session_state.sentence_index = 0
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0  # Initialize input key
    if 'mistakes' not in st.session_state:
        st.session_state.mistakes = 0
    if 'final_congratulations' not in st.session_state:
        st.session_state.final_congratulations = False
    if 'show_continue_button' not in st.session_state:
        st.session_state.show_continue_button = False  # Controls visibility of Continue button
    if 'show_try_again_button' not in st.session_state:
        st.session_state.show_try_again_button = False  # Controls visibility of Try Again button

    # Get the current sentence from the file
    sentence = get_sentence(show, st.session_state.sentence_index)

    if sentence:
        # Prepare the audio file path based on the selected TV show and sentence index
        audio_file = os.path.join(os.path.dirname(__file__), '..', 'audio', f"{show_no_spaces}_{st.session_state.sentence_index}.mp3")

        # Check if the MP3 file exists
        if os.path.exists(audio_file):
            # Play the audio file
            st.audio(audio_file)
        else:
            st.error(f"Audio file {audio_file} not found.")

        # Input box for the user's answer
        user_input = st.text_input(
            "What did you hear?",
            value='' if st.session_state.show_try_again_button else '',
            key=f"user_input_box_{st.session_state.input_key}"  # Dynamic key for input box
        )

        # Create placeholders for the messages and buttons to dynamically update
        message_placeholder = st.empty()
        button_placeholder = st.empty()

        # Display the "Submit", "Continue", or "Try Again" button based on the answer correctness
        if st.session_state.show_continue_button:
            # Show "Correct" message above "Continue" button
            message_placeholder.markdown('<div class="success-fail success-message">Correct!</div>', unsafe_allow_html=True)
            with button_placeholder:
                if st.button("Continue", key="continue_button"):
                    # Move to the next sentence
                    st.session_state.sentence_index += 1
                    st.session_state.input_key += 1  # Change key to reset input box
                    st.session_state.show_continue_button = False  # Hide Continue button

                    # Check if there are more sentences (0-3 for each TV show)
                    if st.session_state.sentence_index > 3:
                        calculate_and_store_score(st.session_state.mistakes)
                        st.session_state.final_congratulations = True
                        st.experimental_rerun()  # Rerun to display the final message
                    else:
                        st.experimental_rerun()

        elif st.session_state.show_try_again_button:
            # Show "Incorrect! Try again." message above "Try Again" button
            message_placeholder.markdown('<div class="success-fail error-message">Incorrect! Try again.</div>', unsafe_allow_html=True)
            with button_placeholder:
                if st.button("Try Again", key="try_again_button"):
                    # Clear the input and reset visibility for next attempt
                    st.session_state.input_key += 1  # Change key to reset input box
                    st.session_state.show_try_again_button = False  # Hide Try Again button
                    st.experimental_rerun()

        else:
            # Show "Submit" button for checking the answer
            if button_placeholder.button("Submit", key="submit_button"):
                cleaned_user_input = clean_text(user_input)
                cleaned_sentence = clean_text(sentence)

                if cleaned_user_input == cleaned_sentence:
                    st.session_state.show_continue_button = True  # Show Continue button
                    message_placeholder.markdown('<div class="success-fail success-message">Correct!</div>', unsafe_allow_html=True)  # Display "Correct" message
                    st.experimental_rerun()  # Automatically rerun to hide Submit and show Continue
                else:
                    st.session_state.show_try_again_button = True  # Show Try Again button
                    message_placeholder.markdown('<div class="success-fail error-message">Incorrect! Try again.</div>', unsafe_allow_html=True)  # Display "Incorrect" message
                    st.session_state.mistakes += 1  # Increment mistakes counter
                    st.experimental_rerun()

    else:
        if st.session_state.final_congratulations:
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
                st.session_state.sentence_index = 0  # Reset the index for future plays
                st.session_state.input_key += 1  # Change key to reset input box
                st.session_state.mistakes = 0
                st.session_state.final_congratulations = False
                
                # Append score and points to the URL
                home_url = f"http://localhost:8000/index.html?level3_score={st.session_state['level3_score']}&level3_points={st.session_state['level3_points']}"
                st.write(f'<meta http-equiv="refresh" content="0; url={home_url}">', unsafe_allow_html=True)
        else:
            st.write("No more sentences available for this show.")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
