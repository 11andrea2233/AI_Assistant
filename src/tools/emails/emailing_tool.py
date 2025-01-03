from pydantic import BaseModel
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailingTool(BaseModel):
    recipient_name: Optional[str] = None
    recipient_email: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def openai_schema(self):
        return {
            "name": "send_email",
            "description": "Send an email to a recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient_name": {
                        "type": "string",
                        "description": "Name of the recipient"
                    },
                    "recipient_email": {
                        "type": "string",
                        "description": "Email address of the recipient"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject of the email"
                    },
                    "body": {
                        "type": "string",
                        "description": "Body content of the email"
                    }
                },
                "required": ["recipient_name", "recipient_email", "subject", "body"]
            }
        }

    def execute(self, **kwargs):
        self.recipient_name = kwargs.get('recipient_name')
        self.recipient_email = kwargs.get('recipient_email')
        self.subject = kwargs.get('subject')
        self.body = kwargs.get('body')
        
        try:
            # Your email sending implementation here
            return f"Email sent to {self.recipient_name} ({self.recipient_email})"
        except Exception as e:
            return f"Failed to send email: {str(e)}"