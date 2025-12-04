"""
AI-powered ticket understanding service using Groq
"""
import json
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel
from groq import Groq

logger = logging.getLogger(__name__)


class TicketAnalysis(BaseModel):
    """AI analysis results for a ticket"""
    summary: str
    intent: str
    entities: Dict
    sentiment: float
    priority: str
    category: str
    suggested_actions: List[Dict]


class TicketUnderstandingService:
    """Service for AI-powered ticket analysis"""
    
    def __init__(self, groq_api_key: str):
        self.client = Groq(api_key=groq_api_key)
        self.model = "llama-3.1-70b-versatile"
    
    async def analyze_ticket(self, title: str, description: Optional[str] = None) -> TicketAnalysis:
        """
        Analyze a ticket using LLM to extract insights
        
        Args:
            title: Ticket title/subject
            description: Ticket description/body
            
        Returns:
            TicketAnalysis with AI-generated insights
        """
        full_text = f"{title}\n\n{description or ''}"
        
        prompt = f"""Analyze this customer support ticket and provide structured insights.

Ticket Title: {title}
Ticket Description: {description or 'No description provided'}

Provide analysis in JSON format with these fields:
{{
  "summary": "Brief 1-2 sentence summary of the issue",
  "intent": "Primary intent - choose from: refund_request, bug_report, feature_request, account_issue, billing_question, technical_support, shipping_issue, product_inquiry, complaint, feedback",
  "entities": {{"order_id": "value", "amount": 123.45, "product": "value", "date": "value", etc.}},
  "sentiment": 0.5,  // Range: -1.0 (very negative) to 1.0 (very positive)
  "priority": "low|medium|high|urgent",
  "category": "billing|technical|account|shipping|product|sales|other",
  "suggested_actions": [{{"action": "specific_action", "confidence": 0.95, "reason": "why this action"}}]
}}

Extract as many relevant entities as possible (order IDs, amounts, dates, products, etc.).
Be accurate with sentiment analysis based on tone and urgency.
Suggest practical actions that would help resolve the issue.

Return ONLY valid JSON, no markdown formatting or explanation."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            
            # Parse JSON response
            result = json.loads(result_text)
            
            return TicketAnalysis(**result)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            logger.error(f"Response text: {result_text}")
            
            # Fallback to basic analysis
            return self._fallback_analysis(title, description)
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._fallback_analysis(title, description)
    
    def _fallback_analysis(self, title: str, description: Optional[str]) -> TicketAnalysis:
        """Fallback analysis when AI fails"""
        return TicketAnalysis(
            summary=title[:200] if title else "No summary available",
            intent="unknown",
            entities={},
            sentiment=0.0,
            priority="medium",
            category="other",
            suggested_actions=[]
        )
