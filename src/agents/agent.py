from typing import List, Dict, Any
from litellm import completion

class Agent:
    def __init__(self, name: str, model: str, tools: List[Any], system_prompt: str):
        self.name = name
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt

    def get_tools_schema(self) -> List[Dict]:
        tool_schemas = []
        for tool in self.tools:
            schema = tool.openai_schema
            # Add name attribute if not present in schema
            if 'name' not in schema:
                schema['name'] = tool.__class__.__name__.lower()
            tool_schemas.append(schema)
        return tool_schemas

    def invoke(self, user_input: str) -> str:
        print(f"\nCalling Agent: {self.name}")
        
        try:
            # Format the messages
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]

            # Get completion from the model
            response = completion(
                model=self.model,
                messages=messages,
                tools=self.get_tools_schema()
            )

            # Process the response
            if hasattr(response, 'choices') and response.choices:
                message = response.choices[0].message
                
                # Check for tool calls
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    tool_call = message.tool_calls[0]
                    tool_name = tool_call.function.name
                    tool_args = tool_call.function.arguments

                    # Find the matching tool
                    for tool in self.tools:
                        if tool.openai_schema['name'] == tool_name:
                            print(f"\nCalling Tool: {tool.__class__.__name__}")
                            print(f"Arguments: {tool_args}")
                            return tool.execute(**eval(tool_args))

                # If no tool calls, return the content
                return message.content if hasattr(message, 'content') else str(message)
            
            return "No response generated"

        except Exception as e:
            print(f"\nError: {str(e)}")
            return f"An error occurred: {str(e)}"