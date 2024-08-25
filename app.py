from flask import Flask, request, render_template, jsonify, send_from_directory
from gradio_client import Client, handle_file
from PIL import Image
import os
import glob

app = Flask(__name__)

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
    
    return f"A full body photo of a {gender_str} dressed in a complete {character} costume, showing the entire body from head to toe, including the legs, on a plain white background with no other elements"

# Function to remove the background using the Hugging Face Gradio model
def remove_background(image_path):
    client = Client("ECCV2022/dis-background-removal")
    result = client.predict(
        image=handle_file(image_path),
        api_name="/predict"
    )
    
    background_removed_image_path = result[0]
    return background_removed_image_path

# Function to clear the existing images in the directory
def clear_directory(directory):
    files = glob.glob(os.path.join(directory, '*'))
    for f in files:
        os.remove(f)

# Ensure the user_img directory exists
output_dir = "user_img"
os.makedirs(output_dir, exist_ok=True)

@app.route('/')
def index():
    return render_template('gen_img.html')  # Use gen_img.html

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Clear the directory before saving the new image
        clear_directory(output_dir)

        # Save the uploaded image
        uploaded_file = request.files['file']
        gender = request.form['gender']
        tv_show = request.form['tv_show']
        temp_image_path = os.path.join(output_dir, "temp.jpg")
        uploaded_file.save(temp_image_path)
        
        # Generate the image using the prompt
        prompt = get_prompt(gender, tv_show)
        client = Client("multimodalart/Ip-Adapter-FaceID")
        result = client.predict(
            images=[handle_file(temp_image_path)],
            prompt=prompt,
            negative_prompt="",
            preserve_face_structure=True,
            face_strength=1.0,
            likeness_strength=1.0,
            nfaa_negative_prompt="naked, bikini, skimpy, scanty, bare skin, lingerie, swimsuit, exposed, see-through",
            api_name="/generate_image"
        )
        
        if result and isinstance(result, list) and "image" in result[0]:
            generated_image_path = result[0]["image"]
            
            # Remove the background
            background_removed_image_path = remove_background(generated_image_path)
            background_removed_image = Image.open(background_removed_image_path)
            
            # Save the final image
            save_path = os.path.join(output_dir, "generated_image_no_bg.png")
            background_removed_image.save(save_path)
            
            return jsonify({"success": True, "image_url": f"/user_img/{os.path.basename(save_path)}"})
        else:
            return jsonify({"success": False, "error": "Failed to generate image."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/user_img/<filename>')
def get_image(filename):
    return send_from_directory(output_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
