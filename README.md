# AI Information Retrieval Agent

## Project Description
A Streamlit application that automates information gathering by:
- Uploading CSV or connecting to Google Sheets
- Performing web searches for each entity
- Extracting structured information using AI
- Generating downloadable results

## Prerequisites
- Python 3.8+
- OpenAI API key
- SerpAPI key
- Google Cloud service account

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ai-information-retrieval.git
cd ai-information-retrieval
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

## Configuration

### Google Sheets Authentication
1. Create a Google Cloud service account
2. Download service account JSON
3. Update path in `google_sheets_authenticate()` function

## Usage

### Running the Application
```bash
streamlit run project.py
```

### Workflow
1. Upload CSV or connect Google Sheet
2. Select column for entity search
3. Enter custom query template
4. Click "Fetch Information"
5. Download results as CSV

## Required API Services
- OpenAI (GPT-3.5-turbo)
- SerpAPI (web search)
- Google Sheets API

## Customization
- Modify prompt template
- Change AI model
- Adjust search parameters

## Limitations
- Requires active API subscriptions
- Search results depend on SerpAPI
- Rate limits may apply
