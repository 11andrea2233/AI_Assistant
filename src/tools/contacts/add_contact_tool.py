from pydantic import BaseModel
from typing import Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

class AddContactTool(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def openai_schema(self):
        return {
            "name": "add_contact",
            "description": "Add a new contact to contacts list",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the contact"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number of the contact"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email address of the contact (optional)"
                    }
                },
                "required": ["name", "phone"]
            }
        }

    def execute(self, **kwargs):
        self.name = kwargs.get('name')
        self.phone = kwargs.get('phone')
        self.email = kwargs.get('email', '')
        
        try:
            # Your contact implementation here
            return f"Added contact: {self.name} with phone: {self.phone}"
        except Exception as e:
            return f"Failed to add contact: {str(e)}"