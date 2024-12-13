# English Learning Game for Kids

### Overview

🎥 [Watch Demo Video](https://drive.google.com/file/d/1HaLKFED6mDRjV987PGKf3qE2RAtHVZdI/view?usp=drive_link)

This interactive game "Littel Talkers" helps children learn English through engaging levels themed around popular TV shows: **SpongeBob**, **PJ Masks**, **Winx Club**, and **Spidey and His Amazing Friends**. Players create a personalized character by uploading a close-up photo, which is transformed into a TV show-inspired avatar using AI. The game features multiple levels, incorporating sentence completion, listening comprehension, and speech practice activities that progressively become more challenging.

### Features

1. **Personalized Character Creation**:
   - Players upload a photo of themselves.
   - The game uses the **IP Adapter FaceID Plus demo** to create an avatar dressed as a character from the selected TV show.

2. **Themed Levels**:
   - **Sentence Completion**: Choose the correct words to complete sentences related to the TV show.
   - **Listening Comprehension**: Listen to pre-recorded sentences (created using Speechify) and type them.
   - **Speech Practice**: Record yourself reading sentences using Python's **sounddevice** library and validate the text with **Whisper AI**.
   - Some levels combine these activities, include time limits, or have other creative challenges.

3. **Dynamic Gameplay**:
   - Levels become progressively harder as the user advances.
   - Earn stars and scores based on performance and mistakes in each level.

4. **Interactive Home Page**:
   - The home page design and game levels are customized based on the selected TV show.

### Technologies Used

- **Backend**:
  - Python for the main logic.
  - Libraries: `streamlit`, `sounddevice`, `whisper`, `Speechify`.
- **Frontend**:
  - HTML/CSS for interactive pages.
  - JavaScript for dynamic elements and local storage handling.
- **AI/ML**:
  - **IP Adapter FaceID Plus demo** for avatar generation.
  - **Whisper AI** for speech-to-text functionality.

### Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/DaphneMessing/Final_Project-English_Game_For_Kids.git
   ```
2. Install the required Python libraries:
   ```bash
   pip install streamlit sounddevice whisper Speechify
   ```
3. Set up OpenAI API Key:
   - Obtain your API key from OpenAI.
   - Open the following files in "pages" subfolder:
      - `Level 2.py`
      - `Level 5.py`
      - `Level 8.py`
      - `Level 11.py`
      - `Level 14.py`
      - `Level 16.py`
   - Add your OpenAI API key to the specified placeholder in these files:
     ```bash
     openai.api_key = "your_openai_api_key_here"
     ```
   - Save the changes.
4. Ensure the following folders and files exist in the project directory:
    - `user_img/`: For storing user-generated avatars.
    - `HomePage/`: Background images for the TV shows.
    - `audio_levelX/`: Audio files for listening comprehension activities.
    - `default_player_img/`: Default character images for each TV show.
    - Pre-loaded audio files, word lists, and level scripts (`Level X.py`).

### How to Run

1. Open the terminal and run the following command to start the image generation service:
   ```bash
   streamlit run img_generator.py --client.showSidebarNavigation=false
   ```
2. In another terminal window, serve the selection page:
   ```bash
   python -m http.server 8000
   ```
3. Open your browser and navigate to:
   ```bash
   http://localhost:8000/SelectionPage.html
   ```
4.  Follow the instructions:
   - Select a TV show and upload a close-up image.
   - Proceed to the home page to start playing the levels.
5. Navigate through the levels, completing tasks and improving your English skills!

### File Structure

- **Python Scripts**:
  - `img_generator.py`: Generates the player avatar.
  - `Level X.py`: Implements the logic for specific levels.
- **HTML Files**:
  - `SelectionPage.html`: TV show selection and image upload.
  - `index.html`: Main game page with level navigation.
- **Assets**:
  - `HomePage/`: Contains TV show background images.
  - `default_player_img/`: Stores default character images.
  - `audio_levelX/`: Holds pre-recorded audio files.
  - `sentences_levelX.txt`: Text for listening comprehension.




   
   
