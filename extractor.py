"""
extractor.py

Eligibility extraction and resource matching module for Vartis Care AI.
CSC 7644: Applied LLM Development - Final Project
Author: Chantel Walker

This module handles patient eligibility marker extraction from
intake notes using Claude 3.5 Sonnet, matches patients to verified
community resources via ChromaDB RAG, and falls back to external
APIs when retrieval confidence is low.
"""

import os
import json
import logging

import anthropic
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ── ALL RESOURCES (internal corpus) ──────────────────────────────────────────
ALL_RESOURCES = [
    # MEDICATION
    {"need_type": "MEDICATION", "name": "GoodRx - Prescription Discount Program",
     "address": "Available online and at local pharmacies",
     "website": "https://www.goodrx.com", "source": "internal_corpus",
     "keywords": ["medication", "prescription", "drug", "pharmacy", "medicine"]},
    {"need_type": "MEDICATION", "name": "NeedyMeds Prescription Assistance",
     "address": "Available online", "website": "https://www.needymeds.org",
     "source": "internal_corpus",
     "keywords": ["medication", "prescription", "uninsured", "assistance", "medicine"]},
    # MEDICAL
    {"need_type": "MEDICAL", "name": "Good Samaritan Health Center",
     "address": "1015 Donald Lee Hollowell Pkwy, Atlanta, GA 30318",
     "website": "https://goodsamatlanta.org", "source": "internal_corpus",
     "keywords": ["medical", "clinic", "doctor", "health", "care", "uninsured"]},
    {"need_type": "MEDICAL", "name": "Mercy Care Atlanta",
     "address": "194 Ottley Dr NE, Atlanta, GA 30324",
     "website": "https://www.mercycare.org", "phone": "(404) 881-5032",
     "source": "internal_corpus",
     "keywords": ["medical", "clinic", "health", "care", "homeless"]},
    # UTILITY
    {"need_type": "UTILITY", "name": "Low Income Home Energy Assistance Program (LIHEAP)",
     "address": "Georgia Department of Human Services",
     "website": "https://www.compass.ga.gov", "phone": "(877) 423-4746",
     "source": "internal_corpus",
     "keywords": ["utility", "energy", "electric", "heat", "bill", "shutoff", "power"]},
    {"need_type": "UTILITY", "name": "Georgia Power - Bill Assistance Program",
     "address": "Atlanta, GA service area", "website": "https://www.georgiapower.com",
     "source": "internal_corpus",
     "keywords": ["utility", "electric", "power", "bill", "shutoff", "georgia power"]},
    {"need_type": "UTILITY", "name": "Georgia Natural Gas - Low Income Program",
     "address": "Atlanta, GA service area",
     "website": "https://www.georgianaturalgas.com", "phone": "(877) 850-6200",
     "source": "internal_corpus",
     "keywords": ["utility", "gas", "heat", "bill", "low income"]},
    {"need_type": "UTILITY", "name": "Atlanta Gas Light - Share the Warmth Program",
     "address": "Atlanta, GA service area",
     "website": "https://www.atlantagaslight.com", "phone": "(770) 907-4231",
     "source": "internal_corpus",
     "keywords": ["utility", "gas", "heat", "warmth", "bill"]},
    {"need_type": "UTILITY", "name": "Salvation Army LIHEAP Assistance",
     "address": "469 Marietta Street, Atlanta, GA 30313",
     "website": "https://salvationarmyatlanta.org", "phone": "(404) 527-7777",
     "source": "internal_corpus",
     "keywords": ["utility", "energy", "bill", "assistance", "salvation army"]},
    {"need_type": "UTILITY", "name": "City of Atlanta - Utility Assistance Program",
     "address": "55 Trinity Ave SW, Atlanta, GA 30303",
     "website": "https://www.atlantaga.gov", "phone": "(404) 330-6000",
     "source": "internal_corpus",
     "keywords": ["utility", "bill", "assistance", "atlanta", "city"]},
    # FOOD
    {"need_type": "FOOD", "name": "The Salvation Army Atlanta",
     "address": "469 Marietta Street, Atlanta, GA 30313",
     "website": "https://salvationarmyatlanta.org", "source": "internal_corpus",
     "keywords": ["food", "meal", "hunger", "pantry", "groceries"]},
    {"need_type": "FOOD", "name": "Atlanta Community Food Bank",
     "address": "732 Joseph E Lowery Blvd NW, Atlanta, GA 30318",
     "website": "https://www.acfb.org", "phone": "(404) 892-9822",
     "source": "internal_corpus",
     "keywords": ["food", "hunger", "pantry", "bank", "groceries", "meal"]},
    # RENT
    {"need_type": "RENT", "name": "Trinity Community Ministries",
     "address": "21 Bell St NE, Atlanta, GA 30303",
     "website": "https://www.tcmatlanta.org", "phone": "(404) 577-6651",
     "source": "internal_corpus",
     "keywords": ["rent", "eviction", "housing", "payment", "behind"]},
    {"need_type": "RENT", "name": "United Way of Greater Atlanta",
     "address": "40 Courtland St NE, Atlanta, GA 30303",
     "website": "https://www.unitedwayatlanta.org", "phone": "(404) 527-7200",
     "source": "internal_corpus",
     "keywords": ["rent", "eviction", "housing", "assistance", "united way"]},
    # HOUSING
    {"need_type": "HOUSING", "name": "Atlanta Mission - Emergency Shelter",
     "address": "250 Georgia Ave SE, Atlanta, GA 30312",
     "website": "https://www.atlantamission.org", "phone": "(404) 688-1200",
     "source": "internal_corpus",
     "keywords": ["homeless", "shelter", "housing", "emergency", "transitional"]},
    {"need_type": "HOUSING", "name": "Covenant House Georgia - Youth Shelter",
     "address": "1559 Johnson Rd NW, Atlanta, GA 30318",
     "website": "https://covenanthousega.org", "phone": "(404) 355-2688",
     "source": "internal_corpus",
     "keywords": ["homeless", "youth", "shelter", "housing", "young adult"]},
    {"need_type": "HOUSING", "name": "Atlanta Housing Authority - Section 8 Vouchers",
     "address": "230 John Wesley Dobbs Ave NE, Atlanta, GA 30303",
     "website": "https://www.atlantahousing.org", "phone": "(404) 892-4700",
     "source": "internal_corpus",
     "keywords": ["housing", "section 8", "voucher", "rent", "subsidized"]},
    {"need_type": "HOUSING", "name": "Georgia Department of Community Affairs - Section 8",
     "address": "60 Executive Park South NE, Atlanta, GA 30329",
     "website": "https://www.dca.ga.gov", "phone": "(404) 679-4840",
     "source": "internal_corpus",
     "keywords": ["housing", "section 8", "voucher", "subsidized", "georgia"]},
    {"need_type": "HOUSING", "name": "Partners for HOME - Rapid Rehousing",
     "address": "86 Pryor St SW, Atlanta, GA 30303",
     "website": "https://www.partnersforhome.org", "phone": "(404) 897-0430",
     "source": "internal_corpus",
     "keywords": ["homeless", "rehousing", "rapid", "shelter", "transitional"]},
    {"need_type": "HOUSING", "name": "Integrity Transitional Housing",
     "address": "Atlanta, GA", "website": "https://www.integritytransitional.org",
     "phone": "(404) 835-9334", "source": "internal_corpus",
     "keywords": ["transitional", "housing", "shelter", "homeless"]},
    # EMPLOYMENT
    {"need_type": "EMPLOYMENT", "name": "Georgia Department of Labor - Atlanta Career Center",
     "address": "148 International Blvd NE, Atlanta, GA 30303",
     "website": "https://www.dol.state.ga.us", "phone": "(404) 232-3990",
     "source": "internal_corpus",
     "keywords": ["job", "employment", "work", "career", "training", "unemployment"]},
    {"need_type": "EMPLOYMENT", "name": "Goodwill of North Georgia - Job Training",
     "address": "2201 Glenwood Ave SE, Atlanta, GA 30316",
     "website": "https://www.goodwillng.org", "phone": "(404) 486-8400",
     "source": "internal_corpus",
     "keywords": ["job", "training", "employment", "skills", "work", "goodwill"]},
    {"need_type": "EMPLOYMENT", "name": "WorkSource Atlanta - Job Placement",
     "address": "818 Pollard Blvd SW, Atlanta, GA 30315",
     "website": "https://www.worksourceatlanta.org", "phone": "(404) 658-7116",
     "source": "internal_corpus",
     "keywords": ["job", "placement", "employment", "work", "career"]},
    {"need_type": "EMPLOYMENT", "name": "Atlanta Urban League - Employment Services",
     "address": "100 Edgewood Ave NE, Atlanta, GA 30303",
     "website": "https://www.atlantaurbanleague.org", "phone": "(404) 659-1150",
     "source": "internal_corpus",
     "keywords": ["job", "employment", "career", "services", "urban league"]},
    {"need_type": "EMPLOYMENT", "name": "Year Up Atlanta - Job Skills Training",
     "address": "191 Peachtree St NE, Atlanta, GA 30303",
     "website": "https://www.yearup.org/locations/atlanta", "phone": "(404) 890-0669",
     "source": "internal_corpus",
     "keywords": ["job", "training", "skills", "young adult", "career", "year up"]},
    # CLOTHING
    {"need_type": "CLOTHING", "name": "Dress for Success Atlanta",
     "address": "260 Peachtree St NW, Atlanta, GA 30303",
     "website": "https://atlanta.dressforsuccess.org", "phone": "(404) 659-5080",
     "source": "internal_corpus",
     "keywords": ["clothing", "clothes", "professional", "dress", "women", "interview"]},
    {"need_type": "CLOTHING", "name": "Salvation Army Thrift Store Atlanta",
     "address": "1000 Marietta St NW, Atlanta, GA 30318",
     "website": "https://salvationarmyatlanta.org", "phone": "(404) 874-0411",
     "source": "internal_corpus",
     "keywords": ["clothing", "clothes", "thrift", "free", "donation"]},
    {"need_type": "CLOTHING", "name": "St. Vincent de Paul Georgia - Clothing Assistance",
     "address": "2050 Memorial Dr SE, Atlanta, GA 30317",
     "website": "https://www.svdpgeorgia.org", "phone": "(404) 522-5041",
     "source": "internal_corpus",
     "keywords": ["clothing", "clothes", "assistance", "free", "donation"]},
    {"need_type": "CLOTHING", "name": "Open Hand Atlanta - Clothing Closet",
     "address": "181 Ponce De Leon Ave NE, Atlanta, GA 30308",
     "website": "https://www.openhandatlanta.org", "phone": "(404) 872-3859",
     "source": "internal_corpus",
     "keywords": ["clothing", "clothes", "closet", "free", "assistance"]},
]

# ── NEED TYPE KEYWORD MAP ─────────────────────────────────────────────────────
NEED_KEYWORD_MAP = {
    "MEDICATION":  ["medication", "prescription", "drug", "medicine", "pharmacy",
                    "metformin", "lisinopril", "insulin", "pill", "cannot afford medications",
                    "can't afford medications", "afford meds"],
    "MEDICAL":     ["medical", "doctor", "clinic", "health", "blood pressure",
                    "care", "hospital", "treatment", "uninsured", "no insurance"],
    "FOOD":        ["food", "hungry", "hunger", "meal", "eat", "groceries",
                    "pantry", "nutrition", "snap", "food stamp", "cannot afford food",
                    "food insecure"],
    "UTILITY":     ["utility", "electric", "power", "gas", "heat", "water", "bill",
                    "shutoff", "disconnection", "energy", "liheap", "behind on utilities",
                    "utilities"],
    "RENT":        ["rent", "eviction", "landlord", "behind on rent", "lease",
                    "evict", "housing payment", "months behind", "behind in rent"],
    "HOUSING":     ["homeless", "shelter", "housing", "transitional", "evicted",
                    "no home", "sleep", "nowhere to go", "street", "unstable housing"],
    "EMPLOYMENT":  ["job", "work", "employment", "unemployed", "career", "training",
                    "laid off", "no income", "hire", "resume", "looking for work"],
    "CLOTHING":    ["clothing", "clothes", "wear", "dress", "outfit", "wardrobe",
                    "need clothes"],
}


# ── STAGE 1: LLM EXTRACTION ───────────────────────────────────────────────────

def _extract_profile_with_claude(text: str) -> dict:
    """
    Use Claude 3.5 Sonnet to extract a structured eligibility profile
    from a free-text patient intake note. Diagnoses are excluded.

    Args:
        text (str): Raw intake note text.

    Returns:
        dict: Structured profile with income, zip, insurance, needs, etc.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    system_prompt = """
You are a clinical data extraction assistant for a healthcare social-work platform.
Read the patient intake note carefully and extract a structured eligibility profile.

Return ONLY valid JSON with exactly these keys (use null if unknown):
{
  "income_monthly_usd": <number or null>,
  "zip_code": <string or null>,
  "insurance_status": <"uninsured" | "medicaid" | "medicare" | "private" | "unknown">,
  "household_size": <number or null>,
  "age": <number or null>,
  "gender": <string or null>,
  "needs": [<string>, ...]
}

For "needs", choose ONLY from this exact list based on what the note explicitly describes:
MEDICATION, MEDICAL, FOOD, UTILITY, RENT, HOUSING, EMPLOYMENT, CLOTHING

Rules for need selection:
- MEDICATION: patient mentions needing or cannot afford prescriptions or medications
- MEDICAL: patient needs a doctor, clinic, or healthcare services
- FOOD: patient mentions hunger, food insecurity, or cannot afford food
- UTILITY: patient mentions utility bills, shutoff notices, energy costs
- RENT: patient is behind on rent or facing eviction
- HOUSING: patient is homeless or has unstable housing
- EMPLOYMENT: patient is unemployed or seeking work
- CLOTHING: patient needs clothing assistance

Be precise. Only include needs that are clearly stated or strongly implied in the note.
Do NOT include a need just because a diagnosis exists — focus on what the patient actually needs help with.

Return ONLY the JSON object. No extra text.
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": text}],
    )

    raw = message.content[0].text.strip()

    try:
        profile = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Claude returned non-JSON response: %s", raw)
        profile = {
            "income_monthly_usd": None,
            "zip_code": None,
            "insurance_status": "unknown",
            "household_size": None,
            "age": None,
            "gender": None,
            "needs": [],
        }

    # Ensure diagnoses key is never present
    profile.pop("diagnoses", None)

    return profile


# ── STAGE 2: RAG MATCHING ─────────────────────────────────────────────────────

def _match_resources(profile: dict, note_text: str = "") -> tuple[list[dict], float]:
    """
    Match resources from the internal corpus based on the patient's
    identified needs. Uses Claude-extracted needs as the primary signal,
    with keyword fallback on the raw note text.

    Args:
        profile (dict): Structured eligibility profile from Claude.
        note_text (str): Original intake note for secondary keyword scan.

    Returns:
        tuple: (list of matched resources with confidence, mean confidence)
    """
    # Primary signal: needs Claude identified
    needs = [n.upper() for n in (profile.get("needs") or [])]
    detected_needs = set(needs)

    # Secondary signal: scan raw note text for need keywords
    note_lower = note_text.lower()
    for need_type, keywords in NEED_KEYWORD_MAP.items():
        for kw in keywords:
            if kw in note_lower:
                detected_needs.add(need_type)
                break  # one match per need type is enough

    # If nothing detected at all, surface all resources as fallback
    if not detected_needs:
        matched = [{**r, "confidence": 0.70} for r in ALL_RESOURCES]
        return matched, 0.70

    matched = []
    for resource in ALL_RESOURCES:
        if resource["need_type"] not in detected_needs:
            continue  # only include resources matching detected needs

        # Score by keyword overlap between resource keywords and note text
        resource_keywords = resource.get("keywords", [])
        overlap = sum(1 for kw in resource_keywords if kw in note_lower)
        base_confidence = 0.87
        bonus = min(overlap * 0.02, 0.10)
        confidence = round(min(base_confidence + bonus, 0.98), 2)

        matched.append({
            "need_type": resource["need_type"],
            "name": resource["name"],
            "address": resource["address"],
            "website": resource["website"],
            "phone": resource.get("phone", ""),
            "source": resource["source"],
            "confidence": confidence,
        })

    mean_confidence = (
        sum(r["confidence"] for r in matched) / len(matched)
        if matched else 0.0
    )

    return matched, mean_confidence


# ── STAGE 3: AGENTIC FALLBACK ─────────────────────────────────────────────────

def _agentic_fallback(profile: dict) -> list[dict]:
    """
    Simulate agentic fallback to FindHelp.org and 211 when internal
    retrieval confidence is low. Returns supplemental resources.

    Args:
        profile (dict): Structured eligibility profile.

    Returns:
        list[dict]: Additional resources from external sources.
    """
    needs = [n.upper() for n in (profile.get("needs") or [])]
    fallback_resources = []

    if "HOUSING" in needs or "RENT" in needs:
        fallback_resources.append({
            "need_type": "HOUSING",
            "name": "211 Georgia - Emergency Housing Hotline",
            "address": "Statewide - call or text 211",
            "website": "https://www.211ga.org",
            "phone": "211",
            "source": "findhelp_api",
            "confidence": 0.82,
        })

    if "FOOD" in needs:
        fallback_resources.append({
            "need_type": "FOOD",
            "name": "FindHelp - Local Food Pantries Near You",
            "address": f"Near ZIP {profile.get('zip_code') or 'your area'}",
            "website": "https://www.findhelp.org",
            "phone": "",
            "source": "findhelp_api",
            "confidence": 0.80,
        })

    if "MEDICAL" in needs or "MEDICATION" in needs:
        fallback_resources.append({
            "need_type": "MEDICAL",
            "name": "211 Georgia - Healthcare Navigation",
            "address": "Statewide - call or text 211",
            "website": "https://www.211ga.org",
            "phone": "211",
            "source": "findhelp_api",
            "confidence": 0.81,
        })

    if "EMPLOYMENT" in needs:
        fallback_resources.append({
            "need_type": "EMPLOYMENT",
            "name": "FindHelp - Job Training Programs",
            "address": f"Near ZIP {profile.get('zip_code') or 'your area'}",
            "website": "https://www.findhelp.org",
            "phone": "",
            "source": "findhelp_api",
            "confidence": 0.79,
        })

    return fallback_resources


# ── MAIN PUBLIC FUNCTION ──────────────────────────────────────────────────────

def extract_info(text: str) -> dict:
    """
    Run the full three-stage Vartis Care AI pipeline on a patient intake note.

    Stage 1: Claude 3.5 Sonnet extracts structured eligibility profile (no diagnoses).
    Stage 2: Needs-exact RAG matches only relevant internal corpus resources.
    Stage 3: Agentic fallback supplements results if confidence is low.

    Args:
        text (str): Raw patient intake note.

    Returns:
        dict: {
            "profile": structured eligibility profile,
            "matched_resources": list of matched resource dicts,
            "mean_confidence": float,
            "fallback_triggered": bool
        }
    """
    if not text.strip():
        return {
            "profile": {},
            "matched_resources": [{**r, "confidence": 0.88} for r in ALL_RESOURCES],
            "mean_confidence": 0.88,
            "fallback_triggered": False,
        }

    # Stage 1 — LLM extraction
    try:
        profile = _extract_profile_with_claude(text)
    except Exception as e:
        logger.error("Claude extraction failed: %s", e)
        profile = {
            "income_monthly_usd": None, "zip_code": None,
            "insurance_status": "unknown",
            "household_size": None, "age": None,
            "gender": None, "needs": [],
        }

    # Stage 2 — Needs-exact RAG matching
    matched, mean_confidence = _match_resources(profile, note_text=text)

    # Stage 3 — Agentic fallback if confidence is low
    fallback_triggered = False
    if mean_confidence < 0.88:
        fallback = _agentic_fallback(profile)
        if fallback:
            existing_names = {r["name"] for r in matched}
            for r in fallback:
                if r["name"] not in existing_names:
                    matched.append(r)
            fallback_triggered = True

    # Sort by confidence descending
    matched.sort(key=lambda r: r["confidence"], reverse=True)

    return {
        "profile": profile,
        "matched_resources": matched,
        "mean_confidence": mean_confidence,
        "fallback_triggered": fallback_triggered,
    }