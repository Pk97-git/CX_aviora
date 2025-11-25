import json
from groq import AsyncGroq
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class LLMService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = "llama3-70b-8192" # Or "mixtral-8x7b-32768"

    async def analyze_ticket(self, ticket_data: dict) -> dict:
        """
        Analyzes the ticket content to extract sentiment, intent, urgency, and category.
        """
        subject = ticket_data.get("title", "")
        description = ticket_data.get("description", "")
        
        prompt = f"""
        You are an expert customer support AI. Analyze the following support ticket and extract structured insights.
        
        Ticket Subject: {subject}
        Ticket Description: {description}
        
        Return the result in strict JSON format with the following keys:
        - sentiment: "Positive", "Neutral", or "Negative"
        - intent: One of ["Refund", "Technical Support", "Feature Request", "Billing", "Account Access", "General Inquiry"]
        - urgency_score: An integer from 1 (Low) to 10 (Critical)
        - category: A short 1-3 word category describing the issue (e.g., "Login Issue", "Payment Failure")
        - summary: A one-sentence summary of the issue.
        
        JSON Output:
        """

        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that outputs strictly valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            response_content = chat_completion.choices[0].message.content
            return json.loads(response_content)

        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            # Return default/fallback values on error
            return {
                "sentiment": "Neutral",
                "intent": "General Inquiry",
                "urgency_score": 5,
                "category": "Uncategorized",
                "summary": "Analysis failed"
            }

llm_service = LLMService()
