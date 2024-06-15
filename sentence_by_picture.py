import streamlit as st
import os
import random

# Function to read sentences from a text file
def read_sentences(file_path):
    with open(file_path, 'r') as file:
        sentences = file.readlines()
    return [sentence.strip() for sentence in sentences]

# Path to the image folder and sentence file
image_folder = "SpongeBob_img"
sentence_file = "SpongeBob_sentences_img.txt"

# Get list of images and sentences
images = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith('.jpeg')])
sentences = read_sentences(sentence_file)

# Ensure the number of images matches the number of sentences
assert len(images) == len(sentences), "Number of images and sentences do not match!"

# Initialize session state
if 'image_index' not in st.session_state:
    st.session_state.image_index = 0

if 'selected_words' not in st.session_state:
    st.session_state.selected_words = []

if 'correct' not in st.session_state:
    st.session_state.correct = False

if 'shuffled_words' not in st.session_state:
    st.session_state.shuffled_words = []

# Custom CSS to center the buttons within their columns
st.markdown("""
    <style>
    .stButton > button {
        display: block;
        margin: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to display image and buttons for sentence words
def display_image_and_sentence(image_path, sentence):
    st.image(image_path)
    
    # Shuffle words only if they haven't been shuffled for this sentence
    if not st.session_state.shuffled_words:
        words = sentence.split()
        random.shuffle(words)
        st.session_state.shuffled_words = words
        st.session_state.selected_words = ['_'] * len(words)
    
    st.write("Reconstruct the sentence by pressing the words in the correct order:")
    
    # Display buttons for each word in the shuffled list
    remaining_words = [word for word in st.session_state.shuffled_words if word != '_']
    if remaining_words:
        rows = (len(remaining_words) + 5) // 6  # Calculate number of rows needed
        for i in range(rows):
            cols = st.columns(6)
            for j, word in enumerate(remaining_words[i*6:(i+1)*6]):
                with cols[j]:
                    if st.button(word, key=f"word_{i*6 + j}"):
                        index = st.session_state.selected_words.index('_')
                        st.session_state.selected_words[index] = word
                        st.session_state.shuffled_words[st.session_state.shuffled_words.index(word)] = '_'
                        st.experimental_rerun()
    
    # Display selected words as buttons to allow moving back to selectable options
    st.write("Selected words (click to move back):")
    rows = (len(st.session_state.selected_words) + 5) // 6  # Calculate number of rows needed
    for i in range(rows):
        cols = st.columns(6)
        for j, word in enumerate(st.session_state.selected_words[i*6:(i+1)*6]):
            with cols[j]:
                if word != '_' and st.button(word, key=f"selected_word_{i*6 + j}"):
                    st.session_state.shuffled_words[st.session_state.shuffled_words.index('_')] = word
                    st.session_state.selected_words[i*6 + j] = '_'
                    st.experimental_rerun()
    
    # Display current selected words
    st.write("Current selection: " + " ".join([word for word in st.session_state.selected_words if word != '_']))
    
    # Check if the sentence is correct
    if " ".join([word for word in st.session_state.selected_words if word != '_']) == sentence:
        st.session_state.correct = True
        st.success("Correct!")

# Main Streamlit app
st.title("Sentence Construction Game")

if st.session_state.image_index < len(images):
    correct = display_image_and_sentence(images[st.session_state.image_index], sentences[st.session_state.image_index])
    if st.session_state.correct:
        if st.button("Continue"):
            st.session_state.image_index += 1
            st.session_state.selected_words = []  # Reset for the next image
            st.session_state.shuffled_words = []  # Reset shuffled words for the next image
            st.session_state.correct = False
            st.experimental_rerun()
else:
    st.write("Congratulations! You've completed the game.")
