import warnings
import asyncio
import time
from litellm import RateLimitError
from src.speech_processing.speech_to_text import get_transcript
from src.speech_processing.text_to_speech import TTS
from src.agents.agent import Agent
from src.tools.calendar.calendar_tool import CalendarTool
from src.tools.contacts import AddContactTool, FetchContactTool
from src.tools.emails.emailing_tool import EmailingTool
from src.tools.search import SearchWebTool
from src.prompts.prompts import assistant_prompt
from dotenv import load_dotenv

load_dotenv()


model = "gpt-3.5-turbo"  # OpenAI (faster, cheaper)


# agent tools
tools_list = [
    CalendarTool,
    AddContactTool,
    FetchContactTool,
    EmailingTool,
    SearchWebTool,
    # KnowledgeSearchTool
]

# Initiate the sale agent
agent = Agent("Assistant Agent", model, tools_list, system_prompt=assistant_prompt)

async def retry_with_backoff(func, max_retries=3, initial_delay=1):
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return await func()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait_time = float(str(e).split("try again in ")[1].split("s")[0])
            print(f"Rate limit hit, waiting {wait_time} seconds...")
            await asyncio.sleep(wait_time)
    return None

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
            
            # Wrap the LLM call in retry logic
            llm_response = await retry_with_backoff(
                lambda: self.assistant.invoke(self.transcription_response)
            )
            
            if llm_response:
                print(f"AI: {llm_response}")
                self.tts.speak(llm_response)

            self.transcription_response = ""

    def handle_full_sentence(self, full_sentence):
        self.transcription_response = full_sentence

if __name__ == "__main__":
    manager = ConversationManager(agent)
    asyncio.run(manager.main())