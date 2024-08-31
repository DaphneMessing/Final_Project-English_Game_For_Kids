import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image
import os
import glob
import shutil

# Function to get the prompt based on user inputs
def get_prompt(gender, tv_show):
    gender_str = "girl" if gender == "Female" else "boy"
    character = ""
    if tv_show == "Spidey And His Amazing Friends":
        character = "Spiderman"
    elif tv_show == "PJ Masks":
        character = "Gekko from PJ Masks"
    elif tv_show == "Spongebob":
        character = "SpongeBob"
    elif tv_show == "Winx Club":
        character = "Flora from Winx"
    
    return f"A full body photo of a {gender_str} dressed in a complete {character} costume, showing the entire body from head to toe, including the legs, on a plain white background with no other elements"

# Function to remove the background using the Hugging Face Gradio model
def remove_background(image_path):
    client = Client("ECCV2022/dis-background-removal")
    result = client.predict(
        image=handle_file(image_path),
        api_name="/predict"
    )
    
    background_removed_image_path = result[0]  # Path to the image with background removed
    return background_removed_image_path

# Function to clear the existing images in the directory
def clear_directory(directory):
    files = glob.glob(os.path.join(directory, '*'))
    for f in files:
        os.remove(f)

def handle_skip(tv_show):
    # Map default images for each TV show
    default_images = {
        "Spidey And His Amazing Friends": "default_player_img/default_spidey.png",
        "PJ Masks": "default_player_img/default_pj_masks.png",
        "Spongebob": "default_player_img/default_spongebob.png",
        "Winx Club": "default_player_img/default_winx_club.png"
    }

    # Get the path to the default image for the selected TV show
    selected_image = default_images.get(tv_show, None)

    if selected_image:
        # Define the destination path in the user_img directory
        destination_path = os.path.join("user_img", "generated_image_no_bg.png")
        
        # Copy the default image to the user_img directory with the correct name
        try:
            shutil.copy(selected_image, destination_path)

            # Update session state to indicate that the image is generated
            st.session_state['image_generated'] = True
            st.session_state['selected_image_path'] = destination_path

            # Update session state for skipping
            st.session_state['skip_image_generation'] = True

            # Force rerun to handle the skip logic
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error copying default image: {e}")  # Display error message


# Get selected TV show from URL query parameters
query_params = st.query_params
tv_show = query_params.get('tv_show', [None])

if not tv_show:
    st.error("No TV show selected. Please go back and select a TV show.")
else:
    # Ensure the user_img directory exists
    output_dir = "user_img"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize session state for image generation
    if 'image_generated' not in st.session_state:
        st.session_state['image_generated'] = False
    if 'button_clicked' not in st.session_state:
        st.session_state['button_clicked'] = False
    if 'error_occurred' not in st.session_state:
        st.session_state['error_occurred'] = False
    if 'skip_image_generation' not in st.session_state:
        st.session_state['skip_image_generation'] = False

    # Handle the skip state by redirecting to the home page
    if st.session_state['skip_image_generation']:
        st.markdown(f'<meta http-equiv="refresh" content="0; url=http://localhost:8000/index.html">', unsafe_allow_html=True)

    # Streamlit UI
    st.markdown(
        """
        <style>
            .center-container {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            .stButton button {
                display: block;
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 1.1rem;
                margin: auto;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Create a two-column layout to position the "Skip" button to the right
    col1, col2 = st.columns([8, 1])

    with col2:
        if st.button("Skip"):
            handle_skip(tv_show)

    # Heading below the button
    st.markdown("<h1 style='font-size: 36px; text-align: center;'>Creating Your Player</h1>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload a close-up picture of your face", type=["jpg", "jpeg", "png"])
    gender = st.selectbox("Select your gender", ["Male", "Female"])

    # Placeholder for the button or message
    button_placeholder = st.empty()

    # Center the button or message
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    
    # Check if the "Generate Image" button was pressed
    if not st.session_state['button_clicked']:
        if button_placeholder.button("Generate Image"):
            if uploaded_file is not None:  # Ensure an image is uploaded before starting
                st.session_state['button_clicked'] = True  # Set flag to True to hide button
                st.session_state['error_occurred'] = False  # Reset error state
                st.experimental_rerun()  # Rerun immediately to hide the button
            else:
                st.error("Please upload an image.")  # Show an error if no image is uploaded

    # Process the image if the button was clicked
    if st.session_state['button_clicked']:
        # Display the "Creating the image..." message instead of the button
        button_placeholder.markdown("<p style='text-align: center;'>Creating the image...</p>", unsafe_allow_html=True)

        if uploaded_file is not None:
            # Clear the directory before saving the new image
            clear_directory(output_dir)

            with open("temp.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())

            prompt = get_prompt(gender, tv_show)

            try:
                client = Client("multimodalart/Ip-Adapter-FaceID")

                result = client.predict(
                    images=[handle_file("temp.jpg")],
                    prompt=prompt,
                    negative_prompt="",
                    preserve_face_structure=True,
                    face_strength=1.0,
                    likeness_strength=1.0,
                    nfaa_negative_prompt="naked, bikini, skimpy, scanty, bare skin, lingerie, swimsuit, exposed, see-through",
                    api_name="/generate_image"
                )

                if result and isinstance(result, list) and "image" in result[0]:
                    first_image_path = result[0]["image"]
                    first_image = Image.open(first_image_path)

                    background_removed_image_path = remove_background(first_image_path)
                    background_removed_image = Image.open(background_removed_image_path)

                    save_path = os.path.join(output_dir, "generated_image_no_bg.png")
                    background_removed_image.save(save_path)

                    # Set the session state variable to True after successful generation
                    st.session_state['image_generated'] = True
                    st.session_state['button_clicked'] = False  # Reset button click state

                else:
                    st.error("An error occurred, please try again.")
                    st.session_state['button_clicked'] = False  # Reset button state to show the button again
                    st.session_state['error_occurred'] = True  # Indicate an error occurred

            except Exception as e:
                st.error("An error occurred, please try again.")
                st.write(f"Exception details: {e}")
                st.session_state['button_clicked'] = False  # Reset button state to show the button again
                st.session_state['error_occurred'] = True  # Indicate an error occurred

    # Show "Generate Image" button again if there was an error
    if st.session_state['error_occurred']:
        if button_placeholder.button("Generate Image"):
            if uploaded_file is not None:  # Ensure an image is uploaded before starting
                st.session_state['button_clicked'] = True
                st.session_state['error_occurred'] = False  # Reset error state
                st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # Close the center-container div

    # Display the "Start" button if the image has been generated
    if st.session_state['image_generated']:
        if st.button("Start"):
            home_url = "http://localhost:8000/index.html"
            st.markdown(f'<meta http-equiv="refresh" content="0; url={home_url}">', unsafe_allow_html=True)
