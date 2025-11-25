from sqlalchemy import text
from app.db.session import get_db
from app.models.ticket import AnalysisResult
import logging

logger = logging.getLogger(__name__)

class TicketService:
    async def update_ticket_analysis(self, ticket_id: str, analysis: AnalysisResult):
        """
        Updates the ticket in the database with analysis results.
        """
        query = text("""
            UPDATE tickets 
            SET 
                sentiment = :sentiment,
                intent = :intent,
                urgency_score = :urgency_score,
                category = :category,
                metadata = jsonb_set(COALESCE(metadata, '{}'), '{summary}', to_jsonb(CAST(:summary AS TEXT)), true),
                updated_at = NOW()
            WHERE id = :ticket_id
        """)
        
        # We need to manually manage the session since we're not in a request context
        # This is a bit of a hack for the consumer; normally we'd use dependency injection
        from app.db.session import async_session
        
        async with async_session() as session:
            try:
                await session.execute(query, {
                    "sentiment": analysis.sentiment,
                    "intent": analysis.intent,
                    "urgency_score": analysis.urgency_score,
                    "category": analysis.category,
                    "summary": analysis.summary,
                    "ticket_id": ticket_id
                })
                await session.commit()
                logger.info(f"Updated ticket {ticket_id} with analysis results")
            except Exception as e:
                logger.error(f"Failed to update ticket {ticket_id}: {e}")
                await session.rollback()
                raise e

ticket_service = TicketService()
