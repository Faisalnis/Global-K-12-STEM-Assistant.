# agents/orchestrator_agent.py

import time
from typing import Any, Dict, List

from agents.curriculum_agent import CurriculumAgent
from agents.lesson_planner_agent import LessonPlannerAgent
from agents.robotics_agent import RoboticsAgent
from agents.assessment_agent import AssessmentAgent
from agents.career_agent import CareerAgent
from agents.parent_report_agent import ParentReportAgent

class OrchestratorAgent:
    """
    OrchestratorAgent sits at the top of the multi-agent hierarchy.
    It coordinates execution, routes inputs to the specialized sub-agents,
    and constructs a unified, structured learning package response.
    """

    def __init__(self):
        # Instantiate sub-agents
        self.curriculum_agent = CurriculumAgent()
        self.lesson_planner_agent = LessonPlannerAgent()
        self.robotics_agent = RoboticsAgent()
        self.assessment_agent = AssessmentAgent()
        self.career_agent = CareerAgent()
        self.parent_report_agent = ParentReportAgent()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes educational requirements by executing all sub-agents.
        
        Args:
            input_data (dict): Standard system inputs containing grade, subject,
                              topic, language, and custom prompt guidelines.
                              
        Returns:
            dict: Unified package containing curriculum, lesson, robotics,
                  assessment, career, and parent report results.
        """
        start_time = time.time()
        
        # Route to CurriculumAgent first to fetch alignments
        curriculum_result = self.curriculum_agent.run(input_data)
        
        # Extract standard alignments and format them for the prompt templates of other agents
        standards_list = curriculum_result.get("data", {}).get("standards_alignment", [])
        standards_formatted_str = ""
        if standards_list:
            standards_formatted_str = "\n".join([
                f"- {std.get('code')}: {std.get('description')}" 
                for std in standards_list if std.get('code') and std.get('description')
            ])
        else:
            standards_formatted_str = "No specific standards retrieved."

        # Propagate curriculum standard mappings to downstream agents
        enriched_input = dict(input_data)
        enriched_input["standards"] = standards_formatted_str

        # Route remaining agents with enriched context
        lesson_result = self.lesson_planner_agent.run(enriched_input)
        robotics_result = self.robotics_agent.run(enriched_input)
        assessment_result = self.assessment_agent.run(enriched_input)
        career_result = self.career_agent.run(enriched_input)
        parent_report_result = self.parent_report_agent.run(enriched_input)


        # Aggregate outputs
        aggregated_results = {
            "curriculum": curriculum_result.get("data", {}),
            "lesson_plan": lesson_result.get("data", {}),
            "robotics": robotics_result.get("data", {}),
            "assessment": assessment_result.get("data", {}),
            "careers": career_result.get("data", {}),
            "parent_report": parent_report_result.get("data", {})
        }

        execution_duration = time.time() - start_time

        return {
            "status": "success",
            "metadata": {
                "orchestrator_version": "1.0.0",
                "execution_time_seconds": round(execution_duration, 4),
                "grade": input_data.get("grade"),
                "subject": input_data.get("subject"),
                "topic": input_data.get("topic"),
                "language": input_data.get("language")
            },
            "results": aggregated_results
        }
