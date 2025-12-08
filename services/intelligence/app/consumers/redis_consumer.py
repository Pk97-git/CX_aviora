import asyncio
import json
from app.core.redis import redis_client
from app.services.llm_service import llm_service
from app.services.ticket_service import ticket_service
from app.models.ticket import AnalysisResult
import logging

logger = logging.getLogger(__name__)

class RedisConsumer:
    def __init__(self):
        self.is_running = False

    async def start(self):
        self.is_running = True
        client = await redis_client.get_client()
        pubsub = client.pubsub()
        await pubsub.subscribe("tickets:new")
        
        logger.info("Started listening for tickets:new...")

        while self.is_running:
            try:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    await self.process_message(message)
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in Redis consumer loop: {e}")
                await asyncio.sleep(5) # Backoff on error

    async def stop(self):
        self.is_running = False
        logger.info("Stopping Redis consumer...")

    async def process_message(self, message):
        try:
            # Ingestion service publishes the raw ticket JSON
            ticket_data = json.loads(message["data"])
            
            ticket_id = ticket_data.get("id")
            title = ticket_data.get("title")
            description = ticket_data.get("description")
            
            if not ticket_id or not title:
                logger.warning("Received invalid ticket data")
                return

            logger.info(f"Processing ticket {ticket_id}: {title}")
            
            # Analyze with LLM
            analysis_dict = await llm_service.analyze_ticket({
                "title": title,
                "description": description
            })
            
            analysis_result = AnalysisResult(**analysis_dict)
            
            # Update DB
            await ticket_service.update_ticket_analysis(ticket_id, analysis_result)
                
        except Exception as e:
            logger.error(f"Failed to process message: {e}")

redis_consumer = RedisConsumer()
