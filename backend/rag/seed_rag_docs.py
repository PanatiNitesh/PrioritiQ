import os

NOTES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "notes"))
os.makedirs(NOTES_DIR, exist_ok=True)

extra_unstructured_docs = [
    {
        "filename": "Product_Doc_Enterprise_ZeroTrust.txt",
        "lead_id": "GLOBAL-PROD",
        "author": "Product Engineering",
        "date": "2026-09-20 10:00",
        "type": "Product Document",
        "subject": "PrioritiQ Zero-Trust Data Ingestion & SOC2 Specifications",
        "content": """PrioritiQ Zero-Trust Architecture guarantees that customer CRM data, email streams, and transcripts remain encrypted in-transit (TLS 1.3) and at-rest (AES-256). Enterprise tier includes VPC peering, HIPAA BAA compliance, SOC2 Type II audited perimeter, and customer-managed KMS keys. Deployments can run fully on-premises or via dedicated AWS/Azure private endpoints without external model training leakage."""
    },
    {
        "filename": "Company_Note_ApexFin_Strategy.txt",
        "lead_id": "LEAD-101",
        "author": "Strategic Accounts Desk",
        "date": "2026-09-24 14:00",
        "type": "Company Note",
        "subject": "ApexFin Q4 Expansion & Decision-Maker Map",
        "content": """ApexFin Technologies is consolidating their sales intelligence stack from Gong and Clari into PrioritiQ. Primary champion Sarah Jenkins (VP RevOps) reports directly to CEO David Vance. Budget ($145k) is already fully reserved under their FY26 automation modernization budget. Key risk: contract must execute prior to their September 30 end-of-quarter blackout."""
    },
    {
        "filename": "Transcript_BioHealth_CMO_Debrief.txt",
        "lead_id": "LEAD-103",
        "author": "Alex Rivera",
        "date": "2026-09-26 09:30",
        "type": "Meeting Transcript",
        "subject": "CMO Dr. Robert Chen on HIPAA BAA & Multi-Hospital Analytics",
        "content": """Speaker 1 (Alex Rivera): 'Dr. Chen, thank you for joining Eleanor on today's session.'
Speaker 2 (Dr. Robert Chen, CMO): 'We have 14 clinical networks struggling with prioritization. If your engine can parse our clinical triage metrics while maintaining BAA safeguards, we have the $220k budget available right now. We just need the BAA signed today to present to our clinical board Monday.'"""
    },
    {
        "filename": "Email_TerraGreen_Procurement_Surplus.txt",
        "lead_id": "LEAD-104",
        "author": "Liam Gallagher",
        "date": "2026-09-25 11:15",
        "type": "Customer Email",
        "subject": "Quote #TG-4029 CapEx Surplus Approval Window",
        "content": """From: Liam Gallagher <lgallagher@terragreen.energy>
To: Devon Miller <dmiller@prioritiq.ai>
Date: Thu, 25 Sep 2026 11:15:02 CST
Subject: Re: Quote TG-4029 Follow-up

Devon,
Our annual fiscal year closes this Friday. Our procurement director confirmed that the $95,000 CapEx balance is approved for Quote #TG-4029. Please get our mutual signatures on the clean agreement by 3:00 PM Thursday so accounting can release the purchase order."""
    }
]

def add_extra_docs():
    for doc in extra_unstructured_docs:
        fp = os.path.join(NOTES_DIR, doc['filename'])
        header = f"""---
lead_id: {doc['lead_id']}
author: {doc['author']}
date: {doc['date']}
type: {doc['type']}
subject: {doc['subject']}
---

"""
        with open(fp, "w", encoding="utf-8") as f:
            f.write(header + doc['content'])
        print(f"Created {fp}")

if __name__ == "__main__":
    add_extra_docs()
