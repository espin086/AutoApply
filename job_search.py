from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()

async def main():
    # Get the API key directly from environment
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
        
    # Create the agent with minimal configuration
    agent = Agent(
        task=f"""
        1. Go to indeed.com. You need to login with my Google Account. 
        Use the email and password from the .env file.
        You need to click on the "Continue with Google" button.
           email: {os.environ.get("INDEED_EMAIL")}
           password: {os.environ.get("INDEED_PASSWORD")}
        2. Search for jobs with the title "Principal Machine Learning Engineer"
        3. Apply filters for:
           - Remote jobs only
           - Salary estimate of $200,000 or more per year
        4. Browse through the first page of results
        5. Save the job titles, companies, and links for the top 5 matches to a text file
        """,
        llm=ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.2,
            google_api_key=api_key,
        )
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main()) 