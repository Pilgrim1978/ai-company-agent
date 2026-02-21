import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

# Load API keys
load_dotenv()

# Set up clients
llm = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
search = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_company_ai_usage(company_name):
    """Search the web for how a company is using AI"""
    queries = [
        f"{company_name} artificial intelligence strategy 2024 2025",
        f"{company_name} AI use cases and initiatives",
        f"{company_name} machine learning generative AI adoption"
    ]
    
    all_results = ""
    for query in queries:
        results = search.search(query, max_results=3)
        for result in results["results"]:
            all_results += f"Source: {result['url']}\n"
            all_results += f"{result['content']}\n\n"
    
    return all_results

def summarize_with_llm(company_name, search_results):
    """Send search results to DeepSeek to generate 10 bullet points"""
    prompt = f"""Based on the following search results, summarize how {company_name} 
is currently using AI in exactly 10 bullet points.

Rules:
- Each bullet point should cover a distinct AI use case or initiative
- Be specific — mention product names, tools, or technologies where possible
- Focus on current and recent initiatives (2024-2025)
- If you don't have enough info for 10 distinct points, note that clearly

Search Results:
{search_results}
"""

    response = llm.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a research analyst who summarizes how companies are using AI. Be concise, specific, and factual."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content

# --- Streamlit UI starts here ---

# Page configuration
st.set_page_config(
    page_title="AI Company Research Agent",
    page_icon="🏢",
    layout="centered"
)

# Title and description
st.title("🏢 AI Company Research Agent")
st.markdown("Enter a company name to discover how they're using AI today.")

# Divider
st.divider()

# Input field
company = st.text_input("Company Name", placeholder="e.g. Google, JPMorgan, Tesla...")

# Search button
if st.button("🔍 Research", type="primary"):
    if not company.strip():
        st.warning("Please enter a company name.")
    else:
        # Step 1: Search
        with st.spinner(f"Searching the web for {company}'s AI initiatives..."):
            search_results = search_company_ai_usage(company)
        
        # Step 2: Summarize
        with st.spinner("Analyzing with AI..."):
            summary = summarize_with_llm(company, search_results)
        
        # Step 3: Display
        st.success("Research complete!")
        st.markdown(f"### How {company} is using AI")
        st.markdown(summary)

# Footer
st.divider()
st.caption("Powered by DeepSeek + Tavily | Built by Ankur")