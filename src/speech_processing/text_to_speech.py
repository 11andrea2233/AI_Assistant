import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, SpeakOptions
from playsound import playsound
from pathlib import Path

load_dotenv()

class TTS:
    def __init__(self):
        # Create a directory for audio files if it doesn't exist
        self.audio_dir = Path("audio_output")
        self.audio_dir.mkdir(exist_ok=True)
        self.filename = self.audio_dir / "output.wav"
    
    def speak(self, text):
        try:
            # STEP 1: Create a Deepgram client using the API key from environment variables
            deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

            # STEP 2: Configure the options
            options = SpeakOptions(
                model="aura-asteria-en",
                encoding="linear16",
                container="wav"
            )

            # STEP 3: Call the save method on the speak property
            SPEAK_OPTIONS = {"text": text}
            response = deepgram.speak.v("1").save(str(self.filename), SPEAK_OPTIONS, options)

            # STEP 4: Play the audio file
            playsound(str(self.filename))

            # STEP 5: Clean up the file after playing
            try:
                os.remove(self.filename)
            except:
                pass

        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    tts = TTS()
    tts.speak("Hello, how can I help you today?")