import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image

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
    
    # Add "no background" to the prompt
    return f"A photo of a {gender_str} dressed up as {character}, no background"

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
            
            # Display only the first image returned in the result
            if result and isinstance(result, list) and "image" in result[0]:
                first_image_path = result[0]["image"]
                first_image = Image.open(first_image_path)
                st.image(first_image, caption="Generated Image")
            else:
                st.error("Failed to generate image. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.write(f"Exception details: {e}")
    else:
        st.error("Please upload an image.")




# import streamlit as st
# from gradio_client import Client, handle_file
# from PIL import Image
# import io  # Import the io module

# # Hugging Face API Client
# client = Client("multimodalart/Ip-Adapter-FaceID")

# def generate_image(uploaded_file, gender):
#     if uploaded_file is not None:
#         # Save the uploaded image to a temporary file
#         image = Image.open(uploaded_file)
#         img_byte_arr = io.BytesIO()
#         image.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()
        
#         # Save image to a temporary file
#         with open("temp.jpg", "wb") as f:
#             f.write(img_byte_arr)

#         # Define the prompt based on gender
#         prompt = f"a closeup picture of a {gender} dressed as Spider-Man"

#         # Call the Gradio API to generate the image
#         result = client.predict(
#             images=[handle_file("temp.jpg")],
#             prompt=prompt,
#             negative_prompt="",
#             preserve_face_structure=True,
#             face_strength=1.0,
#             likeness_strength=1.0,
#             nfaa_negative_prompt="naked, bikini, skimpy, scanty, bare skin, lingerie, swimsuit, exposed, see-through",
#             api_name="/generate_image"
#         )

#         # Display only the first image returned in the result
#         if result and len(result) > 0:
#             image_path = result[0].get('image')
#             if image_path:
#                 generated_image = Image.open(image_path)
#                 st.image(generated_image, caption="Generated Image")
#             else:
#                 st.error("Could not find 'image' in the response.")
#         else:
#             st.error("No images were generated by the API.")

# st.title("Face Swap with Spider-Man Costume")

# # Uploading the image
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# # Gender selection
# gender = st.radio("Select your gender:", ("woman", "man"))

# if st.button("Generate Image"):
#     generate_image(uploaded_file, gender)
