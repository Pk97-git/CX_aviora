"""
Base integration class for all external system integrations
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime


class BaseIntegration(ABC):
    """Abstract base class for all integrations"""
    
    def __init__(self, config: dict):
        """
        Initialize integration with configuration
        
        Args:
            config: Integration configuration (API keys, URLs, etc.)
        """
        self.config = config
    
    @abstractmethod
    async def authenticate(self) -> bool:
        """
        Test authentication with the external system
        
        Returns:
            True if authentication successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def test_connection(self) -> Dict:
        """
        Test connection and return status information
        
        Returns:
            Dict with status, message, and any additional info
        """
        pass
    
    # Optional methods - not all integrations need all features
    async def sync_tickets(self, since: Optional[datetime] = None) -> List[Dict]:
        """
        Fetch tickets from external system (optional)
        
        Args:
            since: Only fetch tickets updated since this datetime
            
        Returns:
            List of ticket dictionaries
        """
        return []
    
    async def create_ticket(self, ticket_data: dict) -> Optional[str]:
        """
        Create ticket in external system (optional)
        
        Args:
            ticket_data: Ticket information
            
        Returns:
            External ticket ID if successful, None otherwise
        """
        return None
    
    async def update_ticket(self, external_id: str, updates: dict) -> bool:
        """
        Update ticket in external system (optional)
        
        Args:
            external_id: External system's ticket ID
            updates: Fields to update
            
        Returns:
            True if successful, False otherwise
        """
        return False
    
    async def add_comment(self, external_id: str, comment: str, is_internal: bool = False) -> bool:
        """
        Add comment to ticket in external system (optional)
        
        Args:
            external_id: External system's ticket ID
            comment: Comment text
            is_internal: Whether comment is internal/private
            
        Returns:
            True if successful, False otherwise
        """
        return False
    
    async def register_webhook(self, webhook_url: str, events: List[str]) -> bool:
        """
        Register webhook with external system (optional)
        
        Args:
            webhook_url: URL to receive webhooks
            events: List of events to subscribe to
            
        Returns:
            True if successful, False otherwise
        """
        return False
