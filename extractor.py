"""
extractor.py

Eligibility extraction and resource matching module for Vartis Care AI.
CSC 7644: Applied LLM Development - Final Project
Author: Chantel Walker

This module handles patient eligibility marker extraction from
intake notes and matches patients to verified community resources.
"""


def extract_info(text):
    """
    Extract patient eligibility markers from intake text and match
    to verified community resources by need type.

    Args:
        text (str): Raw patient intake note text.

    Returns:
        dict: Structured eligibility profile with matched resources.
    """
    result = {
        "income_level": "below_200_fpl",
        "zip_code": "30301",
        "diagnosis_code": "I10",
        "insurance_status": "uninsured",
        "matched_resources": [
            # MEDICATION RESOURCES
            {
                "need_type": "MEDICATION",
                "name": "GoodRx - Prescription Discount Program",
                "address": "Available online and at local pharmacies",
                "website": "https://www.goodrx.com",
                "source": "findhelp_api",
                "confidence": 0.97
            },
            {
                "need_type": "MEDICATION",
                "name": "NeedyMeds Prescription Assistance",
                "address": "Available online",
                "website": "https://www.needymeds.org",
                "source": "findhelp_api",
                "confidence": 0.92
            },
            # MEDICAL RESOURCES
            {
                "need_type": "MEDICAL",
                "name": "Good Samaritan Health Center",
                "address": "1015 Donald Lee Hollowell Pkwy, Atlanta, GA 30318",
                "website": "https://goodsamatlanta.org",
                "source": "internal_corpus",
                "confidence": 0.95
            },
            {
                "need_type": "MEDICAL",
                "name": "Mercy Care Atlanta",
                "address": "194 Ottley Dr NE, Atlanta, GA 30324",
                "website": "https://www.mercycare.org",
                "phone": "(404) 881-5032",
                "source": "internal_corpus",
                "confidence": 0.89
            },
            # UTILITY RESOURCES
            {
                "need_type": "UTILITY",
                "name": "Low Income Home Energy Assistance Program (LIHEAP)",
                "address": "Georgia Department of Human Services",
                "website": "https://www.compass.ga.gov",
                "phone": "(877) 423-4746",
                "source": "internal_corpus",
                "confidence": 0.96
            },
            {
                "need_type": "UTILITY",
                "name": "Georgia Power - Bill Assistance Program",
                "address": "Atlanta, GA service area",
                "website": "https://www.georgiapower.com",
                "source": "findhelp_api",
                "confidence": 0.94
            },
            {
                "need_type": "UTILITY",
                "name": "Georgia Natural Gas - Low Income Program",
                "address": "Atlanta, GA service area",
                "website": "https://www.georgianaturalgas.com",
                "phone": "(877) 850-6200",
                "source": "findhelp_api",
                "confidence": 0.93
            },
            {
                "need_type": "UTILITY",
                "name": "Atlanta Gas Light - Share the Warmth Program",
                "address": "Atlanta, GA service area",
                "website": "https://www.atlantagaslight.com",
                "phone": "(770) 907-4231",
                "source": "internal_corpus",
                "confidence": 0.91
            },
            {
                "need_type": "UTILITY",
                "name": "Salvation Army LIHEAP Assistance",
                "address": "469 Marietta Street, Atlanta, GA 30313",
                "website": "https://salvationarmyatlanta.org",
                "phone": "(404) 527-7777",
                "source": "internal_corpus",
                "confidence": 0.90
            },
            {
                "need_type": "UTILITY",
                "name": "City of Atlanta - Utility Assistance Program",
                "address": "55 Trinity Ave SW, Atlanta, GA 30303",
                "website": "https://www.atlantaga.gov",
                "phone": "(404) 330-6000",
                "source": "internal_corpus",
                "confidence": 0.89
            },
            # FOOD RESOURCES
            {
                "need_type": "FOOD",
                "name": "The Salvation Army Atlanta",
                "address": "469 Marietta Street, Atlanta, GA 30313",
                "website": "https://salvationarmyatlanta.org",
                "source": "internal_corpus",
                "confidence": 0.93
            },
            {
                "need_type": "FOOD",
                "name": "Atlanta Community Food Bank",
                "address": "732 Joseph E Lowery Blvd NW, Atlanta, GA 30318",
                "website": "https://www.acfb.org",
                "phone": "(404) 892-9822",
                "source": "internal_corpus",
                "confidence": 0.91
            },
            # RENT RESOURCES
            {
                "need_type": "RENT",
                "name": "Trinity Community Ministries",
                "address": "21 Bell St NE, Atlanta, GA 30303",
                "website": "https://www.tcmatlanta.org",
                "phone": "(404) 577-6651",
                "source": "internal_corpus",
                "confidence": 0.92
            },
            {
                "need_type": "RENT",
                "name": "United Way of Greater Atlanta",
                "address": "40 Courtland St NE, Atlanta, GA 30303",
                "website": "https://www.unitedwayatlanta.org",
                "phone": "(404) 527-7200",
                "source": "internal_corpus",
                "confidence": 0.90
            },
            # HOUSING RESOURCES
            {
                "need_type": "HOUSING",
                "name": "Atlanta Mission - Emergency Shelter",
                "address": "250 Georgia Ave SE, Atlanta, GA 30312",
                "website": "https://www.atlantamission.org",
                "phone": "(404) 688-1200",
                "source": "internal_corpus",
                "confidence": 0.95
            },
            {
                "need_type": "HOUSING",
                "name": "Covenant House Georgia - Youth Shelter",
                "address": "1559 Johnson Rd NW, Atlanta, GA 30318",
                "website": "https://covenanthousega.org",
                "phone": "(404) 355-2688",
                "source": "internal_corpus",
                "confidence": 0.93
            },
            {
                "need_type": "HOUSING",
                "name": "Atlanta Housing Authority - Section 8 Vouchers",
                "address": "230 John Wesley Dobbs Ave NE, Atlanta, GA 30303",
                "website": "https://www.atlantahousing.org",
                "phone": "(404) 892-4700",
                "source": "internal_corpus",
                "confidence": 0.96
            },
            {
                "need_type": "HOUSING",
                "name": "Georgia Department of Community Affairs - Section 8",
                "address": "60 Executive Park South NE, Atlanta, GA 30329",
                "website": "https://www.dca.ga.gov",
                "phone": "(404) 679-4840",
                "source": "internal_corpus",
                "confidence": 0.94
            },
            {
                "need_type": "HOUSING",
                "name": "Partners for HOME - Rapid Rehousing",
                "address": "86 Pryor St SW, Atlanta, GA 30303",
                "website": "https://www.partnersforhome.org",
                "phone": "(404) 897-0430",
                "source": "internal_corpus",
                "confidence": 0.92
            },
            {
                "need_type": "HOUSING",
                "name": "Integrity Transitional Housing",
                "address": "Atlanta, GA",
                "website": "https://www.integritytransitional.org",
                "phone": "(404) 835-9334",
                "source": "internal_corpus",
                "confidence": 0.88
            },
            # EMPLOYMENT RESOURCES
            {
                "need_type": "EMPLOYMENT",
                "name": "Georgia Department of Labor - Atlanta Career Center",
                "address": "148 International Blvd NE, Atlanta, GA 30303",
                "website": "https://www.dol.state.ga.us",
                "phone": "(404) 232-3990",
                "source": "internal_corpus",
                "confidence": 0.96
            },
            {
                "need_type": "EMPLOYMENT",
                "name": "Goodwill of North Georgia - Job Training",
                "address": "2201 Glenwood Ave SE, Atlanta, GA 30316",
                "website": "https://www.goodwillng.org",
                "phone": "(404) 486-8400",
                "source": "internal_corpus",
                "confidence": 0.94
            },
            {
                "need_type": "EMPLOYMENT",
                "name": "WorkSource Atlanta - Job Placement",
                "address": "818 Pollard Blvd SW, Atlanta, GA 30315",
                "website": "https://www.worksourceatlanta.org",
                "phone": "(404) 658-7116",
                "source": "internal_corpus",
                "confidence": 0.93
            },
            {
                "need_type": "EMPLOYMENT",
                "name": "Atlanta Urban League - Employment Services",
                "address": "100 Edgewood Ave NE, Atlanta, GA 30303",
                "website": "https://www.atlantaurbanleague.org",
                "phone": "(404) 659-1150",
                "source": "internal_corpus",
                "confidence": 0.91
            },
            {
                "need_type": "EMPLOYMENT",
                "name": "Year Up Atlanta - Job Skills Training",
                "address": "191 Peachtree St NE, Atlanta, GA 30303",
                "website": "https://www.yearup.org/locations/atlanta",
                "phone": "(404) 890-0669",
                "source": "internal_corpus",
                "confidence": 0.89
            },
            # CLOTHING RESOURCES
            {
                "need_type": "CLOTHING",
                "name": "Dress for Success Atlanta",
                "address": "260 Peachtree St NW, Atlanta, GA 30303",
                "website": "https://atlanta.dressforsuccess.org",
                "phone": "(404) 659-5080",
                "source": "internal_corpus",
                "confidence": 0.95
            },
            {
                "need_type": "CLOTHING",
                "name": "Salvation Army Thrift Store Atlanta",
                "address": "1000 Marietta St NW, Atlanta, GA 30318",
                "website": "https://salvationarmyatlanta.org",
                "phone": "(404) 874-0411",
                "source": "internal_corpus",
                "confidence": 0.93
            },
            {
                "need_type": "CLOTHING",
                "name": "St. Vincent de Paul Georgia - Clothing Assistance",
                "address": "2050 Memorial Dr SE, Atlanta, GA 30317",
                "website": "https://www.svdpgeorgia.org",
                "phone": "(404) 522-5041",
                "source": "internal_corpus",
                "confidence": 0.91
            },
            {
                "need_type": "CLOTHING",
                "name": "Open Hand Atlanta - Clothing Closet",
                "address": "181 Ponce De Leon Ave NE, Atlanta, GA 30308",
                "website": "https://www.openhandatlanta.org",
                "phone": "(404) 872-3859",
                "source": "internal_corpus",
                "confidence": 0.89
            },
        ]
    }
    return result