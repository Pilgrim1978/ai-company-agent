import os
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

# Load API keys from .env file
load_dotenv()

# Set up DeepSeek client (uses OpenAI-compatible API)
llm = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Set up Tavily search client
search = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_company_ai_usage(company_name):
    """Search the web for how a company is using AI"""
    print(f"\n🔍 Searching for how {company_name} is using AI...\n")
    
    # Run multiple searches to get better coverage
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
    print("🤖 Analyzing with DeepSeek...\n")
    
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

def run_agent():
    """Main agent loop"""
    print("=" * 50)
    print("🏢 AI Company Research Agent")
    print("=" * 50)
    
    while True:
        company = input("\nEnter a company name (or 'quit' to exit): ").strip()
        
        if company.lower() == "quit":
            print("👋 Goodbye!")
            break
        
        if not company:
            print("⚠️ Please enter a valid company name.")
            continue
        
        # Step 1: Search the web
        search_results = search_company_ai_usage(company)
        
        # Step 2: Summarize with LLM
        summary = summarize_with_llm(company, search_results)
        
        # Step 3: Display results
        print("=" * 50)
        print(f"📊 How {company} is using AI:")
        print("=" * 50)
        print(summary)
        print("=" * 50)

# Run the agent
if __name__ == "__main__":
    run_agent()