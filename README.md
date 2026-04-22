# Vartis Care AI
### CSC 7644: Applied LLM Development | Final Project
**Author: Chantel Walker**

## Overview
Vartis Care AI is an AI-powered decision-support system that extracts
patient eligibility information from unstructured intake notes and
clinical documents and matches them to verified community resources
in real time. It is designed to help healthcare social workers and
patient navigators reduce manual search time and eliminate referral
dead-ends for vulnerable patients. This is the final project for
CSC 7644: Applied LLM Development at Louisiana State University.

## Key Features
- Extracts structured eligibility markers (income, zip code, diagnosis,
  insurance status) from text intake notes and scanned document images
- RAG pipeline grounded in a curated PDF corpus of hospital financial
  assistance protocols stored in ChromaDB
- Agentic fallback to FindHelp.org and 211 National Data Platform when
  internal retrieval confidence is low
- Human-in-the-loop review step before any referral reaches the patient
- Evaluation using DeepEval targeting 95% faithfulness and 80% recall

## Tech Stack and Architecture
- **Model:** Claude 3.5 Sonnet via Anthropic API
- **Vector Store:** ChromaDB (locally hosted)
- **External Tools:** FindHelp.org API, 211 National Data Platform,
  NPPES NPI Registry, ASPE Poverty Guidelines
- **Evaluation:** DeepEval
- **Language:** Python 3.10+

### Main Components
- `vartis_agent.py` - main entry point, handles CLI and coordinates pipeline
- `extractor.py` - eligibility extraction and resource matching logic
- `intake_sample.txt` - sample patient intake data for demonstration

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip
- An Anthropic API key (get one at console.anthropic.com)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
Copy the example env file and fill in your API key:
```bash
cp .env.example .env
```
Open .env and add your Anthropic API key:

## Running the Application
```bash
python vartis_agent.py --mode extract --input intake_sample.txt
```

### Expected Output
```json
{
  "income_level": "below_200_fpl",
  "zip_code": "30301",
  "diagnosis_code": "E11.9",
  "insurance_status": "uninsured",
  "matched_resources": [
    {
      "name": "Grady Health Financial Assistance",
      "source": "internal_corpus",
      "confidence": 0.94
    },
    {
      "name": "GoodRx Insulin Program",
      "source": "findhelp_api",
      "confidence": 0.88
    }
  ]
}
```

## Repository Organization
- `vartis_agent.py` - main entry point and CLI handler
- `extractor.py` - eligibility extraction and resource matching module
- `intake_sample.txt` - sample patient intake data for demonstration
- `requirements.txt` - all Python dependencies
- `.env.example` - template for environment variables
- `.gitignore` - files excluded from version control

## Attributions and Citations
- Anthropic Claude API: https://docs.anthropic.com
- ChromaDB: https://docs.trychroma.com
- DeepEval: https://docs.confident-ai.com
- FindHelp.org API: https://company.findhelp.com/api
- Lewis et al. (2020) RAG paper: https://arxiv.org/abs/2005.11401
- Hu et al. (2022) LoRA paper: https://arxiv.org/abs/2106.09685
- Liang et al. (2019) LLMs in healthcare: https://doi.org/10.1038/s41591-018-0335-9