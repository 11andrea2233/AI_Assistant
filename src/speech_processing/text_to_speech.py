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
            # Ensure text is a string and not empty
            if not isinstance(text, str) or not text.strip():
                print("Empty or invalid text input")
                return

            # Clean up the text
            text = text.strip()
            
            # Break up long text into chunks (Deepgram has a limit)
            max_chars = 1000
            text_chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
            
            for i, chunk in enumerate(text_chunks):
                # Create unique filename for each chunk
                chunk_file = self.audio_dir / f"output_{i}.wav"
                
                # Initialize Deepgram client
                deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

                # Configure options
                options = SpeakOptions(
                    model="aura-asteria-en",
                    encoding="linear16",
                    container="wav"
                )

                # Generate speech
                SPEAK_OPTIONS = {"text": chunk}
                response = deepgram.speak.v("1").save(str(chunk_file), SPEAK_OPTIONS, options)

                # Play the audio
                playsound(str(chunk_file))

                # Clean up the file
                try:
                    os.remove(chunk_file)
                except:
                    pass

        except Exception as e:
            print(f"TTS Exception: {e}")

if __name__ == "__main__":
    tts = TTS()
    tts.speak("Hello, how can I help you today?")