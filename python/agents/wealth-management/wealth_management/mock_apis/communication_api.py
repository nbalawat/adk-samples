"""Mock Communication API for client outreach and emergency communications"""

import os
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from .base_api import BaseMockAPI, APIResponse

class CommunicationType(Enum):
    EMAIL = "email"
    PHONE = "phone"
    SMS = "sms"
    PORTAL_MESSAGE = "portal_message"
    LETTER = "letter"

class UrgencyLevel(Enum):
    LOW = "low"
    MODERATE = "moderate" 
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class CommunicationTemplate:
    """Communication template structure"""
    template_id: str
    name: str
    type: CommunicationType
    subject_line: str
    content: str
    target_audience: str
    urgency: UrgencyLevel
    approval_required: bool

@dataclass
class OutreachCampaign:
    """Outreach campaign structure"""
    campaign_id: str
    name: str
    trigger_event: str
    target_segments: List[str]
    communication_methods: List[CommunicationType]
    timeline: str
    status: str
    created_timestamp: datetime
    estimated_reach: int

class MockCommunicationAPI(BaseMockAPI):
    """Mock communication API for client outreach management"""
    
    def __init__(self):
        super().__init__("communication_api")
        self._initialize_templates()
        self._initialize_campaigns()
        self._message_log = []
    
    def _initialize_templates(self):
        """Initialize communication templates"""
        self._templates = {
            "MARKET_VOLATILITY_CONSERVATIVE": CommunicationTemplate(
                template_id="TMPL_001",
                name="Market Volatility - Conservative Clients",
                type=CommunicationType.EMAIL,
                subject_line="Market Update: Your Conservative Portfolio Remains Stable",
                content="""Dear [CLIENT_NAME],

I hope this message finds you well. I'm writing to provide you with an update on today's market activity and reassure you about your portfolio positioning.

While today's market movements may seem concerning, your conservative portfolio allocation is specifically designed to weather these periods of volatility. Your bond and cash positions are providing the stability and protection we built into your strategy.

Key points about your portfolio:
• Your conservative allocation significantly limits exposure to market swings
• Quality bonds and cash reserves are acting as stabilizers
• This market behavior validates our defensive positioning
• Your long-term financial goals remain on track

Market volatility is a normal part of investing, and your portfolio is structured to protect your wealth during uncertain times. If you have any concerns or would like to discuss your portfolio, please don't hesitate to reach out.

Best regards,
[ADVISOR_NAME]""",
                target_audience="conservative_clients",
                urgency=UrgencyLevel.MODERATE,
                approval_required=False
            ),
            
            "MARKET_CORRECTION_URGENT": CommunicationTemplate(
                template_id="TMPL_002",
                name="Market Correction - Urgent Client Communication",
                type=CommunicationType.EMAIL,
                subject_line="Important Market Update and Your Portfolio",
                content="""Dear [CLIENT_NAME],

I'm reaching out immediately regarding the current market correction to provide you with context and reassurance about your investment strategy.

Current Situation:
• The market has entered correction territory (decline >10%)
• This is a normal part of market cycles that occurs regularly
• Your diversified portfolio is designed for exactly these conditions

Your Portfolio Status:
• Risk management strategies are working as intended
• Defensive positions are providing downside protection
• Long-term investment thesis remains intact
• No immediate action required on your part

I will be closely monitoring the situation and will reach out if any adjustments to your strategy become advisable. In the meantime, please remember that maintaining discipline during corrections has historically been rewarded.

I'm available for a call if you'd like to discuss this further.

Warm regards,
[ADVISOR_NAME]
[PHONE_NUMBER]""",
                target_audience="all_clients",
                urgency=UrgencyLevel.HIGH,
                approval_required=True
            ),

            "EMERGENCY_CONTACT": CommunicationTemplate(
                template_id="TMPL_003",
                name="Emergency Client Contact",
                type=CommunicationType.PHONE,
                subject_line="Emergency Client Contact Script",
                content="""EMERGENCY CONTACT SCRIPT

Opening:
"Hello [CLIENT_NAME], this is [ADVISOR_NAME]. I'm calling because of the significant market event happening today, and I wanted to personally reach out to discuss your portfolio and address any concerns you might have."

Key Message Points:
1. Acknowledge the seriousness of the situation
2. Provide immediate context about their specific portfolio
3. Explain protective measures in place
4. Offer specific next steps and availability
5. Schedule immediate follow-up if needed

Closing:
"I want you to know that I'm monitoring this situation closely and am available throughout this period. My immediate focus is on protecting your wealth and ensuring you feel supported during this challenging time."

IMPORTANT: Use calm, confident tone. Listen actively. Document all interactions.""",
                target_audience="high_priority_clients",
                urgency=UrgencyLevel.EMERGENCY,
                approval_required=False
            )
        }
    
    def _initialize_campaigns(self):
        """Initialize outreach campaigns"""
        self._campaigns = {}
        
        # Sample campaign
        sample_campaign = OutreachCampaign(
            campaign_id="CAMP_001",
            name="Market Volatility Response Campaign",
            trigger_event="Market decline >5% single day",
            target_segments=["conservative", "moderate", "high_net_worth"],
            communication_methods=[CommunicationType.EMAIL, CommunicationType.PHONE],
            timeline="Within 4 hours",
            status="READY",
            created_timestamp=datetime.now(),
            estimated_reach=250
        )
        
        self._campaigns[sample_campaign.campaign_id] = sample_campaign
    
    def send_communication(
        self, 
        client_ids: List[str], 
        template_id: str, 
        personalization: Optional[Dict[str, str]] = None,
        urgency: Optional[str] = None
    ) -> APIResponse:
        """Send communication to specified clients"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to send communications")
        
        if template_id not in self._templates:
            return self._create_response(error=f"Template {template_id} not found")
        
        template = self._templates[template_id]
        
        # Simulate sending messages
        sent_messages = []
        failed_messages = []
        
        for client_id in client_ids:
            # Simulate occasional delivery failures
            if random.random() < 0.05:  # 5% failure rate
                failed_messages.append({
                    "client_id": client_id,
                    "error": "Delivery failed - invalid contact information"
                })
            else:
                message_id = f"MSG_{datetime.now().strftime('%Y%m%d%H%M%S')}_{client_id}"
                
                # Apply personalization if provided
                content = template.content
                if personalization:
                    for key, value in personalization.items():
                        content = content.replace(f"[{key.upper()}]", value)
                
                message_record = {
                    "message_id": message_id,
                    "client_id": client_id,
                    "template_id": template_id,
                    "communication_type": template.type.value,
                    "subject_line": template.subject_line,
                    "sent_timestamp": datetime.now().isoformat(),
                    "urgency_level": urgency or template.urgency.value,
                    "delivery_status": "SENT"
                }
                
                sent_messages.append(message_record)
                self._message_log.append(message_record)
        
        return self._create_response(data={
            "campaign_id": f"SEND_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "template_used": template_id,
            "total_targeted": len(client_ids),
            "successfully_sent": len(sent_messages),
            "failed_deliveries": len(failed_messages),
            "sent_messages": sent_messages,
            "failed_messages": failed_messages,
            "execution_timestamp": datetime.now().isoformat()
        })
    
    def create_outreach_campaign(
        self,
        campaign_name: str,
        trigger_event: str,
        target_segments: List[str],
        timeline: str,
        communication_methods: List[str]
    ) -> APIResponse:
        """Create a new outreach campaign"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to create outreach campaign")
        
        campaign_id = f"CAMP_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Convert string communication methods to enum
        comm_methods = []
        for method in communication_methods:
            try:
                comm_methods.append(CommunicationType(method.lower()))
            except ValueError:
                return self._create_response(error=f"Invalid communication method: {method}")
        
        # Estimate reach based on segments
        segment_sizes = {
            "conservative": 75,
            "moderate": 100, 
            "aggressive": 50,
            "high_net_worth": 25,
            "all_clients": 250
        }
        
        estimated_reach = sum(segment_sizes.get(segment, 50) for segment in target_segments)
        
        campaign = OutreachCampaign(
            campaign_id=campaign_id,
            name=campaign_name,
            trigger_event=trigger_event,
            target_segments=target_segments,
            communication_methods=comm_methods,
            timeline=timeline,
            status="CREATED",
            created_timestamp=datetime.now(),
            estimated_reach=estimated_reach
        )
        
        self._campaigns[campaign_id] = campaign
        
        return self._create_response(data={
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
            "status": "CREATED",
            "estimated_reach": estimated_reach,
            "target_segments": target_segments,
            "timeline": timeline,
            "created_timestamp": datetime.now().isoformat()
        })
    
    def execute_outreach_campaign(self, campaign_id: str, template_mappings: Dict[str, str]) -> APIResponse:
        """Execute an outreach campaign"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to execute outreach campaign")
        
        if campaign_id not in self._campaigns:
            return self._create_response(error=f"Campaign {campaign_id} not found")
        
        campaign = self._campaigns[campaign_id]
        
        # Simulate campaign execution
        execution_results = {}
        total_sent = 0
        total_failed = 0
        
        for segment in campaign.target_segments:
            template_id = template_mappings.get(segment, "TMPL_001")
            
            # Simulate client list for segment
            segment_size = {"conservative": 75, "moderate": 100, "aggressive": 50, "high_net_worth": 25}.get(segment, 50)
            mock_client_ids = [f"{segment.upper()}_{i:03d}" for i in range(1, segment_size + 1)]
            
            # Simulate sending
            sent_count = int(segment_size * 0.95)  # 95% success rate
            failed_count = segment_size - sent_count
            
            execution_results[segment] = {
                "template_used": template_id,
                "targeted_clients": segment_size,
                "successfully_sent": sent_count,
                "failed_deliveries": failed_count,
                "segment_completion": f"{(sent_count/segment_size)*100:.1f}%"
            }
            
            total_sent += sent_count
            total_failed += failed_count
        
        # Update campaign status
        campaign.status = "EXECUTED"
        
        return self._create_response(data={
            "campaign_id": campaign_id,
            "execution_timestamp": datetime.now().isoformat(),
            "overall_results": {
                "total_targeted": campaign.estimated_reach,
                "total_sent": total_sent,
                "total_failed": total_failed,
                "overall_success_rate": f"{(total_sent/(total_sent + total_failed))*100:.1f}%"
            },
            "segment_results": execution_results,
            "campaign_status": "EXECUTED"
        })
    
    def get_communication_templates(self, template_type: Optional[str] = None) -> APIResponse:
        """Get available communication templates"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to retrieve communication templates")
        
        templates_data = {}
        for template_id, template in self._templates.items():
            if template_type is None or template.type.value == template_type:
                templates_data[template_id] = {
                    "name": template.name,
                    "type": template.type.value,
                    "subject_line": template.subject_line,
                    "target_audience": template.target_audience,
                    "urgency": template.urgency.value,
                    "approval_required": template.approval_required,
                    "content_preview": template.content[:200] + "..." if len(template.content) > 200 else template.content
                }
        
        return self._create_response(data={
            "templates": templates_data,
            "total_templates": len(templates_data),
            "filtered_by_type": template_type
        })
    
    def get_message_delivery_status(self, message_ids: List[str]) -> APIResponse:
        """Get delivery status for sent messages"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to retrieve message status")
        
        status_results = {}
        
        for message_id in message_ids:
            # Find message in log
            message_record = next((msg for msg in self._message_log if msg["message_id"] == message_id), None)
            
            if message_record:
                # Simulate delivery progression
                delivery_statuses = ["SENT", "DELIVERED", "READ", "RESPONDED"]
                current_status = random.choice(delivery_statuses)
                
                status_results[message_id] = {
                    "message_id": message_id,
                    "current_status": current_status,
                    "sent_timestamp": message_record["sent_timestamp"],
                    "delivered_timestamp": (datetime.now() + timedelta(minutes=random.randint(1, 30))).isoformat() if current_status in ["DELIVERED", "READ", "RESPONDED"] else None,
                    "read_timestamp": (datetime.now() + timedelta(minutes=random.randint(30, 120))).isoformat() if current_status in ["READ", "RESPONDED"] else None,
                    "client_id": message_record["client_id"]
                }
            else:
                status_results[message_id] = {
                    "message_id": message_id,
                    "error": "Message not found in system"
                }
        
        return self._create_response(data={
            "status_check_timestamp": datetime.now().isoformat(),
            "messages_checked": len(message_ids),
            "delivery_statuses": status_results
        })
    
    def schedule_emergency_calls(
        self, 
        client_priority_list: List[Dict[str, Any]], 
        urgency_level: str,
        estimated_duration: int = 30
    ) -> APIResponse:
        """Schedule emergency calls for high-priority clients"""
        self._simulate_network_delay()
        
        if self._simulate_occasional_failure():
            return self._create_response(error="Failed to schedule emergency calls")
        
        scheduled_calls = []
        current_time = datetime.now()
        
        # Sort by priority (assuming higher priority number = more urgent)
        sorted_clients = sorted(client_priority_list, key=lambda x: x.get("priority", 5), reverse=True)
        
        for i, client_info in enumerate(sorted_clients):
            # Calculate call time based on priority and urgency
            if urgency_level == "emergency":
                call_time = current_time + timedelta(minutes=i * 10)  # Every 10 minutes
            elif urgency_level == "critical":
                call_time = current_time + timedelta(minutes=i * 20)  # Every 20 minutes
            else:
                call_time = current_time + timedelta(hours=i * 0.5)   # Every 30 minutes
            
            call_id = f"CALL_{datetime.now().strftime('%Y%m%d%H%M%S')}_{i:03d}"
            
            scheduled_call = {
                "call_id": call_id,
                "client_id": client_info.get("client_id", "UNKNOWN"),
                "client_name": client_info.get("client_name", "Unknown Client"),
                "priority_level": client_info.get("priority", 5),
                "scheduled_time": call_time.isoformat(),
                "estimated_duration_minutes": estimated_duration,
                "urgency_level": urgency_level,
                "call_status": "SCHEDULED",
                "advisor_assigned": client_info.get("advisor", "Primary Advisor"),
                "phone_number": client_info.get("phone", "XXX-XXX-XXXX")
            }
            
            scheduled_calls.append(scheduled_call)
        
        return self._create_response(data={
            "emergency_call_schedule": {
                "schedule_id": f"SCHED_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "urgency_level": urgency_level,
                "total_calls_scheduled": len(scheduled_calls),
                "first_call_time": scheduled_calls[0]["scheduled_time"] if scheduled_calls else None,
                "last_call_time": scheduled_calls[-1]["scheduled_time"] if scheduled_calls else None,
                "estimated_total_duration_hours": (len(scheduled_calls) * estimated_duration) / 60
            },
            "scheduled_calls": scheduled_calls,
            "scheduling_timestamp": datetime.now().isoformat()
        })