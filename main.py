import asyncio
import os

from dotenv import load_dotenv

from models.agents.primary_agent import PrimaryAgent
from models.data_class.project_input import ProjectInput


async def run_multi_agent_example():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")

    primary_agent = PrimaryAgent(api_key)

    project = ProjectInput(
        tech_stack=["React", "Node.js", "PostgreSQL", "AWS"],
        budget=500000,
        project_description="""
        Building a B2B SaaS platform for supply chain management with 
        real-time tracking, predictive analytics, and vendor management.
        """,
        target_market="Mid-size manufacturing companies",
        user_base=1000,
        timeline_months=12,
        team_size=15,
        business_goals=[
            "Reach 10,000 active users in 18 months",
            "Achieve $2M ARR by end of year 1",
            "Maintain 98% system uptime",
            "Reduce supply chain costs for clients by 20%"
        ]
    )

    return await primary_agent.analyze_project(project)


if __name__ == "__main__":
    load_dotenv(dotenv_path=".env")

    async def main():
        analysis = await run_multi_agent_example()
        print("\nConsolidated Recommendations:")
        print("============================")
        print(analysis["consolidated_recommendation"])

    asyncio.run(main())