import warnings
import asyncio
from litellm import completion
from src.speech_processing.speech_to_text import get_transcript
from src.speech_processing.text_to_speech import TTS
from src.agents.agent import Agent
from src.tools.calendar.calendar_tool import CalendarTool
from src.tools.contacts import AddContactTool, FetchContactTool
from src.tools.emails.emailing_tool import EmailingTool
from src.tools.search import SearchWebTool
from src.prompts.prompts import assistant_prompt
from dotenv import load_dotenv

warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")

load_dotenv()

# Switch to Gemini model
model = "gemini/gemini-1.5-pro"

# Initialize tools
tools_list = [
    CalendarTool(event_name=None, event_datetime=None),
    AddContactTool(name=None, phone=None),
    FetchContactTool(contact_name=None),
    EmailingTool(recipient_name=None, recipient_email=None, subject=None, body=None),
    SearchWebTool(query=None),
]

# Initialize agent
agent = Agent("Assistant Agent", model, tools_list, system_prompt=assistant_prompt)

class ConversationManager:
    def __init__(self, assistant):
        self.transcription_response = ""
        self.assistant = assistant
        self.tts = TTS()

    async def main(self):
        while True:
            await get_transcript(self.handle_full_sentence)
            
            if "goodbye" in self.transcription_response.lower():
                break
            
            try:
                llm_response = self.assistant.invoke(self.transcription_response)
                if llm_response:
                    print(f"AI: {llm_response}")
                    self.tts.speak(llm_response)
            except Exception as e:
                print(f"Error with LLM: {e}")

            self.transcription_response = ""

    def handle_full_sentence(self, full_sentence):
        self.transcription_response = full_sentence

if __name__ == "__main__":
    manager = ConversationManager(agent)
    asyncio.run(manager.main())