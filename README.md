# Vartis Care AI
### CSC 7644: Applied LLM Development | Final Project

## Overview
Vartis Care AI is an AI-powered decision-support system that extracts 
patient eligibility information from unstructured intake notes and clinical 
documents and matches them to verified community resources in real time. 
It is designed to help healthcare social workers and patient navigators 
reduce manual search time and eliminate referral dead-ends for vulnerable 
patients.

## Key Features
- Extracts structured eligibility markers (income, zip code, diagnosis, 
  insurance status) from text intake notes and scanned document images
- RAG pipeline grounded in a curated PDF corpus of hospital financial 
  assistance protocols stored in ChromaDB
- Agentic fallback to FindHelp.org and 211 National Data Platform when 
  internal retrieval confidence is low
- Human-in-the-loop review step before any referral reaches the patient
- Evaluation using DeepEval targeting 95% faithfulness and 80% recall

## Tech Stack
- Model: Claude 3.5 Sonnet via Anthropic API
- Vector Store: ChromaDB (locally hosted)
- External Tools: FindHelp.org API, 211 National Data Platform, 
  NPPES NPI Registry, ASPE Poverty Guidelines
- Evaluation: DeepEval
- Language: Python 3.10+

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip
- An Anthropic API key

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

## Repository Organization
- `vartis_agent.py` - main application logic and eligibility extraction
- `intake_sample.txt` - sample patient intake data for demonstration
- `requirements.txt` - all Python dependencies
- `.env.example` - template for environment variables
- `README.md` - project documentation

## Attributions
- Anthropic Claude API: https://docs.anthropic.com
- ChromaDB: https://docs.trychroma.com
- DeepEval: https://docs.confident-ai.com
- FindHelp.org API: https://company.findhelp.com/api
- Lewis et al. (2020) RAG paper: https://arxiv.org/abs/2005.11401