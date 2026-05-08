# Vartis Care AI

**CSC 7644: Applied LLM Development | Final Project**
**Author: Chantel Walker | Louisiana State University**

---

## Overview

Vartis Care AI is an AI-powered decision-support system that extracts patient eligibility information from unstructured intake notes and matches patients to verified community resources in real time. It is designed to help healthcare social workers and patient navigators reduce manual search time and eliminate referral dead-ends for vulnerable patients.

This is the final project for **CSC 7644: Applied LLM Development** at Louisiana State University.

---

## Application Screenshot

![Vartis Care AI — Application Screenshot](screenshot.png)

> The application features a patient information form, intake note upload, three-stage AI pipeline, matched resource cards, human-in-the-loop review, and a patient care note generator.

---

## Key Features

- **Patient Information Form** — Captures case ID, patient name, date of birth, ZIP code, insurance name, insurance ID, navigator, facility, and visit date before running the pipeline
- **Intake Note Upload** — Accepts `.txt` or `.pdf` intake notes via file upload or direct text paste
- **Stage 1 — LLM Extraction** — Claude 3.5 Sonnet extracts structured eligibility markers (income, ZIP code, insurance status, age, gender, household size, and identified needs) from unstructured intake notes
- **Stage 2 — RAG Retrieval** — Needs-exact keyword matching against a curated internal corpus of 29 verified community resources with confidence scoring
- **Stage 3 — Agentic Fallback** — Automatic fallback to FindHelp.org and 211 National Data Platform when internal retrieval confidence is below threshold
- **Human-in-the-Loop Review** — Social worker must approve or flag every referral before it reaches the patient
- **Patient Care Note Generator** — Select matched resources, add navigator comments, set priority level, and generate a formatted care note with full patient info that can be copied or downloaded as a `.txt` file
- **Resource Filtering** — Filter matched resources by need type, source, confidence level, and keyword search

---

## Tech Stack and Architecture

| Component | Technology |
|---|---|
| LLM | Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`) via Anthropic API |
| Frontend | Streamlit |
| Resource Matching | Keyword-based RAG (internal corpus) |
| External Fallback | FindHelp.org API simulation, 211 National Data Platform |
| Evaluation Target | DeepEval — 95% faithfulness, 80% recall |
| Language | Python 3.10+ |

### Pipeline Architecture

```
Patient Intake Note
       │
       ▼
┌─────────────────────┐
│  Stage 1            │  Claude 3.5 Sonnet extracts:
│  LLM Extraction     │  income, ZIP, insurance status,
│                     │  age, gender, household size, needs
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Stage 2            │  Needs-exact keyword matching
│  RAG Retrieval      │  against 29 verified resources
│                     │  with confidence scoring
└────────┬────────────┘
         │
         ▼ (if confidence < 88%)
┌─────────────────────┐
│  Stage 3            │  FindHelp.org + 211 National
│  Agentic Fallback   │  Data Platform supplemental
│                     │  resource retrieval
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Human-in-the-Loop  │  Social worker reviews and
│  Review             │  approves before referral
└─────────────────────┘
```

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- `pip`
- An Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Copy the example env file and fill in your API key:

```bash
cp .env.example .env
```

Open `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_actual_key_here
```

> **Never commit your `.env` file.** It is listed in `.gitignore` and will not be pushed to GitHub. The `.env.example` file is provided as a template.

---

## Running the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at:

```
http://localhost:8501
```

---

## How to Use the Application

1. **Fill in Patient Information** — Enter case ID, patient name, date of birth, ZIP code, insurance name, and navigator details in the form at the top
2. **Upload or Paste an Intake Note** — Upload a `.txt` or `.pdf` file, or paste the note directly into the text box
3. **Run the Pipeline** — Click the **Run Pipeline** button to trigger all three stages
4. **Review Extracted Profile** — The app displays the AI-extracted patient profile including income, insurance status, and identified needs
5. **Browse Matched Resources** — Resources are displayed by need type with confidence scores; use filters to narrow results
6. **Approve or Flag** — Use the human-in-the-loop review buttons to approve the referral or flag for additional review
7. **Generate Care Note** — Select resources, add navigator comments, choose a priority level, and click Generate to produce a formatted care note ready to download or paste into a patient record

---

## Expected Output

The pipeline returns matched community resources organized by need type:

- 💊 **Medication Assistance** — GoodRx, NeedyMeds
- 🏥 **Medical Care** — Good Samaritan Health Center, Mercy Care Atlanta
- ⚡ **Utility Assistance** — LIHEAP, Georgia Power, Georgia Natural Gas, Atlanta Gas Light, Salvation Army LIHEAP, City of Atlanta
- 🍎 **Food Assistance** — Salvation Army Atlanta, Atlanta Community Food Bank
- 🏠 **Rent Assistance** — Trinity Community Ministries, United Way of Greater Atlanta
- 🏘️ **Housing & Shelter** — Atlanta Mission, Covenant House, Atlanta Housing Authority Section 8, Georgia DCA Section 8, Partners for HOME, Integrity Transitional Housing
- 💼 **Employment Services** — Georgia Department of Labor, Goodwill of North Georgia, WorkSource Atlanta, Atlanta Urban League, Year Up Atlanta
- 👗 **Clothing Assistance** — Dress for Success Atlanta, Salvation Army Thrift Store, St. Vincent de Paul Georgia, Open Hand Atlanta

All resources include address, phone number, website, source, and confidence match score. Results are filterable by need type, source, confidence level, and keyword search.

The generated patient care note includes full patient information (case ID, name, DOB, ZIP, insurance), the extracted eligibility profile, all selected referred resources with contact details, and navigator comments.

---

## Repository Organization

```
vartis-care-ai/
├── app.py               # Main Streamlit application — UI, pipeline orchestration, care notes
├── extractor.py         # Eligibility extraction and resource matching (three-stage pipeline)
├── vartis_agent.py      # CLI entry point and pipeline coordinator
├── intake_sample.txt    # Sample patient intake note for demonstration
├── requirements.txt     # All Python dependencies
├── .env.example         # Template for environment variables (copy to .env and add your key)
├── .gitignore           # Files excluded from version control (.env is excluded)
└── README.md            # This file
```

---

## Attributions and Citations

- Anthropic Claude API: [https://docs.anthropic.com](https://docs.anthropic.com)
- Streamlit: [https://docs.streamlit.io](https://docs.streamlit.io)
- ChromaDB: [https://docs.trychroma.com](https://docs.trychroma.com)
- DeepEval: [https://docs.confident-ai.com](https://docs.confident-ai.com)
- FindHelp.org API: [https://company.findhelp.com/api](https://company.findhelp.com/api)
- Lewis et al. (2020) RAG paper: [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
- Hu et al. (2022) LoRA paper: [https://arxiv.org/abs/2106.09685](https://arxiv.org/abs/2106.09685)
- Liang et al. (2019) LLMs in healthcare: [https://doi.org/10.1038/s41591-018-0335-9](https://doi.org/10.1038/s41591-018-0335-9)
- Patient Advocate Foundation (design inspiration): [https://www.patientadvocate.org](https://www.patientadvocate.org)
