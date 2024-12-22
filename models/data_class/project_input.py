from dataclasses import dataclass
from typing import List

@dataclass
class ProjectInput:
    tech_stack: List[str]
    budget: float
    project_description: str
    target_market: str
    user_base: int
    timeline_months: int
    team_size: int
    business_goals: List[str]