import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image
import os
import glob

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

    # Streamlit UI
    st.markdown("<h1 style='font-size: 36px; text-align: center;'>Customize Your Player</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a close-up picture of your face", type=["jpg", "jpeg", "png"])
    gender = st.selectbox("Select your gender", ["Male", "Female"])
    
    prompt = get_prompt(gender, tv_show)
    st.write(f"Generated prompt: {tv_show}")
    st.write(f"Generated prompt: {prompt}")

    if st.button("Generate Image"):
        if uploaded_file is not None:
            # Clear the directory before saving the new image
            clear_directory(output_dir)
            
            with open("temp.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.write("File uploaded successfully.")
            
            prompt = get_prompt(gender, tv_show)
            st.write(f"Generated prompt: {prompt}")

            try:
                client = Client("multimodalart/Ip-Adapter-FaceID")
                st.write("Client created successfully.")
                
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
                
                st.write("Prediction completed.")
                
                if result and isinstance(result, list) and "image" in result[0]:
                    first_image_path = result[0]["image"]
                    first_image = Image.open(first_image_path)
                    
                    background_removed_image_path = remove_background(first_image_path)
                    background_removed_image = Image.open(background_removed_image_path)
                    
                    save_path = os.path.join(output_dir, "generated_image_no_bg.png")
                    background_removed_image.save(save_path)
                    
                    st.image(background_removed_image, caption="Generated Image with Background Removed")
                    st.write(f"Image saved to {save_path}")

                    # Set the session state variable to True after successful generation
                    st.session_state['image_generated'] = True

                else:
                    st.error("Failed to generate image. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.write(f"Exception details: {e}")
        else:
            st.error("Please upload an image.")

    # Display the "Start" button if the image has been generated
    if st.session_state['image_generated']:
        if st.button("Start"):
            home_url = "http://localhost:8000/index.html"
            st.markdown(f'<meta http-equiv="refresh" content="0; url={home_url}">', unsafe_allow_html=True)
