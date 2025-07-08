# IPL Data Analysis Dashboard

This project is a **Streamlit-based interactive web application** for analyzing **Indian Premier League (IPL)** data using Python, Pandas, and advanced visualizations. It includes natural language summaries powered by Google's Gemini API.

---

## ⚙️ Features

- Player performance analysis across seasons
- Team performance, head-to-head comparisons, and win statistics
- Batting stats: runs, strike rate, boundaries, and growth
- Bowling stats: economy, wickets, strike rate, and dot balls
- Interactive visualizations using Matplotlib, Seaborn, and Plotly
- Gemini-powered summaries with natural language prompts

---

## 📁 Project Structure

|── app.py # Streamlit main application
├── data_loader.py # IPL data loading functions
├── analysis.py # Data aggregation and processing
├── visualize.py # Plotting functions
├── llmutil.py # Gemini API integration
├── prompts.py # Prompt generation for summaries
├── requirements.txt # Python dependencies
├── .env (optional) # Local environment secrets (API key)
└── datasets/ # Folder containing IPL CSV files



---

## 🚀 How to Run the App

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/ipl-data-dashboard.git
cd ipl-data-dashboard

pip install -r requirements.txt

step 3 set data  set path
# Inside data_loader.py
DATA_PATH = "datasets/cleanandmerges.csv"


🔐 Gemini API Setup for Summarization
To enable Summarize buttons in the app, you need to add your Gemini API key.

✅ Step 1: Get a Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey

2. Sign in with your Google account

3. Click "Create API Key" and copy it

✅ Step 2A: Use .env File (For Local Use)

Paste your API key:
API_KEY=your_generated_gemini_api_key_here

Step 3: Run the App
streamlit run app.py
