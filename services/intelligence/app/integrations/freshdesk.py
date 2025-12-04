"""
Freshdesk API integration for bidirectional ticket sync
"""
import httpx
import logging
from typing import List, Dict, Optional
from datetime import datetime

from app.integrations.base import BaseIntegration

logger = logging.getLogger(__name__)


class FreshdeskIntegration(BaseIntegration):
    """Freshdesk API v2 integration"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.domain = config.get('domain', '').replace('https://', '').replace('http://', '')
        self.api_key = config.get('api_key', '')
        self.base_url = f"https://{self.domain}/api/v2"
    
    async def authenticate(self) -> bool:
        """Test Freshdesk API key validity"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/tickets",
                    auth=(self.api_key, 'X'),
                    params={'per_page': 1},
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Freshdesk authentication failed: {e}")
            return False
    
    async def test_connection(self) -> Dict:
        """Test connection and return detailed status"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/tickets",
                    auth=(self.api_key, 'X'),
                    params={'per_page': 1},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return {
                        'status': 'success',
                        'message': 'Connected to Freshdesk successfully',
                        'domain': self.domain
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f'Authentication failed: {response.status_code}',
                        'details': response.text
                    }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection failed: {str(e)}'
            }
    
    async def sync_tickets(self, since: Optional[datetime] = None) -> List[Dict]:
        """Fetch tickets from Freshdesk"""
        try:
            params = {
                'per_page': 100,
                'order_by': 'updated_at',
                'order_type': 'desc'
            }
            
            if since:
                params['updated_since'] = since.isoformat()
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/tickets",
                    auth=(self.api_key, 'X'),
                    params=params,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    tickets = response.json()
                    logger.info(f"Fetched {len(tickets)} tickets from Freshdesk")
                    return tickets
                else:
                    logger.error(f"Failed to fetch tickets: {response.status_code}")
                    return []
        except Exception as e:
            logger.error(f"Error syncing Freshdesk tickets: {e}")
            return []
    
    async def create_ticket(self, ticket_data: dict) -> Optional[str]:
        """Create ticket in Freshdesk"""
        try:
            payload = {
                'subject': ticket_data.get('title', 'No subject'),
                'description': ticket_data.get('description', ''),
                'email': ticket_data.get('customer_email'),
                'priority': self._map_priority_to_freshdesk(ticket_data.get('priority')),
                'status': self._map_status_to_freshdesk(ticket_data.get('status', 'open'))
            }
            
            # Add custom fields if available
            if ticket_data.get('ai_category'):
                payload['custom_fields'] = {
                    'ai_category': ticket_data['ai_category']
                }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/tickets",
                    auth=(self.api_key, 'X'),
                    json=payload,
                    timeout=15.0
                )
                
                if response.status_code == 201:
                    ticket_id = str(response.json()['id'])
                    logger.info(f"Created Freshdesk ticket: {ticket_id}")
                    return ticket_id
                else:
                    logger.error(f"Failed to create ticket: {response.text}")
                    return None
        except Exception as e:
            logger.error(f"Error creating Freshdesk ticket: {e}")
            return None
    
    async def update_ticket(self, external_id: str, updates: dict) -> bool:
        """Update ticket in Freshdesk"""
        try:
            freshdesk_updates = {}
            
            if 'status' in updates:
                freshdesk_updates['status'] = self._map_status_to_freshdesk(updates['status'])
            if 'priority' in updates:
                freshdesk_updates['priority'] = self._map_priority_to_freshdesk(updates['priority'])
            
            if not freshdesk_updates:
                return True  # Nothing to update
            
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.base_url}/tickets/{external_id}",
                    auth=(self.api_key, 'X'),
                    json=freshdesk_updates,
                    timeout=15.0
                )
                
                success = response.status_code == 200
                if success:
                    logger.info(f"Updated Freshdesk ticket {external_id}")
                else:
                    logger.error(f"Failed to update ticket: {response.text}")
                return success
        except Exception as e:
            logger.error(f"Error updating Freshdesk ticket: {e}")
            return False
    
    async def add_comment(self, external_id: str, comment: str, is_internal: bool = False) -> bool:
        """Add comment/note to Freshdesk ticket"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/tickets/{external_id}/notes",
                    auth=(self.api_key, 'X'),
                    json={
                        'body': comment,
                        'private': is_internal
                    },
                    timeout=15.0
                )
                
                success = response.status_code == 201
                if success:
                    logger.info(f"Added comment to Freshdesk ticket {external_id}")
                else:
                    logger.error(f"Failed to add comment: {response.text}")
                return success
        except Exception as e:
            logger.error(f"Error adding comment to Freshdesk: {e}")
            return False
    
    def _map_status_to_freshdesk(self, status: str) -> int:
        """Map our status to Freshdesk status codes"""
        mapping = {
            'open': 2,
            'pending': 3,
            'resolved': 4,
            'closed': 5
        }
        return mapping.get(status, 2)
    
    def _map_priority_to_freshdesk(self, priority: Optional[str]) -> int:
        """Map our priority to Freshdesk priority codes"""
        if not priority:
            return 2
        mapping = {
            'low': 1,
            'medium': 2,
            'high': 3,
            'urgent': 4
        }
        return mapping.get(priority.lower(), 2)
    
    def _map_freshdesk_status_to_ours(self, status: int) -> str:
        """Map Freshdesk status code to our status"""
        mapping = {
            2: 'open',
            3: 'pending',
            4: 'resolved',
            5: 'closed'
        }
        return mapping.get(status, 'open')
    
    def _map_freshdesk_priority_to_ours(self, priority: int) -> str:
        """Map Freshdesk priority code to our priority"""
        mapping = {
            1: 'low',
            2: 'medium',
            3: 'high',
            4: 'urgent'
        }
        return mapping.get(priority, 'medium')
