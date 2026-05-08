# Vartis Care AI
### CSC 7644: Applied LLM Development | Final Project
**Author: Chantel Walker | Louisiana State University | Spring 2026**

---

## Overview

Vartis Care AI is an AI-powered decision-support system that extracts
patient eligibility information from unstructured intake notes and clinical
documents and matches patients to verified community resources in real time.
It is designed to help healthcare social workers and patient navigators
reduce manual search time and eliminate referral dead-ends for vulnerable
patients. This is the final project for CSC 7644: Applied LLM Development
at Louisiana State University.

**GitHub Repository:**
https://github.com/Chantel-W-CodesLSU/csc7644-final-project-walker-VARTIS-AI

---

## Key Features

- Extracts structured eligibility markers (income level, zip code, diagnosis,
  insurance status, household size, urgency) from patient intake notes
- Matches patients to 28 verified Atlanta-area community resources across
  8 need categories: Medication, Medical, Food, Utility, Rent, Housing,
  Employment, and Clothing
- Filters resources by need type, source, confidence score, phone availability,
  and keyword search
- Color-coded professional resource cards with confidence scores, addresses,
  phone numbers, and clickable website links
- Patient profile panel with name, date of birth, zip code, income level,
  insurance status, household size, urgency level, and case reference number
- Human-in-the-loop advocate review interface with approval checkboxes
  before any referral reaches the patient
- Simulated patient chart upload with advocate notes documentation
- RAG pipeline architecture backed by ChromaDB vector store (full
  integration in next development phase)
- Agentic fallback to FindHelp.org and 211 National Data Platform planned
  for production deployment

---

## Tech Stack and Architecture

### Models and APIs
- **Model:** Claude 3.5 Sonnet via Anthropic API
  (claude-3-5-sonnet-20241022)
- **External APIs (planned):** FindHelp.org, 211 National Data Platform,
  NPPES NPI Registry, ASPE Poverty Guidelines, RxUtility API

### Frameworks and Libraries
- **Frontend:** Streamlit with custom HTML and CSS
- **Vector Store:** ChromaDB (locally hosted)
- **Evaluation:** DeepEval (faithfulness and contextual recall)
- **Language:** Python 3.10+

### Main Components
- `app.py` - Streamlit web interface, patient profile form, resource
  display, advocate review workflow
- `extractor.py` - Eligibility extraction and resource matching logic,
  structured resource corpus
- `vartis_agent.py` - Command-line entry point and pipeline coordinator
- `intake_sample.txt` - Sample de-identified patient intake note

### Architecture Flow
```
Patient Intake Note / Document Image
          |
  Claude 3.5 Sonnet (Multimodal Extraction)
          |
  Structured JSON Eligibility Profile
  (income, zip, diagnosis, insurance)
          |
       RAG Router
      /           \
ChromaDB         FindHelp.org / 211 API / NPPES
(PDF Corpus)       (Agentic Fallback)
          |
  Ranked Recommendations + Source Citations
          |
  Advocate Review UI (Human-in-the-Loop)
          |
  Approved Referral Delivered to Patient
```

---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip
- An Anthropic API key (get one at https://console.anthropic.com)
- Windows, macOS, or Linux

### Step 1: Clone the Repository
```bash
git clone https://github.com/Chantel-W-CodesLSU/csc7644-final-project-walker-VARTIS-AI.git
cd csc7644-final-project-walker-VARTIS-AI
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy the example environment file and add your API key:
```bash
cp .env.example .env
```

Open `.env` and fill in your Anthropic API key:
```
ANTHROPIC_API_KEY=your_key_here
```

> Note: Never commit your `.env` file. It is already listed in `.gitignore`.

---

## Running the Application

### Option 1: Streamlit Web Interface (Recommended)
```bash
streamlit run app.py
```
The app opens automatically in your browser at:
```
http://localhost:8501
```

**How to use the app:**
1. Fill in the Patient Profile fields at the top
2. Use the filter panel to narrow resources by need type, source,
   or confidence score
3. Review the matched community resources on the right
4. Add advocate notes in the notes panel at the bottom
5. Check all three approval boxes and click Upload to Patient Chart

### Option 2: Command Line Interface
```bash
python vartis_agent.py --mode extract --input intake_sample.txt
```

**Expected output:**
```json
{
  "income_level": "below_200_fpl",
  "zip_code": "30301",
  "diagnosis_code": "I10",
  "insurance_status": "uninsured",
  "matched_resources": [
    {
      "need_type": "MEDICATION",
      "name": "GoodRx - Prescription Discount Program",
      "address": "Available online and at local pharmacies",
      "website": "https://www.goodrx.com",
      "source": "findhelp_api",
      "confidence": 0.97
    }
  ]
}
```

---

## Repository Organization

```
csc7644-final-project-walker-VARTIS-AI/
|
|- app.py                 # Streamlit web interface, patient profile,
|                         # resource display, advocate review workflow
|
|- extractor.py           # Eligibility extraction and resource matching,
|                         # structured corpus of 28 verified resources
|
|- vartis_agent.py        # Command-line entry point and pipeline
|                         # coordinator
|
|- intake_sample.txt      # Sample de-identified patient intake note
|                         # for demonstration
|
|- requirements.txt       # All Python dependencies
|
|- .env.example           # Template for environment variables
|                         # (copy to .env and fill in API key)
|
|- .gitignore             # Files excluded from version control
|                         # (includes .env, API keys, media files)
|
|- README.md              # Project documentation (this file)
```

---

## Expected Output

The system returns a structured eligibility profile with matched community
resources organized by need type including:

- MEDICATION: GoodRx, NeedyMeds
- MEDICAL: Good Samaritan Health Center, Mercy Care Atlanta
- UTILITY: LIHEAP, Georgia Power, Georgia Natural Gas, Atlanta Gas Light,
  Salvation Army LIHEAP, City of Atlanta Utility Assistance
- FOOD: The Salvation Army Atlanta, Atlanta Community Food Bank
- RENT: Trinity Community Ministries, United Way of Greater Atlanta
- HOUSING: Atlanta Mission, Covenant House Georgia, Atlanta Housing
  Authority Section 8, Georgia DCA Section 8, Partners for HOME,
  Integrity Transitional Housing
- EMPLOYMENT: Georgia Department of Labor, Goodwill of North Georgia,
  WorkSource Atlanta, Atlanta Urban League, Year Up Atlanta
- CLOTHING: Dress for Success Atlanta, Salvation Army Thrift Store,
  St. Vincent de Paul Georgia, Open Hand Atlanta

All resources include address, phone number where available, website,
source, and confidence match score. Results are filterable by need type,
source, confidence level, phone availability, and keyword search.

---

## Attributions and Citations

- Anthropic Claude API Documentation:
  https://docs.anthropic.com/en/docs/about-claude/models

- ChromaDB Documentation:
  https://docs.trychroma.com

- DeepEval Documentation:
  https://docs.confident-ai.com

- Streamlit Documentation:
  https://docs.streamlit.io

- FindHelp.org API:
  https://company.findhelp.com/api

- Lewis, P., et al. (2020). Retrieval-augmented generation for
  knowledge-intensive NLP tasks. NeurIPS.
  https://arxiv.org/abs/2005.11401

- Hu, E. J., et al. (2022). LoRA: Low-rank adaptation of large
  language models. ICLR.
  https://arxiv.org/abs/2106.09685

- Liang, H., et al. (2019). Evaluation and accurate diagnoses of
  pediatric diseases using artificial intelligence. Nature Medicine.
  https://doi.org/10.1038/s41591-018-0335-9

---

## Notes on Scope

The current prototype demonstrates the full user interface and workflow
with a structured static resource corpus. Live Anthropic API extraction,
ChromaDB RAG retrieval, and external API agentic fallbacks are planned
for the next development phase. No real patient data is used at any
stage of development or evaluation.
