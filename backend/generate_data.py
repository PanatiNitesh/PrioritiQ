import os
import csv
import json
import random
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
NOTES_DIR = os.path.join(DATA_DIR, "notes")
os.makedirs(NOTES_DIR, exist_ok=True)

companies = [
    {"company_id": "COMP-101", "name": "ApexFin Technologies", "domain": "apexfin.io", "industry": "Fintech", "employees": 420, "annual_revenue": 85000000, "tech_stack": "AWS, Postgres, Snowflake", "region": "North America", "icp_fit": 96},
    {"company_id": "COMP-102", "name": "BioHealth Global", "domain": "biohealth.co", "industry": "Healthcare", "employees": 1250, "annual_revenue": 210000000, "tech_stack": "Azure, Epic, Salesforce", "region": "North America", "icp_fit": 92},
    {"company_id": "COMP-103", "name": "OmniRetail Group", "domain": "omniretail.com", "industry": "E-Commerce", "employees": 890, "annual_revenue": 145000000, "tech_stack": "GCP, Shopify Plus, BigQuery", "region": "Europe", "icp_fit": 88},
    {"company_id": "COMP-104", "name": "CyberShield Labs", "domain": "cybershield.ai", "industry": "Cybersecurity", "employees": 310, "annual_revenue": 62000000, "tech_stack": "AWS, Kubernetes, Datadog", "region": "North America", "icp_fit": 94},
    {"company_id": "COMP-105", "name": "Vanguard Logistics", "domain": "vanguardlog.com", "industry": "Supply Chain", "employees": 2400, "annual_revenue": 380000000, "tech_stack": "SAP, Oracle, Azure", "region": "North America", "icp_fit": 78},
    {"company_id": "COMP-106", "name": "Aether Dynamics", "domain": "aetherdyn.com", "industry": "Aerospace & Defense", "employees": 1800, "annual_revenue": 450000000, "tech_stack": "On-Prem, AWS GovCloud", "region": "North America", "icp_fit": 84},
    {"company_id": "COMP-107", "name": "PulseMedia Networks", "domain": "pulsemedia.tv", "industry": "Media & Entertainment", "employees": 520, "annual_revenue": 95000000, "tech_stack": "GCP, Cloudflare, Segment", "region": "Europe", "icp_fit": 72},
    {"company_id": "COMP-108", "name": "TerraGreen Energies", "domain": "terragreen.energy", "industry": "CleanTech", "employees": 640, "annual_revenue": 110000000, "tech_stack": "AWS, Snowflake, Tableau", "region": "North America", "icp_fit": 89},
    {"company_id": "COMP-109", "name": "NexusPay Solutions", "domain": "nexuspay.io", "industry": "Fintech", "employees": 280, "annual_revenue": 48000000, "tech_stack": "GCP, Stripe, Postgres", "region": "North America", "icp_fit": 91},
    {"company_id": "COMP-110", "name": "Titan Heavy Industries", "domain": "titanind.com", "industry": "Manufacturing", "employees": 4600, "annual_revenue": 820000000, "tech_stack": "SAP, Infor, Microsoft 365", "region": "Europe", "icp_fit": 65},
    {"company_id": "COMP-111", "name": "Lumina SaaS Systems", "domain": "luminasaas.com", "industry": "Enterprise Software", "employees": 390, "annual_revenue": 72000000, "tech_stack": "AWS, React, MongoDB", "region": "North America", "icp_fit": 95},
    {"company_id": "COMP-112", "name": "Zenith AI Corp", "domain": "zenithai.dev", "industry": "Artificial Intelligence", "employees": 180, "annual_revenue": 35000000, "tech_stack": "GCP, PyTorch, Ray", "region": "North America", "icp_fit": 90}
]

leads = [
    {
        "lead_id": "LEAD-101",
        "company_id": "COMP-101",
        "name": "Sarah Jenkins",
        "title": "VP of Revenue Operations",
        "email": "sjenkins@apexfin.io",
        "phone": "+1-415-555-0192",
        "stage": "Negotiation",
        "deal_size": 145000,
        "created_date": "2026-08-15",
        "last_activity_date": "2026-09-26",
        "assigned_rep": "Alex Rivera",
        "touchpoints_count": 14,
        "intent_score": 96,
        "est_effort_mins": 35,
        "delta_status": "URGENT_INBOUND_TODAY",
        "churn_risk": "Low"
    },
    {
        "lead_id": "LEAD-102",
        "company_id": "COMP-104",
        "name": "Marcus Vance",
        "title": "Chief Information Security Officer",
        "email": "mvance@cybershield.ai",
        "phone": "+1-206-555-0144",
        "stage": "Proposal",
        "deal_size": 180000,
        "created_date": "2026-08-20",
        "last_activity_date": "2026-09-25",
        "assigned_rep": "Elena Rostova",
        "touchpoints_count": 11,
        "intent_score": 92,
        "est_effort_mins": 45,
        "delta_status": "SECURITY_REVIEW_CLEARED",
        "churn_risk": "Low"
    },
    {
        "lead_id": "LEAD-103",
        "company_id": "COMP-102",
        "name": "Dr. Eleanor Hayes",
        "title": "Head of Clinical Informatics",
        "email": "ehayes@biohealth.co",
        "phone": "+1-617-555-0188",
        "stage": "Demo",
        "deal_size": 220000,
        "created_date": "2026-09-01",
        "last_activity_date": "2026-09-26",
        "assigned_rep": "Alex Rivera",
        "touchpoints_count": 8,
        "intent_score": 89,
        "est_effort_mins": 40,
        "delta_status": "EXECUTIVE_JOINED_EVAL",
        "churn_risk": "Medium"
    },
    {
        "lead_id": "LEAD-104",
        "company_id": "COMP-108",
        "name": "Liam Gallagher",
        "title": "Director of Grid Intelligence",
        "email": "lgallagher@terragreen.energy",
        "phone": "+1-512-555-0173",
        "stage": "Negotiation",
        "deal_size": 95000,
        "created_date": "2026-08-10",
        "last_activity_date": "2026-09-25",
        "assigned_rep": "Devon Miller",
        "touchpoints_count": 16,
        "intent_score": 91,
        "est_effort_mins": 30,
        "delta_status": "FISCAL_YEAR_END_FRIDAY",
        "churn_risk": "Low"
    },
    {
        "lead_id": "LEAD-105",
        "company_id": "COMP-111",
        "name": "Rachel Kim",
        "title": "Chief Technology Officer",
        "email": "rkim@luminasaas.com",
        "phone": "+1-650-555-0131",
        "stage": "Proposal",
        "deal_size": 130000,
        "created_date": "2026-08-28",
        "last_activity_date": "2026-09-26",
        "assigned_rep": "Elena Rostova",
        "touchpoints_count": 9,
        "intent_score": 87,
        "est_effort_mins": 30,
        "delta_status": "CONTRACT_REDLINE_RECEIVED",
        "churn_risk": "Low"
    },
    {
        "lead_id": "LEAD-106",
        "company_id": "COMP-109",
        "name": "Jordan Morales",
        "title": "VP of Merchant Operations",
        "email": "jmorales@nexuspay.io",
        "phone": "+1-312-555-0165",
        "stage": "Closing",
        "deal_size": 78000,
        "created_date": "2026-07-22",
        "last_activity_date": "2026-09-26",
        "assigned_rep": "Devon Miller",
        "touchpoints_count": 19,
        "intent_score": 95,
        "est_effort_mins": 25,
        "delta_status": "SIGNATURE_PENDING_TODAY",
        "churn_risk": "Low"
    },
    {
        "lead_id": "LEAD-107",
        "company_id": "COMP-105",
        "name": "Harold Sterling",
        "title": "SVP Global Fleet Systems",
        "email": "hsterling@vanguardlog.com",
        "phone": "+1-404-555-0129",
        "stage": "Discovery",
        "deal_size": 310000,
        "created_date": "2026-09-12",
        "last_activity_date": "2026-09-19",
        "assigned_rep": "Alex Rivera",
        "touchpoints_count": 4,
        "intent_score": 62,
        "est_effort_mins": 60,
        "delta_status": "STALLED_NO_UPDATE_7D",
        "churn_risk": "High"
    },
    {
        "lead_id": "LEAD-108",
        "company_id": "COMP-103",
        "name": "Chloe Dupont",
        "title": "Head of Omnichannel Strategy",
        "email": "cdupont@omniretail.com",
        "phone": "+33-1-55-55-01-42",
        "stage": "Demo",
        "deal_size": 115000,
        "created_date": "2026-09-05",
        "last_activity_date": "2026-09-24",
        "assigned_rep": "Elena Rostova",
        "touchpoints_count": 7,
        "intent_score": 79,
        "est_effort_mins": 35,
        "delta_status": "COMPETITOR_EVAL_ACTIVE",
        "churn_risk": "Medium"
    },
    {
        "lead_id": "LEAD-109",
        "company_id": "COMP-106",
        "name": "General Keith Bradley (Ret.)",
        "title": "Director of Secure Avionics",
        "email": "kbradley@aetherdyn.com",
        "phone": "+1-703-555-0182",
        "stage": "Discovery",
        "deal_size": 420000,
        "created_date": "2026-08-01",
        "last_activity_date": "2026-09-14",
        "assigned_rep": "Devon Miller",
        "touchpoints_count": 5,
        "intent_score": 58,
        "est_effort_mins": 60,
        "delta_status": "BUDGET_FROZEN_UNTIL_Q1",
        "churn_risk": "High"
    },
    {
        "lead_id": "LEAD-110",
        "company_id": "COMP-112",
        "name": "Dr. Tanya O’Connor",
        "title": "Chief Scientist & Co-Founder",
        "email": "toconnor@zenithai.dev",
        "phone": "+1-650-555-0199",
        "stage": "Proposal",
        "deal_size": 88000,
        "created_date": "2026-09-08",
        "last_activity_date": "2026-09-25",
        "assigned_rep": "Elena Rostova",
        "touchpoints_count": 10,
        "intent_score": 86,
        "est_effort_mins": 30,
        "delta_status": "TECH_PO_APPROVED",
        "churn_risk": "Low"
    },
    {
        "lead_id": "LEAD-111",
        "company_id": "COMP-107",
        "name": "Bradley Cooper-Smith",
        "title": "Director of Digital Delivery",
        "email": "bcoopersmith@pulsemedia.tv",
        "phone": "+44-20-7946-0123",
        "stage": "Discovery",
        "deal_size": 65000,
        "created_date": "2026-09-15",
        "last_activity_date": "2026-09-22",
        "assigned_rep": "Alex Rivera",
        "touchpoints_count": 3,
        "intent_score": 54,
        "est_effort_mins": 45,
        "delta_status": "LOW_ENGAGEMENT",
        "churn_risk": "High"
    },
    {
        "lead_id": "LEAD-112",
        "company_id": "COMP-110",
        "name": "Klaus Richter",
        "title": "VP Automation Systems",
        "email": "krichter@titanind.com",
        "phone": "+49-89-555-0155",
        "stage": "Discovery",
        "deal_size": 280000,
        "created_date": "2026-08-18",
        "last_activity_date": "2026-09-10",
        "assigned_rep": "Devon Miller",
        "touchpoints_count": 6,
        "intent_score": 49,
        "est_effort_mins": 60,
        "delta_status": "DECISION_MAKER_ON_LEAVE",
        "churn_risk": "High"
    }
]

activities = [
    {"activity_id": "ACT-301", "lead_id": "LEAD-101", "type": "Email Inbound", "timestamp": "2026-09-26 08:42", "rep": "Alex Rivera", "duration": 0, "outcome": "Urgent Request", "notes_ref": "NOTE-LEAD-101-04"},
    {"activity_id": "ACT-302", "lead_id": "LEAD-101", "type": "Executive Call", "timestamp": "2026-09-25 15:30", "rep": "Alex Rivera", "duration": 45, "outcome": "Pricing Agreed", "notes_ref": "NOTE-LEAD-101-03"},
    {"activity_id": "ACT-303", "lead_id": "LEAD-102", "type": "Security Clearance", "timestamp": "2026-09-25 17:15", "rep": "Elena Rostova", "duration": 30, "outcome": "SOC2 Approved", "notes_ref": "NOTE-LEAD-102-03"},
    {"activity_id": "ACT-304", "lead_id": "LEAD-103", "type": "Demo Meeting", "timestamp": "2026-09-26 09:15", "rep": "Alex Rivera", "duration": 50, "outcome": "VP Clinical Joined", "notes_ref": "NOTE-LEAD-103-02"},
    {"activity_id": "ACT-305", "lead_id": "LEAD-104", "type": "Phone Call", "timestamp": "2026-09-25 11:00", "rep": "Devon Miller", "duration": 25, "outcome": "Budget Deadline Confirmed", "notes_ref": "NOTE-LEAD-104-03"},
    {"activity_id": "ACT-306", "lead_id": "LEAD-105", "type": "Email Inbound", "timestamp": "2026-09-26 07:55", "rep": "Elena Rostova", "duration": 0, "outcome": "Legal Redlines", "notes_ref": "NOTE-LEAD-105-02"},
    {"activity_id": "ACT-307", "lead_id": "LEAD-106", "type": "DocuSign Sent", "timestamp": "2026-09-26 10:10", "rep": "Devon Miller", "duration": 15, "outcome": "DocuSign Opened", "notes_ref": "NOTE-LEAD-106-03"},
    {"activity_id": "ACT-308", "lead_id": "LEAD-107", "type": "Voicemail", "timestamp": "2026-09-19 14:00", "rep": "Alex Rivera", "duration": 5, "outcome": "No Response", "notes_ref": "NOTE-LEAD-107-01"},
    {"activity_id": "ACT-309", "lead_id": "LEAD-108", "type": "Competitive Comparison", "timestamp": "2026-09-24 16:00", "rep": "Elena Rostova", "duration": 40, "outcome": "Evaluating Competitor X", "notes_ref": "NOTE-LEAD-108-02"},
    {"activity_id": "ACT-310", "lead_id": "LEAD-109", "type": "Status Check", "timestamp": "2026-09-14 11:30", "rep": "Devon Miller", "duration": 20, "outcome": "Government Budget Delayed", "notes_ref": "NOTE-LEAD-109-01"},
    {"activity_id": "ACT-311", "lead_id": "LEAD-110", "type": "PO Confirmation", "timestamp": "2026-09-25 14:20", "rep": "Elena Rostova", "duration": 20, "outcome": "Finance Approved", "notes_ref": "NOTE-LEAD-110-02"},
    {"activity_id": "ACT-312", "lead_id": "LEAD-112", "type": "Email Outbound", "timestamp": "2026-09-10 10:00", "rep": "Devon Miller", "duration": 0, "outcome": "Out of Office Reply", "notes_ref": "NOTE-LEAD-112-01"}
]

notes_data = [
    {
        "filename": "NOTE-LEAD-101-04.txt",
        "lead_id": "LEAD-101",
        "author": "Alex Rivera",
        "date": "2026-09-26 08:42",
        "type": "Inbound Email",
        "subject": "Urgent: Final board sign-off pending indemnification clause update",
        "content": """From: Sarah Jenkins <sjenkins@apexfin.io>
To: Alex Rivera <arivera@decisiongraph.ai>
Date: Fri, 26 Sep 2026 08:42:15 EDT
Subject: Re: ApexFin & DecisionGraph Contract Review

Hi Alex,
Good news - our CFO and General Counsel met early this morning. We have full executive authorization to execute the $145,000 annual agreement today, provided we make one quick edit to Section 9.2 (standard mutual indemnification wording).
If your legal team can return the updated contract before 2:00 PM EST, our CEO will countersign before our end-of-quarter freeze at 5:00 PM today.
Please call my direct line if you can turn this around this morning."""
    },
    {
        "filename": "NOTE-LEAD-101-03.txt",
        "lead_id": "LEAD-101",
        "author": "Alex Rivera",
        "date": "2026-09-25 15:30",
        "type": "Executive Call Transcript",
        "subject": "Negotiation wrap-up call with VP RevOps",
        "content": """Summary: Sarah Jenkins confirmed they evaluated Competitor Gong and Clari, but chose DecisionGraph because of our real-time evidence graph explainability. Budget of $145k is 100% earmarked from this fiscal quarter's ops budget. Deal velocity is exceptionally high - 42 days from initial discovery to negotiation. Close probability rated 95%."""
    },
    {
        "filename": "NOTE-LEAD-102-03.txt",
        "lead_id": "LEAD-102",
        "author": "Elena Rostova",
        "date": "2026-09-25 17:15",
        "type": "Security Debrief",
        "subject": "CyberShield SOC2 Type II clearance achieved",
        "content": """CISO Marcus Vance signed off on our InfoSec questionnaire yesterday afternoon. CyberShield was holding off the $180k enterprise tier pending our zero-trust data ingestion safeguards. Now that our security architecture is approved, Vance requested a 45-minute executive briefing with their CEO this afternoon to finalize implementation schedules."""
    },
    {
        "filename": "NOTE-LEAD-103-02.txt",
        "lead_id": "LEAD-103",
        "author": "Alex Rivera",
        "date": "2026-09-26 09:15",
        "type": "Call Transcript",
        "subject": "BioHealth Clinical Informatics Demo debrief",
        "content": """Dr. Eleanor Hayes brought Dr. Robert Chen (Chief Medical Officer) onto our morning demo unexpectedly. This is a massive positive signal: Chen stated 'This directly solves our HIPAA analytics bottleneck across 14 hospital networks'. Deal size estimated at $220,000. Next action required: follow up with HIPAA BAA addendum within 24 hours to keep momentum."""
    },
    {
        "filename": "NOTE-LEAD-104-03.txt",
        "lead_id": "LEAD-104",
        "author": "Devon Miller",
        "date": "2026-09-25 11:00",
        "type": "Sales Call Notes",
        "subject": "TerraGreen Fiscal Year End Budget Surplus",
        "content": """Liam Gallagher informed me that TerraGreen's fiscal year closes this Friday, September 30. They have $95,000 in unallocated CapEx budget that will expire if not committed this week. Quote #TG-4029 has already been drawn up. A quick 30-minute alignment call with their procurement desk today will secure PO signature."""
    },
    {
        "filename": "NOTE-LEAD-105-02.txt",
        "lead_id": "LEAD-105",
        "author": "Elena Rostova",
        "date": "2026-09-26 07:55",
        "type": "Inbound Redline",
        "subject": "Lumina SaaS Master Service Agreement redlines",
        "content": """CTO Rachel Kim returned our standard MSA with 3 minor redlines regarding API uptime SLA (requesting 99.95% instead of 99.9%). Our VP Eng approved this variance. Contract value: $130,000 ARR. Rachel noted: 'Send over the clean DocuSign copy and I will sign today.'"""
    },
    {
        "filename": "NOTE-LEAD-106-03.txt",
        "lead_id": "LEAD-106",
        "author": "Devon Miller",
        "date": "2026-09-26 10:10",
        "type": "DocuSign Telemetry",
        "subject": "NexusPay DocuSign envelope activity",
        "content": """Telemetry alert: Jordan Morales (VP Merchant Ops) and CFO David Lin have opened the final DocuSign agreement ($78,000 ARR) 4 times between 09:30 and 10:05 AM. Sent reminder ping. Closing probability 99% with estimated 25-minute closing call to answer minor billing questions."""
    },
    {
        "filename": "NOTE-LEAD-107-01.txt",
        "lead_id": "LEAD-107",
        "author": "Alex Rivera",
        "date": "2026-09-19 14:00",
        "type": "Rep Notes",
        "subject": "Vanguard Logistics account status - Stalled",
        "content": """Harold Sterling has not replied to 3 consecutive emails or phone inquiries over the past 7 business days. Although deal potential is high ($310,000), internal champion left the company last month. Recommendation: Do NOT spend prime sales capacity today; keep on nurture sequence."""
    },
    {
        "filename": "NOTE-LEAD-108-02.txt",
        "lead_id": "LEAD-108",
        "author": "Elena Rostova",
        "date": "2026-09-24 16:00",
        "type": "Competitive Analysis",
        "subject": "OmniRetail evaluating competitor platform",
        "content": """Chloe Dupont stated that a competitor has offered an aggressive 30% first-year discount. OmniRetail wants a feature comparison on real-time decision explainability before proceeding. Potential deal: $115,000, but closing cycle will take at least 3-4 more weeks. Lower immediate priority for today."""
    },
    {
        "filename": "NOTE-LEAD-109-01.txt",
        "lead_id": "LEAD-109",
        "author": "Devon Miller",
        "date": "2026-09-14 11:30",
        "type": "Executive Debrief",
        "subject": "Aether Dynamics Procurement Freeze",
        "content": """General Keith Bradley informed us that due to federal defense contract reassessments, all external SaaS procurement exceeding $250k is frozen until Q1 2027. Deal size: $420,000. No immediate buying authority. Recommend deferring active outreach until December."""
    },
    {
        "filename": "NOTE-LEAD-110-02.txt",
        "lead_id": "LEAD-110",
        "author": "Elena Rostova",
        "date": "2026-09-25 14:20",
        "type": "Procurement Note",
        "subject": "Zenith AI purchase order approval",
        "content": """Dr. Tanya O'Connor communicated that Zenith's finance committee approved our $88,000 quote. They are waiting for our technical architecture whitepaper and will issue PO on Friday. Requires 30 minutes to review deployment architecture with their lead DevOps engineer."""
    },
    {
        "filename": "NOTE-LEAD-112-01.txt",
        "lead_id": "LEAD-112",
        "author": "Devon Miller",
        "date": "2026-09-10 10:00",
        "type": "Account Note",
        "subject": "Titan Heavy Industries key stakeholder on sabbatical",
        "content": """Klaus Richter is on extended sabbatical until late October. Alternate contact lacks purchasing authority for deals over $50k. Deal size $280,000 is on hold. Mark as deferred."""
    }
]

def generate_csvs():
    # Write companies.csv
    companies_file = os.path.join(DATA_DIR, "companies.csv")
    with open(companies_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(companies[0].keys()))
        writer.writeheader()
        writer.writerows(companies)
    print(f"Created {companies_file} ({len(companies)} rows)")

    # Write leads.csv
    leads_file = os.path.join(DATA_DIR, "leads.csv")
    with open(leads_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(leads[0].keys()))
        writer.writeheader()
        writer.writerows(leads)
    print(f"Created {leads_file} ({len(leads)} rows)")

    # Write activities.csv
    activities_file = os.path.join(DATA_DIR, "activities.csv")
    with open(activities_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(activities[0].keys()))
        writer.writeheader()
        writer.writerows(activities)
    print(f"Created {activities_file} ({len(activities)} rows)")

    # Write unstructured notes
    for note in notes_data:
        note_path = os.path.join(NOTES_DIR, note["filename"])
        metadata_header = f"""---
lead_id: {note['lead_id']}
author: {note['author']}
date: {note['date']}
type: {note['type']}
subject: {note['subject']}
---

"""
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(metadata_header + note["content"])
    print(f"Created {len(notes_data)} notes in {NOTES_DIR}")

if __name__ == "__main__":
    generate_csvs()
