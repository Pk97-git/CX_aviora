"""
Slack API integration for notifications and alerts
"""
import httpx
import logging
from typing import Dict, Optional

from app.integrations.base import BaseIntegration

logger = logging.getLogger(__name__)


class SlackIntegration(BaseIntegration):
    """Slack Web API integration"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.bot_token = config.get('bot_token', '')
        self.channel = config.get('channel', '#general')
    
    async def authenticate(self) -> bool:
        """Test Slack bot token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'https://slack.com/api/auth.test',
                    headers={'Authorization': f'Bearer {self.bot_token}'},
                    timeout=10.0
                )
                data = response.json()
                return data.get('ok', False)
        except Exception as e:
            logger.error(f"Slack authentication failed: {e}")
            return False
    
    async def test_connection(self) -> Dict:
        """Test connection and return detailed status"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'https://slack.com/api/auth.test',
                    headers={'Authorization': f'Bearer {self.bot_token}'},
                    timeout=10.0
                )
                data = response.json()
                
                if data.get('ok'):
                    return {
                        'status': 'success',
                        'message': 'Connected to Slack successfully',
                        'team': data.get('team', 'Unknown'),
                        'user': data.get('user', 'Unknown')
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f"Authentication failed: {data.get('error', 'Unknown error')}"
                    }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection failed: {str(e)}'
            }
    
    async def send_notification(self, ticket_data: dict) -> bool:
        """
        Send ticket notification to Slack channel
        
        Args:
            ticket_data: Ticket information including AI insights
            
        Returns:
            True if successful
        """
        try:
            message_blocks = self._format_ticket_message(ticket_data)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'https://slack.com/api/chat.postMessage',
                    headers={'Authorization': f'Bearer {self.bot_token}'},
                    json={
                        'channel': self.channel,
                        'blocks': message_blocks,
                        'text': f"New ticket: {ticket_data.get('title', 'No title')}"  # Fallback text
                    },
                    timeout=15.0
                )
                
                data = response.json()
                success = data.get('ok', False)
                
                if success:
                    logger.info(f"Sent Slack notification for ticket")
                else:
                    logger.error(f"Failed to send Slack notification: {data.get('error')}")
                
                return success
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")
            return False
    
    async def send_alert(self, alert_data: dict) -> bool:
        """
        Send alert notification to Slack
        
        Args:
            alert_data: Alert information
            
        Returns:
            True if successful
        """
        try:
            message_blocks = self._format_alert_message(alert_data)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'https://slack.com/api/chat.postMessage',
                    headers={'Authorization': f'Bearer {self.bot_token}'},
                    json={
                        'channel': self.channel,
                        'blocks': message_blocks,
                        'text': f"Alert: {alert_data.get('title', 'No title')}"
                    },
                    timeout=15.0
                )
                
                data = response.json()
                return data.get('ok', False)
        except Exception as e:
            logger.error(f"Error sending Slack alert: {e}")
            return False
    
    def _format_ticket_message(self, ticket_data: dict) -> list:
        """Format ticket as Slack message blocks"""
        # Sentiment emoji
        sentiment = ticket_data.get('ai_sentiment', 0)
        sentiment_emoji = '😊' if sentiment > 0.3 else '😞' if sentiment < -0.3 else '😐'
        
        # Priority color
        priority = ticket_data.get('priority', 'medium')
        priority_emoji = '🔴' if priority == 'urgent' else '🟠' if priority == 'high' else '🟡' if priority == 'medium' else '🟢'
        
        blocks = [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': f"🎫 New Ticket: {ticket_data.get('title', 'No title')[:100]}"
                }
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f"*Customer:*\n{ticket_data.get('customer_name', 'Unknown')}"
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*Priority:*\n{priority_emoji} {priority.capitalize()}"
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*Category:*\n{ticket_data.get('ai_category', 'Uncategorized').capitalize()}"
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*Sentiment:*\n{sentiment_emoji} {sentiment:.2f}"
                    }
                ]
            }
        ]
        
        # Add AI summary if available
        if ticket_data.get('ai_summary'):
            blocks.append({
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"*AI Summary:*\n{ticket_data['ai_summary']}"
                }
            })
        
        # Add suggested actions if available
        if ticket_data.get('ai_suggested_actions'):
            actions_text = []
            for action in ticket_data['ai_suggested_actions'][:3]:  # Limit to 3
                confidence = action.get('confidence', 0) * 100
                actions_text.append(
                    f"• {action.get('action', 'Unknown')} ({confidence:.0f}% confidence)"
                )
            
            if actions_text:
                blocks.append({
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f"*Suggested Actions:*\n" + '\n'.join(actions_text)
                    }
                })
        
        # Add divider
        blocks.append({'type': 'divider'})
        
        # Add ticket link if available
        ticket_id = ticket_data.get('id')
        if ticket_id:
            blocks.append({
                'type': 'context',
                'elements': [{
                    'type': 'mrkdwn',
                    'text': f"Ticket ID: `{ticket_id}`"
                }]
            })
        
        return blocks
    
    def _format_alert_message(self, alert_data: dict) -> list:
        """Format alert as Slack message blocks"""
        severity = alert_data.get('severity', 'info')
        severity_emoji = '🔴' if severity == 'critical' else '🟠' if severity == 'high' else '🟡' if severity == 'medium' else '🔵'
        
        return [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': f"{severity_emoji} Alert: {alert_data.get('title', 'No title')}"
                }
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': alert_data.get('message', 'No message')
                }
            },
            {
                'type': 'context',
                'elements': [{
                    'type': 'mrkdwn',
                    'text': f"Severity: *{severity.upper()}* | Type: {alert_data.get('type', 'Unknown')}"
                }]
            }
        ]
