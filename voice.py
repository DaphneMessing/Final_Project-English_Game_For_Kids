
import openai
import time
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

openai.api_key = 'sk-proj-5EFH4cZPnydPbqte06PQT3BlbkFJytQlGYnhClqkCuEmqjsI'

# Function to get user's TV show selection
def select_show():
    shows = ["Spongebob", "Cocomelon", "PJ Masks"]
    print("Select one of the following TV shows:")
    for idx, show in enumerate(shows, 1):
        print(f"{idx}. {show}")

    choice = int(input("Enter the number corresponding to your choice: "))
    return shows[choice - 1]

# Function to generate sentence based on show
def generate_sentence(show):
    if show == "Spongebob":
        return "Spongebob traveled on a trip to Bikini Bottom for a long time."
    elif show == "Cocomelon":
        return "Cocomelon traveled on a trip to the park for a long time."
    elif show == "PJ Masks":
        return "PJ Masks traveled on a trip to the city for a long time."

# Function to recognize and verify speech using OpenAI Whisper API
def recognize_speech(expected_sentence):
    samplerate = 44100  # Sample rate of the recording
    duration = 5  # Duration of the recording

    print(f"Please read the sentence: {expected_sentence}")
    input("Type 'start' and press Enter to begin recording... ")

    print("Recording...")

    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished

    audio_data = np.squeeze(audio_data)

    # Save the recording to a WAV file
    wav_file = "speech.wav"
    wav.write(wav_file, samplerate, audio_data)

    with open(wav_file, "rb") as f:
        result = openai.Audio.transcribe("whisper-1", f, language="en")

    transcription = result['text']
    print("You said: ", transcription)
    return transcription.strip().lower() == expected_sentence.strip().lower()

def main():
    show = select_show()
    sentence = generate_sentence(show)
    attempts = 3

    for attempt in range(attempts):
        if recognize_speech(sentence):
            print("Great job! You read the sentence correctly.")
            break
        else:
            print("Let's try again. You have {} attempts left.".format(attempts - attempt - 1))
            time.sleep(1)
    else:
        print("Better luck next time!")

if __name__ == "__main__":
    main()

