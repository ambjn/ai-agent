from typing import Dict, Any

from models.agents.base_agent import BaseAgent
from models.data_class.project_input import ProjectInput
from models.roles.role import AgentRole


class CTOAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key, AgentRole.CTO)

    def _get_system_prompt(self) -> str:
        return """You are an experienced CTO analyzing technical feasibility, architecture, 
        and implementation challenges. Focus on:
        - Technical stack evaluation
        - Infrastructure requirements
        - Security considerations
        - Scalability analysis
        - Technical risk assessment
        - Resource requirements"""

    async def analyze(self, project: ProjectInput) -> Dict[str, Any]:
        prompt = f"""
        Analyze the technical aspects of:
        Project: {project.project_description}
        Tech Stack: {', '.join(project.tech_stack)}
        Budget: ${project.budget:,.2f}
        Scale: {project.user_base} users
        Timeline: {project.timeline_months} months
        Team Size: {project.team_size}

        Provide technical recommendations considering:
        1. Architecture and scalability
        2. Technical risks and mitigation
        3. Team composition and skills needed
        4. Infrastructure costs
        5. Security requirements
        """
        return await self._get_analysis(prompt)
