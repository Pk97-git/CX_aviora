"""
Integration package initialization
"""
from app.integrations.base import BaseIntegration
from app.integrations.freshdesk import FreshdeskIntegration
from app.integrations.jira import JiraIntegration
from app.integrations.slack import SlackIntegration

__all__ = [
    'BaseIntegration',
    'FreshdeskIntegration',
    'JiraIntegration',
    'SlackIntegration'
]
