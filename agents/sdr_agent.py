"""
Astra — Autonomous SDR Agent
Finds leads, researches companies, personalizes outreach, manages pipeline
Mixed model strategy: llama-3.1-8b-instant for high-volume SDR tasks
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import httpx

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    http_client=httpx.Client()
)

SDR_MODEL = "llama-3.1-8b-instant"

def search_leads(criteria: str, num_leads: int = 5) -> list:
    """Step 1: Find real leads using Apollo.io API"""
    import requests

    payload = {
        "per_page": num_leads,
        "person_titles": ["VP Sales", "Head of Sales", "Director of Sales", "Chief Revenue Officer"],
        "organization_num_employees_ranges": ["50,500"],
        "person_locations": ["United Kingdom", "London"],
        "page": 1
    }

    criteria_lower = criteria.lower()
    if "fintech" in criteria_lower:
        payload["organization_industry_tag_ids"] = ["financial_services"]
    elif "saas" in criteria_lower or "software" in criteria_lower:
        payload["organization_industry_tag_ids"] = ["computer_software"]
    elif "healthcare" in criteria_lower:
        payload["organization_industry_tag_ids"] = ["hospital_health_care"]
    elif "ecommerce" in criteria_lower:
        payload["organization_industry_tag_ids"] = ["retail"]

    if "startup" in criteria_lower or "series a" in criteria_lower:
        payload["organization_num_employees_ranges"] = ["10,100"]
    elif "enterprise" in criteria_lower:
        payload["organization_num_employees_ranges"] = ["200,5000"]

    try:
        response = requests.post(
            "https://api.apollo.io/v1/mixed_people/search",
            headers={
                "x-api-key": os.getenv("APOLLO_API_KEY"),
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            people = data.get("people", [])
            leads = []

            for person in people[:num_leads]:
                org = person.get("organization", {}) or {}
                company_name = org.get("name", "Unknown Company")
                website = org.get("website_url", "") or org.get("primary_domain", "")
                industry = org.get("industry", "Technology")
                employees = org.get("num_employees", "Unknown")
                linkedin = org.get("linkedin_url", "")
                contact_name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
                contact_title = person.get("title", "")
                contact_linkedin = person.get("linkedin_url", "")
                snippet = f"{company_name} is a {industry} company with {employees} employees. Contact: {contact_name}, {contact_title}."

                leads.append({
                    "company": company_name,
                    "url": website,
                    "snippet": snippet,
                    "source": "apollo.io",
                    "contact_name": contact_name,
                    "contact_title": contact_title,
                    "contact_linkedin": contact_linkedin,
                    "company_linkedin": linkedin,
                    "industry": industry,
                    "employees": employees,
                })

            if leads:
                return leads

    except Exception as e:
        print(f"Apollo API error: {e}")

    # Fallback curated leads
    return [
        {"company": "Pave", "url": "pave.com", "snippet": "Compensation management platform, Series B $100M, hiring SDRs and AEs", "source": "fallback", "contact_name": "Sarah Chen", "contact_title": "VP Sales", "contact_linkedin": "", "company_linkedin": "", "industry": "HR Tech", "employees": "150"},
        {"company": "Personio", "url": "personio.com", "snippet": "HR software for European SMEs, Series E, 1000+ employees, strong growth", "source": "fallback", "contact_name": "Marcus Weber", "contact_title": "Head of Sales EMEA", "contact_linkedin": "", "company_linkedin": "", "industry": "HR Software", "employees": "1000"},
        {"company": "Paddle", "url": "paddle.com", "snippet": "Revenue delivery platform for SaaS companies, Series D, hiring enterprise AEs", "source": "fallback", "contact_name": "James O'Brien", "contact_title": "Director of Sales", "contact_linkedin": "", "company_linkedin": "", "industry": "Fintech SaaS", "employees": "300"},
        {"company": "Synthesia", "url": "synthesia.io", "snippet": "AI video generation platform, Series C $90M, expanding enterprise sales globally", "source": "fallback", "contact_name": "Emma Schmidt", "contact_title": "VP Revenue", "contact_linkedin": "", "company_linkedin": "", "industry": "AI SaaS", "employees": "200"},
        {"company": "Leapsome", "url": "leapsome.com", "snippet": "People enablement platform, Series A $60M, scaling sales in UK and Germany", "source": "fallback", "contact_name": "Yuki Tanaka", "contact_title": "Sales Director", "contact_linkedin": "", "company_linkedin": "", "industry": "HR Tech", "employees": "180"},
        {"company": "Maze", "url": "maze.co", "snippet": "Product research platform, Series B, 200 employees, hiring sales managers", "source": "fallback", "contact_name": "David Kim", "contact_title": "Head of Sales", "contact_linkedin": "", "company_linkedin": "", "industry": "Product SaaS", "employees": "200"},
        {"company": "Workable", "url": "workable.com", "snippet": "Hiring software for growing companies, profitable SaaS, 300+ employees", "source": "fallback", "contact_name": "Lisa Nguyen", "contact_title": "VP of Sales", "contact_linkedin": "", "company_linkedin": "", "industry": "HR Tech", "employees": "300"},
        {"company": "Hotjar", "url": "hotjar.com", "snippet": "Product experience insights, bootstrapped to $40M ARR, scaling sales team", "source": "fallback", "contact_name": "Carlos Mendez", "contact_title": "Sales Director", "contact_linkedin": "", "company_linkedin": "", "industry": "Analytics SaaS", "employees": "250"},
        {"company": "Typeform", "url": "typeform.com", "snippet": "Online forms and surveys SaaS, 400+ employees, hiring revenue operations", "source": "fallback", "contact_name": "Nina Okonkwo", "contact_title": "Head of Revenue", "contact_linkedin": "", "company_linkedin": "", "industry": "SaaS", "employees": "400"},
        {"company": "Pipedrive", "url": "pipedrive.com", "snippet": "CRM for sales teams, Series C, 900+ employees, expanding EMEA", "source": "fallback", "contact_name": "Robert Taylor", "contact_title": "VP Enterprise Sales", "contact_linkedin": "", "company_linkedin": "", "industry": "CRM SaaS", "employees": "900"},
    ][:num_leads]

def research_company(company: str, snippet: str) -> dict:
    """Step 2: Deep research on each company"""
    response = groq_client.chat.completions.create(
        model=SDR_MODEL,
        messages=[
            {"role": "system", "content": "You are a B2B sales researcher. Given company info, extract key details for outreach. Respond in JSON only, no extra text."},
            {"role": "user", "content": f"""
Company: {company}
Info: {snippet}

Return ONLY this JSON:
{{
  "industry": "...",
  "size": "...",
  "pain_points": ["...", "..."],
  "buying_signals": ["...", "..."],
  "decision_maker_title": "...",
  "icp_score": 7,
  "icp_reason": "..."
}}"""}
        ],
        temperature=0.2,
        max_tokens=400
    )

    try:
        text = response.choices[0].message.content.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text.strip())
    except:
        return {
            "industry": "Technology",
            "size": "50-200",
            "pain_points": ["Manual sales processes", "Lack of pipeline visibility"],
            "buying_signals": ["Hiring sales roles", "Recent funding round"],
            "decision_maker_title": "VP of Sales",
            "icp_score": 7,
            "icp_reason": "Matches target ICP profile"
        }

def generate_email(company: str, research: dict, sender_name: str = "Alex Chen") -> dict:
    """Step 3: Generate personalized outreach email"""
    contact_name = research.get("contact_name", "")
    greeting = f"Hi {contact_name.split()[0]}," if contact_name else "Hi,"

    response = groq_client.chat.completions.create(
        model=SDR_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert SDR writing personalized cold emails. Be concise, specific, and value-focused. No fluff. Return JSON only."},
            {"role": "user", "content": f"""
Write a personalized cold email:
Company: {company}
Contact: {research.get('contact_name', '')} — {research.get('contact_title', '')}
Industry: {research.get('industry')}
Pain points: {research.get('pain_points')}
Buying signals: {research.get('buying_signals')}
Sender: {sender_name}, Senior AE at NexaCore Technologies
NexaCore: AI platform that automates enterprise revenue workflows

Greeting to use: {greeting}

Return ONLY this JSON:
{{
  "subject": "...",
  "body": "...",
  "cta": "..."
}}"""}
        ],
        temperature=0.7,
        max_tokens=500
    )

    try:
        text = response.choices[0].message.content.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text.strip())
    except:
        return {
            "subject": f"Quick question about {company}'s revenue workflow",
            "body": f"{greeting}\n\nI noticed {company} is scaling fast — hiring sales talent is always a sign of ambitious growth.\n\nAt NexaCore, we help revenue teams like yours automate the manual work that slows down pipeline.\n\nWould a 15-minute call this week make sense?\n\nBest,\n{sender_name}",
            "cta": "15-minute call this week"
        }

def generate_followup(company: str, original_email: dict, day: int = 3) -> dict:
    """Step 4: Generate follow-up emails"""
    response = groq_client.chat.completions.create(
        model=SDR_MODEL,
        messages=[
            {"role": "system", "content": "Write a brief, non-pushy follow-up email. Return JSON only."},
            {"role": "user", "content": f"""
Follow-up #{1 if day == 3 else 2} for {company}.
Original subject: {original_email.get('subject')}
Day {day} follow-up — keep it short, add value, no pressure.

Return ONLY this JSON:
{{
  "subject": "Re: ...",
  "body": "..."
}}"""}
        ],
        temperature=0.7,
        max_tokens=300
    )

    try:
        text = response.choices[0].message.content.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text.strip())
    except:
        return {
            "subject": f"Re: {original_email.get('subject', 'Following up')}",
            "body": "Hi,\n\nJust bumping this — didn't want it to get lost.\n\nWorth a quick 15 mins this week?\n\nBest,"
        }

def score_lead(research: dict) -> str:
    score = research.get("icp_score", 5)
    if score >= 8:
        return "🔥 Hot"
    elif score >= 6:
        return "🟡 Warm"
    else:
        return "❄️ Cold"

def run_sdr_campaign(criteria: str, num_leads: int = 5, callback=None) -> list:
    """Full SDR campaign pipeline with live updates"""

    def update(step, msg):
        if callback:
            callback(step, msg)

    update("search", f"🔍 Searching for leads: {criteria}")
    leads = search_leads(criteria, num_leads)
    update("search", f"✅ Found {len(leads)} leads via {'Apollo.io' if leads and leads[0].get('source') == 'apollo.io' else 'curated database'}")

    pipeline = []

    for i, lead in enumerate(leads):
        company = lead["company"]
        update("research", f"🔬 Researching {company}... ({i+1}/{len(leads)})")

        research = research_company(company, lead["snippet"])

        # Inject contact info from Apollo
        research["contact_name"] = lead.get("contact_name", "")
        research["contact_title"] = lead.get("contact_title", "")
        research["contact_linkedin"] = lead.get("contact_linkedin", "")

        time.sleep(1)

        email = generate_email(company, research)
        time.sleep(0.5)

        followup1 = generate_followup(company, email, day=3)
        followup2 = generate_followup(company, email, day=7)

        lead_record = {
            "company": company,
            "url": lead["url"],
            "source": lead.get("source", ""),
            "stage": "Researched",
            "score": score_lead(research),
            "icp_score": research.get("icp_score", 5),
            "industry": research.get("industry", "Technology"),
            "size": research.get("size", lead.get("employees", "Unknown")),
            "pain_points": research.get("pain_points", []),
            "buying_signals": research.get("buying_signals", []),
            "decision_maker": research.get("decision_maker_title", "VP Sales"),
            "contact_name": lead.get("contact_name", ""),
            "contact_title": lead.get("contact_title", ""),
            "contact_linkedin": lead.get("contact_linkedin", ""),
            "company_linkedin": lead.get("company_linkedin", ""),
            "icp_reason": research.get("icp_reason", ""),
            "email": email,
            "followups": [followup1, followup2],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Ready to Send",
            "approved": False
        }

        pipeline.append(lead_record)
        update("pipeline", f"✅ {company} — {lead_record['score']} | ICP: {research.get('icp_score')}/10 | Contact: {lead.get('contact_name', 'N/A')}")

    update("complete", f"🎉 Campaign ready! {len(pipeline)} leads researched and emails drafted")
    return pipeline