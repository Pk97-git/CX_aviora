"""
JIRA API integration for issue creation and tracking
"""
import httpx
import logging
from typing import Dict, Optional

from app.integrations.base import BaseIntegration

logger = logging.getLogger(__name__)


class JiraIntegration(BaseIntegration):
    """JIRA Cloud API v3 integration"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.domain = config.get('domain', '').replace('https://', '').replace('http://', '')
        self.email = config.get('email', '')
        self.api_token = config.get('api_token', '')
        self.project_key = config.get('project_key', '')
        self.base_url = f"https://{self.domain}/rest/api/3"
    
    async def authenticate(self) -> bool:
        """Test JIRA credentials"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/myself",
                    auth=(self.email, self.api_token),
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"JIRA authentication failed: {e}")
            return False
    
    async def test_connection(self) -> Dict:
        """Test connection and return detailed status"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/myself",
                    auth=(self.email, self.api_token),
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    return {
                        'status': 'success',
                        'message': 'Connected to JIRA successfully',
                        'domain': self.domain,
                        'user': user_data.get('displayName', 'Unknown')
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
    
    async def create_issue(self, ticket_data: dict) -> Optional[str]:
        """
        Create JIRA issue from ticket
        
        Args:
            ticket_data: Ticket information
            
        Returns:
            JIRA issue key (e.g., 'PROJ-123') if successful
        """
        try:
            # Build description in Atlassian Document Format
            description_text = ticket_data.get('description', 'No description provided')
            
            # Add AI insights to description
            ai_summary = ticket_data.get('ai_summary')
            if ai_summary:
                description_text = f"*AI Summary:* {ai_summary}\n\n{description_text}"
            
            payload = {
                'fields': {
                    'project': {'key': self.project_key},
                    'summary': ticket_data.get('title', 'No title'),
                    'description': {
                        'type': 'doc',
                        'version': 1,
                        'content': [{
                            'type': 'paragraph',
                            'content': [{
                                'type': 'text',
                                'text': description_text
                            }]
                        }]
                    },
                    'issuetype': {'name': 'Task'},  # or 'Bug', 'Story', etc.
                }
            }
            
            # Add priority if available
            priority = ticket_data.get('priority') or ticket_data.get('ai_priority')
            if priority:
                jira_priority = self._map_priority_to_jira(priority)
                payload['fields']['priority'] = {'name': jira_priority}
            
            # Add labels
            labels = []
            if ticket_data.get('ai_category'):
                labels.append(ticket_data['ai_category'])
            if ticket_data.get('ai_intent'):
                labels.append(ticket_data['ai_intent'])
            if labels:
                payload['fields']['labels'] = labels
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/issue",
                    auth=(self.email, self.api_token),
                    json=payload,
                    timeout=15.0
                )
                
                if response.status_code == 201:
                    issue_key = response.json()['key']
                    logger.info(f"Created JIRA issue: {issue_key}")
                    return issue_key
                else:
                    logger.error(f"Failed to create JIRA issue: {response.text}")
                    return None
        except Exception as e:
            logger.error(f"Error creating JIRA issue: {e}")
            return None
    
    async def add_comment(self, issue_key: str, comment: str, is_internal: bool = False) -> bool:
        """Add comment to JIRA issue"""
        try:
            payload = {
                'body': {
                    'type': 'doc',
                    'version': 1,
                    'content': [{
                        'type': 'paragraph',
                        'content': [{
                            'type': 'text',
                            'text': comment
                        }]
                    }]
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/issue/{issue_key}/comment",
                    auth=(self.email, self.api_token),
                    json=payload,
                    timeout=15.0
                )
                
                success = response.status_code == 201
                if success:
                    logger.info(f"Added comment to JIRA issue {issue_key}")
                else:
                    logger.error(f"Failed to add comment: {response.text}")
                return success
        except Exception as e:
            logger.error(f"Error adding comment to JIRA: {e}")
            return False
    
    async def update_issue_status(self, issue_key: str, status: str) -> bool:
        """Transition JIRA issue to new status"""
        try:
            # Get available transitions
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/issue/{issue_key}/transitions",
                    auth=(self.email, self.api_token),
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    return False
                
                transitions = response.json()['transitions']
                
                # Find matching transition
                target_transition = None
                status_lower = status.lower()
                for transition in transitions:
                    if transition['name'].lower() == status_lower:
                        target_transition = transition['id']
                        break
                
                if not target_transition:
                    logger.warning(f"No matching transition found for status: {status}")
                    return False
                
                # Execute transition
                response = await client.post(
                    f"{self.base_url}/issue/{issue_key}/transitions",
                    auth=(self.email, self.api_token),
                    json={'transition': {'id': target_transition}},
                    timeout=15.0
                )
                
                success = response.status_code == 204
                if success:
                    logger.info(f"Updated JIRA issue {issue_key} status to {status}")
                return success
        except Exception as e:
            logger.error(f"Error updating JIRA issue status: {e}")
            return False
    
    def _map_priority_to_jira(self, priority: str) -> str:
        """Map our priority to JIRA priority names"""
        mapping = {
            'low': 'Low',
            'medium': 'Medium',
            'high': 'High',
            'urgent': 'Highest'
        }
        return mapping.get(priority.lower(), 'Medium')
