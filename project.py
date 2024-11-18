import streamlit as st
import pandas as pd
import requests
import openai #type: ignore
import os
import gspread
from google.oauth2.service_account import Credentials

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY") 

# Google Sheets API setup
def google_sheets_authenticate():
    creds = Credentials.from_service_account_file(
        r"C:\Users\Shivansh\Downloads\breakoutai-441611-b5c92202fc12.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    return gspread.authorize(creds)

def fetch_search_results(query):
    api_key = os.getenv("SERPAPI_API_KEY")  # Make sure to set this in your environment
    url = f"https://serpapi.com/search.json?api_key={api_key}&q={query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching search results: {response.status_code}")
        return {}

def extract_information(entity, search_results, prompt):
    # Prepare the messages for the new API format
    messages = [
        {"role": "user", "content": f"{prompt} {search_results}"}
    ]
    
    # Call OpenAI API to extract information using the new method
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or any other model you want to use
            messages=messages
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error extracting information: {e}")
        return "Error"

def main():
    st.title("AI Agent for Information Retrieval")

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df)

    # Google Sheets connection
    st.write("Or connect to a Google Sheet:")
    sheet_url = st.text_input("Enter Google Sheet URL:")
    if st.button("Load Google Sheet"):
        try:
            gc = google_sheets_authenticate()
            sheet = gc.open_by_url(sheet_url)
            worksheet = sheet.get_worksheet(0)  # Get the first worksheet
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)
            st.write("Data Preview from Google Sheet:")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error loading Google Sheet: {e}")

    if 'df' in locals() and not df.empty:
        # Select main column
        column_names = df.columns.tolist()
        selected_column = st.selectbox("Select the main column", column_names)

        # Input custom prompt
        prompt = st.text_input("Enter your query (use {entity} as a placeholder):")

        if st.button("Fetch Information"):
            results = []
            for entity in df[selected_column]:
                query = prompt.replace("{entity}", str(entity))
                search_results = fetch_search_results(query)
                extracted_info = extract_information(entity, search_results, prompt)
                results.append({"Entity": entity, "Extracted Info": extracted_info})

            # Display results
            results_df = pd.DataFrame(results)
            st.write("Extracted Information:")
            st.dataframe(results_df)

            # Download results
            csv = results_df.to_csv(index=False)
            st.download_button("Download Results", csv, "extracted_info.csv", "text/csv")

if __name__ == "__main__":
    main()
