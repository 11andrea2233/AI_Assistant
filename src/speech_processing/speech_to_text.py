import asyncio
from dotenv import load_dotenv
import os
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone
)

# Load environment variables from a .env file
load_dotenv()

class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        # Initialize or reset the transcript parts list
        self.transcript_parts = []

    def add_part(self, part):
        # Add a part of the transcript to the list
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        # Join all parts of the transcript into a single string
        return ' '.join(self.transcript_parts)

# Global variable to store the transcription response
transcription_response = ""

def handle_full_sentence(full_sentence):
    global transcription_response
    transcription_response = full_sentence

async def get_transcript(callback):
    transcript_collector = TranscriptCollector()
    transcription_complete = asyncio.Event()

    try:
        # Get API key from environment
        api_key = os.getenv('DEEPGRAM_API_KEY')
        if not api_key:
            raise ValueError("Deepgram API key not found!")

        # Configure Deepgram client with keepalive
        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram = DeepgramClient(api_key, config)

        # Create connection
        dg_connection = deepgram.listen.asyncwebsocket.v("1")

        print("\nListening... (Speak into your microphone)")

        async def on_message(self, result, **kwargs):
            try:
                sentence = result.channel.alternatives[0].transcript
                
                if sentence.strip():  # Only process non-empty transcripts
                    if not result.speech_final:
                        transcript_collector.add_part(sentence)
                    else:
                        transcript_collector.add_part(sentence)
                        full_sentence = transcript_collector.get_full_transcript()
                        if full_sentence.strip():
                            print(f"\nYou said: {full_sentence}")
                            callback(full_sentence)
                            transcript_collector.reset()
                            transcription_complete.set()
            except Exception as e:
                print(f"Error in message handling: {e}")

        # Set up event handlers
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        # Configure transcription options
        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            endpointing=300,
            smart_format=True,
        )

        # Start connection and microphone
        await dg_connection.start(options)
        microphone = Microphone(dg_connection.send)

        try:
            print("Microphone activated. Start speaking...")
            microphone.start()
            await transcription_complete.wait()
        except Exception as e:
            print(f"Microphone error: {e}")
        finally:
            print("Stopping microphone...")
            microphone.finish()
            await dg_connection.finish()

    except Exception as e:
        print(f"Setup error: {e}")
    finally:
        # Ensure everything is cleaned up
        if 'microphone' in locals():
            microphone.finish()
        if 'dg_connection' in locals():
            await dg_connection.finish()

if __name__ == "__main__":
    # Run the get_transcript function and pass handle_full_sentence as the callback
    asyncio.run(get_transcript(handle_full_sentence))