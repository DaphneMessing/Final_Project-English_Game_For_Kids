import streamlit as st
import os
import random

def read_sentences(file_path):
    with open(file_path, 'r') as file:
        sentences = file.readlines()
    return [sentence.strip() for sentence in sentences]

image_folder = "SpongeBob_img"
sentence_file = "SpongeBob_sentences_img.txt"

images = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith('.jpeg')])
sentences = read_sentences(sentence_file)

assert len(images) == len(sentences), "Number of images and sentences do not match!"

if 'image_index' not in st.session_state:
    st.session_state.image_index = 0

if 'selected_words' not in st.session_state:
    st.session_state.selected_words = []

if 'correct' not in st.session_state:
    st.session_state.correct = False

if 'shuffled_words' not in st.session_state:
    st.session_state.shuffled_words = []

if 'original_shuffled_words' not in st.session_state:
    st.session_state.original_shuffled_words = []

def select_word(index):
    word = st.session_state.shuffled_words[index]
    selected_index = st.session_state.selected_words.index('_')
    st.session_state.selected_words[selected_index] = word
    st.session_state.shuffled_words[index] = '_'

def deselect_word(index):
    word = st.session_state.selected_words[index]
    shuffled_index = st.session_state.shuffled_words.index('_')
    st.session_state.shuffled_words[shuffled_index] = word
    st.session_state.selected_words[index] = '_'

st.markdown("""
    <style>
    .stButton > button {
        display: block;
        margin: auto;
    }
    </style>
    """, unsafe_allow_html=True)

def display_image_and_sentence(image_path, sentence):
    st.image(image_path)
    
    if not st.session_state.shuffled_words:
        words = sentence.split()
        random.shuffle(words)
        st.session_state.shuffled_words = words
        st.session_state.selected_words = ['_'] * len(words)
        st.session_state.original_shuffled_words = words.copy()
    
    st.write("Reconstruct the sentence by pressing the words in the correct order:")
    
    remaining_words = [word for word in st.session_state.shuffled_words if word != '_']
    rows = (len(remaining_words) + 5) // 6  # Calculate number of rows needed
    for i in range(rows):
        cols = st.columns(6)
        for j, word in enumerate(remaining_words[i*6:(i+1)*6]):
            if word != '_':
                with cols[j]:
                    unique_key = f"word_{st.session_state.original_shuffled_words.index(word)}"
                    if st.button(word, key=unique_key, on_click=select_word, args=(st.session_state.shuffled_words.index(word),)):
                        pass
    
    st.write("Selected words (click to move back):")
    rows = (len(st.session_state.selected_words) + 5) // 6  # Calculate number of rows needed
    for i in range(rows):
        cols = st.columns(6)
        for j, word in enumerate(st.session_state.selected_words[i*6:(i+1)*6]):
            if word != '_':
                with cols[j]:
                    unique_key = f"selected_word_{st.session_state.original_shuffled_words.index(word)}"
                    if st.button(word, key=unique_key, on_click=deselect_word, args=(i*6 + j,)):
                        pass
    
    st.write("Current selection: " + " ".join([word for word in st.session_state.selected_words if word != '_']))
    
    if " ".join([word for word in st.session_state.selected_words if word != '_']) == sentence:
        st.session_state.correct = True
        st.success("Correct!")

st.title("Sentence Construction Game")

if st.session_state.image_index < len(images):
    display_image_and_sentence(images[st.session_state.image_index], sentences[st.session_state.image_index])
    if st.session_state.correct:
        if st.button("Continue"):
            st.session_state.image_index += 1
            st.session_state.selected_words = []  # Reset for the next image
            st.session_state.shuffled_words = []  # Reset shuffled words for the next image
            st.session_state.original_shuffled_words = []  # Reset original shuffled words for the next image
            st.session_state.correct = False
            st.experimental_rerun()
else:
    st.write("Congratulations! You've completed the game.")
