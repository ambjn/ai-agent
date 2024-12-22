from typing import Dict, Any

from models.agents.base_agent import BaseAgent
from models.data_class.project_input import ProjectInput
from models.roles.role import AgentRole


class ProductAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key, AgentRole.PRODUCT)

    def _get_system_prompt(self) -> str:
        return """You are a Product Manager focused on user needs, feature prioritization, 
        and product-market fit. Analyze:
        - User needs and pain points
        - Feature prioritization
        - Product roadmap
        - Success metrics
        - User experience
        - Market positioning"""

    async def analyze(self, project: ProjectInput) -> Dict[str, Any]:
        prompt = f"""
        Analyze product strategy for:
        Project: {project.project_description}
        Target Market: {project.target_market}
        Timeline: {project.timeline_months} months
        Goals: {', '.join(project.business_goals)}

        Provide product recommendations considering:
        1. Core features and MVP scope
        2. User experience priorities
        3. Product roadmap
        4. Success metrics
        5. Market positioning
        """
        return await self._get_analysis(prompt)

