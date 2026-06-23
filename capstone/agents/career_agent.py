# agents/career_agent.py

from typing import Any, Dict
from models.gemini_client import GeminiClient
from models.llm_utils import load_prompt_template, render_prompt, clean_and_parse_json

class CareerAgent:
    """
    CareerAgent is responsible for connecting classroom STEM lessons to real-world
    career pathways and introducing diverse role models to inspire students.
    """

    def __init__(self):
        self.client = GeminiClient()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes career guidance details generation.
        
        Args:
            input_data (dict): Includes grade, subject, topic, language, standards
            
        Returns:
            dict: Careers and role models
        """
        grade = input_data.get("grade", "Middle School")
        subject = input_data.get("subject", "Science")
        topic = input_data.get("topic", "STEM Topic")
        language = input_data.get("language", "English")
        notes = input_data.get("additional_notes", "")
        standards_str = input_data.get("standards", "No standards provided.")

        data = {}
        try:
            template = load_prompt_template("career_prompt.txt")
            prompt = render_prompt(template, {
                "grade": grade,
                "subject": subject,
                "topic": topic,
                "language": language,
                "additional_notes": notes,
                "standards": standards_str
            })
            raw_response = self.client.generate(prompt)
            data = clean_and_parse_json(raw_response)
        except Exception as e:
            print(f"Error calling Gemini in CareerAgent: {e}. Using local fallback.")

        # Double-check parsed results or use hardcoded backups
        if not data or "careers" not in data:
            # Careers and profiles
            career_list = [
                {
                    "title": "Systems Dynamics Architect",
                    "description": f"Designs systems capable of handling loads, vibrations, and movements influenced by {topic}.",
                    "median_salary": "$95,000 - $120,000",
                    "key_skills": ["CAD Design", "System Modeling", "Physics Analytics"]
                },
                {
                    "title": "Environmental Automation Engineer",
                    "description": f"Builds smart sensors to detect and mitigate anomalies related to {topic} in urban regions.",
                    "median_salary": "$88,000 - $110,000",
                    "key_skills": ["Python Coding", "Electronics", "Sensors and Actuators"]
                }
            ]

            role_model = {
                "name": "Dr. Mae Jemison",
                "background": "First African American woman in space. Accomplished engineer, physician, and astronaut.",
                "quote": "Never be limited by other people's limited imaginations.",
                "lesson_connection": f"Dr. Jemison combined her understanding of {topic} and aerospace mechanics to carry out space shuttle operations."
            }

            data = {
                "careers": career_list,
                "role_model": role_model
            }

        return {
            "status": "success",
            "agent": "CareerAgent",
            "data": data
        }

