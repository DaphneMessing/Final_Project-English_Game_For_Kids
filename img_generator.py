import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image
import os
import glob

# Function to get the prompt based on user inputs
def get_prompt(gender, tv_show):
    gender_str = "girl" if gender == "Female" else "boy"
    character = ""
    if tv_show == "Spidey and his Amazing Friends":
        character = "Spiderman"
    elif tv_show == "PJ Masks":
        character = "PJ Masks"
    elif tv_show == "SpongeBob":
        character = "SpongeBob"
    else:
        character = "Flora from Winx"
    
    return f"A photo of a {gender_str} in a full body costume of {character}, on a plain white background with no other elements"

# Function to remove the background using the Hugging Face Gradio model
def remove_background(image_path):
    client = Client("ECCV2022/dis-background-removal")
    result = client.predict(
        image=handle_file(image_path),
        api_name="/predict"
    )
    
    # The result contains file paths to the generated images
    background_removed_image_path = result[0]  # Path to the image with background removed
    return background_removed_image_path

# Function to clear the existing images in the directory
def clear_directory(directory):
    files = glob.glob(os.path.join(directory, '*'))
    for f in files:
        os.remove(f)

# Ensure the user_img directory exists
output_dir = "user_img"
os.makedirs(output_dir, exist_ok=True)

# Clear the directory before saving the new image
clear_directory(output_dir)

# Streamlit UI
st.markdown("<h1 style='font-size: 36px; text-align: center;'>Learn English With Your Favorite TV Show</h1>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a close-up picture of your face", type=["jpg", "jpeg", "png"])
gender = st.selectbox("Select your gender", ["Male", "Female"])
tv_show = st.selectbox("Select a TV show", ["Spidey and his Amazing Friends", "PJ Masks", "Winx", "SpongeBob"])

if st.button("Generate Image"):
    if uploaded_file is not None:
        with open("temp.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write("File uploaded successfully.")
        
        prompt = get_prompt(gender, tv_show)
        st.write(f"Generated prompt: {prompt}")
        
        try:
            client = Client("multimodalart/Ip-Adapter-FaceID")
            st.write("Client created successfully.")
            
            result = client.predict(
                images=[handle_file("temp.jpg")],    # User uploaded image
                prompt=prompt,                        # Prompt with "no background"
                negative_prompt="",                   # Negative Prompt
                preserve_face_structure=True,         # Preserve Face Structure
                face_strength=1.0,                    # Face Structure Strength
                likeness_strength=1.0,                # Face Embed Strength
                nfaa_negative_prompt="naked, bikini, skimpy, scanty, bare skin, lingerie, swimsuit, exposed, see-through",
                api_name="/generate_image"
            )
            
            st.write("Prediction completed.")
            
            # Display and save only the first image returned in the result
            if result and isinstance(result, list) and "image" in result[0]:
                first_image_path = result[0]["image"]
                first_image = Image.open(first_image_path)
                
                # Remove the background
                background_removed_image_path = remove_background(first_image_path)
                background_removed_image = Image.open(background_removed_image_path)
                
                # Save the image with background removed to the user_img folder
                save_path = os.path.join(output_dir, "generated_image_no_bg.png")
                background_removed_image.save(save_path)
                
                st.image(background_removed_image, caption="Generated Image with Background Removed")
                st.write(f"Image saved to {save_path}")
            else:
                st.error("Failed to generate image. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.write(f"Exception details: {e}")
    else:
        st.error("Please upload an image.")
