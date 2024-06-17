import streamlit as st
from gradio_client import Client

# Function to get the prompt based on user inputs
def get_prompt(gender, tv_show):
    gender_str = "girl" if gender == "Female" else "boy"
    if tv_show == "Spidey and his Amazing Friends":
        character = "Spiderman"
    elif tv_show == "PJ Masks":
        character = "PJ Masks"

    elif tv_show == "SpongeBob":
        character = "SpongeBob"
    else:
        character = "Flora from Winx"
    return f"A photo of a {gender_str} dressed up as {character}"

# Streamlit UI
st.markdown("<h1 style='font-size: 36px; text-align: center;'>Learn English With Your Favorite TV Show</h1>", unsafe_allow_html=True)
# st.title("Learn English With Your Favorite Tv Show")
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
            client = Client("https://multimodalart-ip-adapter-faceid.hf.space/--replicas/l3rst/")
            st.write("Client created successfully.")
            
            # Log the request data
            st.write("Sending the following data to the API:")
            st.write({
                "image_path": "temp.jpg",
                "prompt": prompt,
                "negative_prompt": "",
                "preserve_face_structure": True,
                "face_structure_strength": 0,
                "face_embed_strength": 0,
                "appended_negative_prompts": ""
            })
            
            result = client.predict(
                ["temp.jpg"],    # User uploaded image
                prompt,          # Prompt
                "",              # Negative Prompt
                True,            # Preserve Face Structure
                0,               # Face Structure Strength
                0,               # Face Embed Strength
                "",              # Appended Negative Prompts
                api_name="/generate_image"
            )
            
            st.write("Prediction completed.")
            st.write(f"Raw result: {result}")
            
            if result and isinstance(result, list) and all("image" in item for item in result):
                st.write("Generated Images:")
                for image_info in result:
                    st.image(image_info["image"], caption="Generated Image")
            else:
                st.error("Failed to generate image. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.write(f"Exception details: {e}")
    else:
        st.error("Please upload an image.")
