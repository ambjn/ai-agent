import asyncio
from datetime import datetime
from functools import partial
from typing import Dict, Any

from groq import Groq

from models.agents.cto_agent import CTOAgent
from models.agents.growth_agent import GrowthAgent
from models.agents.product_agent import ProductAgent
from models.data_class.project_input import ProjectInput


class PrimaryAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.cto = CTOAgent(api_key)
        self.growth = GrowthAgent(api_key)
        self.product = ProductAgent(api_key)
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"

    async def _get_consolidated_analysis(self,
                                       analyses: Dict[str, Any],
                                       project: ProjectInput) -> str:
        consolidation_prompt = f"""
        As a business strategy advisor, review and consolidate these department analyses
        for the following project:

        Project Overview:
        {project.project_description}

        Department Analyses:
        CTO Analysis: {analyses['cto']}
        Growth Analysis: {analyses['growth']}
        Product Analysis: {analyses['product']}

        Provide a consolidated recommendation addressing:
        1. Key agreements and conflicts between departments
        2. Priority recommendations
        3. Risk factors and mitigation strategies
        4. Resource allocation suggestions
        5. Timeline and milestone recommendations
        6. Success metrics and KPIs

        Format the response in clear sections with specific, actionable recommendations.
        """

        messages = [
            {
                "role": "system",
                "content": "You are a senior business advisor providing strategic recommendations based on multi-department analyses."
            },
            {"role": "user", "content": consolidation_prompt}
        ]

        # Run the synchronous Groq API call in a thread pool
        loop = asyncio.get_event_loop()
        completion = await loop.run_in_executor(
            None,
            partial(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
        )

        return completion.choices[0].message.content

    async def analyze_project(self, project: ProjectInput) -> Dict[str, Any]:
        """Get analyses from all agents and consolidate recommendations"""

        # Gather analyses from all agents concurrently
        analyses = await asyncio.gather(
            self.cto.analyze(project),
            self.growth.analyze(project),
            self.product.analyze(project)
        )

        department_analyses = {
            "cto": analyses[0],
            "growth": analyses[1],
            "product": analyses[2]
        }

        # Get consolidated recommendations
        consolidated = await self._get_consolidated_analysis(department_analyses, project)

        return {
            "department_analyses": department_analyses,
            "consolidated_recommendation": consolidated,
            "timestamp": datetime.now().isoformat()
        }

