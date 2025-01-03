AI Assistant: Your Smart Interactive Partner

Elevate your digital communication with your personalized AI Voice Assistant🎙️🤖

This advanced project features an AI Voice Assistant equipped with Text-to-Speech (TTS) and Speech-to-Text (STT) functions, enabling users to interact with the assistant verbally and receive spoken answers. The assistant leverages a variety of tools to assist with user inquiries, such as handling calendars, managing contacts, composing emails, and executing web searches.

FEATURES:

Speech-to-Text (STT): Convert spoken language into written text.

Text-to-Speech (TTS): Generate vocal responses from text input.

Vocal Interaction: Engage in natural conversations with the AI assistant.

Tool Integration: Utilize built-in tools for calendar management, contact handling, email composition, web searching, and personal knowledge base access.


AVAILABLE TOOLS:

CalendarTool: Schedule events in Google Calendar, including event name, date/time, and an optional description.

AddContactTool: Insert new contact details into Google Contacts, including name, phone number, and optional email.

FetchContactTool: Search for and retrieve details from Google Contacts using the contact’s name.

EmailingTool: Compose and send emails through Gmail with the recipient's name, subject, and message body.

SearchWebTool: Conduct web searches to find current information.

KnowledgeBaseTool: Access personal notes and stored data from the custom knowledge base located in the /files folder.


REQUIREMENTS AND PREREQUISITES:

Python version 3.9 or higher

Google API credentials (for accessing Calendar, Contacts, and Gmail)

Tavily API key (for web searches)

Groq API key (for Llama3)

Google Gemini API key (for the Gemini model)

Deepgram API key (for voice processing)

OpenAI API Key

Essential Python libraries (specified in requirements.txt)


SETUP

1. Clone the repository:

    git clone https://github.com/yourusername/AI_Assistant.git

    cd AI_Assistant

2. Create and activate a virtual environment:

    python -m venv venv

    venv\Scripts\activate

3. Install requirements

    pip install -r requirements.txt

4. Set up environment variables:

Create a .env file in the root directory of the project and add your API keys:

    OPENAI_API_KEY=your_openai_api_key

    GOOGLE_API_KEY=your_google_api_key

    DEEPGRAM_API_KEY=your_deepgram_api_key

    TAVILY_API_KEY=your_tavily_api_key

    GEMINI_API_KEY=your_gemini_api_key

    GROQ_API_KEY=your_groq_api_key

5. Configure Google API credentials:

Refer to Google's guides to configure Calendar, Contacts, and Gmail APIs. Securely store the credentials file and update its path in the configuration.

RUNNING THE APPLICATION

Engage with the assistant:

    python main.py


The assistant is programmed to stop the conversation when the user says "goodbye".

Sample Prompts

    "Schedule a meeting with John tomorrow at 2 PM."
    "Add a new contact: Jane Doe, phone number 555-1234."
    "What is Mary's email?"
    "Send an email to Bob titled 'Project Update'."
    "Look up recent artificial intelligence news online."
    "Remind me of the chocolate chip cookie recipe I saved last week."