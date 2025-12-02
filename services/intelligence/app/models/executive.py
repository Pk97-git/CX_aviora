"""
Financial metrics and executive dashboard models.
"""
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Boolean, DECIMAL, Text
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.models.database import Base


class FinancialMetric(Base):
    """Daily financial impact metrics"""
    __tablename__ = "financial_metrics"

    id = Column(String, primary_key=True)  # UUID
    date = Column(Date, nullable=False, unique=True)
    
    # Revenue Protection
    churn_prevented_count = Column(Integer, default=0)
    revenue_protected = Column(DECIMAL(12, 2), default=0)
    
    # Cost Savings
    automation_cost_saved = Column(DECIMAL(12, 2), default=0)
    resolution_time_saved_hours = Column(Float, default=0)
    
    # Efficiency Gains
    friction_cost_reduced = Column(DECIMAL(12, 2), default=0)
    sla_compliance_bonus = Column(DECIMAL(12, 2), default=0)
    
    # Totals
    total_value_generated = Column(DECIMAL(12, 2), default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ROICalculation(Base):
    """ROI calculations for specific periods"""
    __tablename__ = "roi_calculations"

    id = Column(String, primary_key=True)  # UUID
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    total_investment = Column(DECIMAL(12, 2))
    total_return = Column(DECIMAL(12, 2))
    roi_percentage = Column(Float)
    
    breakdown = Column(JSONB)  # Detailed breakdown of sources
    
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AlertRule(Base):
    """Alert rule configurations"""
    __tablename__ = "alert_rules"

    id = Column(String, primary_key=True)  # UUID
    name = Column(String(255), nullable=False)
    metric_type = Column(String(50), nullable=False)  # 'sla_breach', 'churn_risk', 'sentiment_drop'
    threshold_value = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)  # 'critical', 'high', 'medium', 'low'
    notification_channels = Column(JSONB)  # ['email', 'slack', 'webhook']
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Alert(Base):
    """Alert history and tracking"""
    __tablename__ = "alerts"

    id = Column(String, primary_key=True)  # UUID
    rule_id = Column(String)  # References alert_rules
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    metric_value = Column(Float)
    triggered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    acknowledged_at = Column(DateTime)
    acknowledged_by = Column(String(255))


class SavedReport(Base):
    """Saved report configurations"""
    __tablename__ = "saved_reports"

    id = Column(String, primary_key=True)  # UUID
    name = Column(String(255), nullable=False)
    description = Column(Text)
    report_type = Column(String(50), nullable=False)  # 'dashboard', 'analytics', 'custom'
    
    # Configuration
    config = Column(JSONB, nullable=False)  # Chart types, metrics, filters
    
    # Scheduling
    schedule_enabled = Column(Boolean, default=False)
    schedule_frequency = Column(String(20))  # 'daily', 'weekly', 'monthly'
    schedule_day_of_week = Column(Integer)  # 0-6 for weekly
    schedule_day_of_month = Column(Integer)  # 1-31 for monthly
    schedule_time = Column(String(5))  # HH:MM format
    
    # Recipients
    recipients = Column(JSONB)  # ['email1@example.com', 'email2@example.com']
    
    # Metadata
    created_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_sent_at = Column(DateTime)


class ReportDelivery(Base):
    """Report delivery history"""
    __tablename__ = "report_deliveries"

    id = Column(String, primary_key=True)  # UUID
    report_id = Column(String)  # References saved_reports
    delivered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    delivery_status = Column(String(20))  # 'success', 'failed'
    recipient_count = Column(Integer)
    file_size_bytes = Column(Integer)
    error_message = Column(Text)
