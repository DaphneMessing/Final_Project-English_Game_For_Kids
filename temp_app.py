# from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# import os

# app = Flask(__name__)

# # Directories for user images and backgrounds
# UPLOAD_FOLDER = 'user_img'
# HOMEPAGE_FOLDER = 'HomePage'

# # Ensure directories exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/')
# def select_tv_show():
#     return render_template('SelectionPage.html')

# @app.route('/index')
# def game_index():
#     tv_show = request.args.get('tv_show')
#     if not tv_show:
#         return redirect(url_for('select_tv_show'))
    
#     # Pass the tv_show to the template
#     return render_template('index.html', tv_show=tv_show)

# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return redirect(url_for('select_tv_show'))

#     file = request.files['file']
#     gender = request.form.get('gender')
#     tv_show = request.form.get('tv_show')

#     if file.filename == '':
#         return redirect(url_for('select_tv_show'))

#     if file and gender and tv_show:
#         # Save the file in the specified directory
#         file_path = os.path.join(UPLOAD_FOLDER, 'generated_image_no_bg.png')
#         file.save(file_path)

#         # Optionally process the image here (e.g., face swap, filters)

#         return redirect(url_for('game_index', tv_show=tv_show))

#     return redirect(url_for('select_tv_show'))

# @app.route('/homepage/<path:filename>')
# def serve_homepage_file(filename):
#     return send_from_directory(HOMEPAGE_FOLDER, filename)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template, jsonify, send_from_directory, redirect, url_for
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
    return render_template('gen_img.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        print("Received POST request at /generate")  # Debugging line
        print("Form data:", request.form)  # Debugging line

        # Clear the directory before saving the new image
        clear_directory(output_dir)

        # Save the uploaded image
        uploaded_file = request.files['file']
        gender = request.form['gender']
        tv_show = request.form['tv_show']
        print(f"Gender: {gender}, TV Show: {tv_show}")  # Debugging line

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
            
            print("Image generated and saved, redirecting to game screen...")  # Debugging line
            # Redirect to the game screen
            return redirect(url_for('game_index', tv_show=tv_show))
        else:
            return jsonify({"success": False, "error": "Failed to generate image."})
    except Exception as e:
        print("Error during image generation:", str(e))  # Debugging line
        return jsonify({"success": False, "error": str(e)})

@app.route('/index')
def game_index():
    tv_show = request.args.get('tv_show')
    if not tv_show:
        return redirect(url_for('index'))
    
    # Pass the tv_show to the template
    return render_template('index.html', tv_show=tv_show)

@app.route('/user_img/<filename>')
def get_image(filename):
    return send_from_directory(output_dir, filename)

# Test route for debugging
@app.route('/test', methods=['POST'])
def test_route():
    print("Test route hit!")
    return "Test route successful!"

@app.route('/test_form')
def test_form():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
