from pydantic import BaseModel
from typing import Optional
from tavily import TavilyClient
import os

class SearchWebTool(BaseModel):
    query: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def openai_schema(self):
        return {
            "name": "search_web",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }

    def format_results(self, results):
        formatted_text = "Here are the recent news about your query:\n\n"
        for i, result in enumerate(results[:3], 1):  # Only show top 3 results
            formatted_text += f"{i}. {result['title']}\n"
            formatted_text += f"   {result['content'][:200]}...\n\n"
        return formatted_text

    def execute(self, **kwargs):
        self.query = kwargs.get('query')
        
        try:
            client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
            result = client.search(query=self.query)
            
            if 'results' in result:
                return self.format_results(result['results'])
            else:
                return "No results found for your query."
                
        except Exception as e:
            return f"Search error: {str(e)}"