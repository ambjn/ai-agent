from typing import Dict, Any

from models.agents.base_agent import BaseAgent
from models.data_class.project_input import ProjectInput
from models.roles.role import AgentRole


class GrowthAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key, AgentRole.GROWTH)

    def _get_system_prompt(self) -> str:
        return """You are a Growth Head focused on market expansion and user acquisition. 
        Analyze:
        - Market opportunity size
        - User acquisition strategies
        - Growth metrics and KPIs
        - Marketing channels
        - Competition analysis
        - Revenue projections"""

    async def analyze(self, project: ProjectInput) -> Dict[str, Any]:
        prompt = f"""
        Analyze growth potential for:
        Project: {project.project_description}
        Target Market: {project.target_market}
        Current User Base: {project.user_base}
        Goals: {', '.join(project.business_goals)}
        Budget: ${project.budget:,.2f}

        Provide growth strategy recommendations considering:
        1. Market sizing and opportunity
        2. User acquisition channels
        3. Growth metrics and targets
        4. Marketing budget allocation
        5. Competitive positioning
        """
        return await self._get_analysis(prompt)
