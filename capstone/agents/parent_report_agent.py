# agents/parent_report_agent.py

from typing import Any, Dict
from models.gemini_client import GeminiClient
from models.llm_utils import load_prompt_template, render_prompt, clean_and_parse_json

class ParentReportAgent:
    """
    ParentReportAgent is responsible for summarizing the classroom learning 
    activities into a friendly, parent/guardian facing report. It provides 
    translated summaries, home discussion questions, and joint activities.
    """

    def __init__(self):
        self.client = GeminiClient()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes parent report generation.
        
        Args:
            input_data (dict): Includes grade, subject, topic, language, standards
            
        Returns:
            dict: Translated summaries for families
        """
        grade = input_data.get("grade", "Middle School")
        subject = input_data.get("subject", "Science")
        topic = input_data.get("topic", "STEM Topic")
        language = input_data.get("language", "English")
        notes = input_data.get("additional_notes", "")
        standards_str = input_data.get("standards", "No standards provided.")

        data = {}
        try:
            template = load_prompt_template("parent_prompt.txt")
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
            print(f"Error calling Gemini in ParentReportAgent: {e}. Using local fallback.")

        # Double-check parsed results or use hardcoded backups
        if not data or "family_letter_intro" not in data:
            # Mock simple localization templates
            intro_dict = {
                "english": f"This week, your student explored the mechanics of {topic} in their {subject} class.",
                "spanish (español)": f"Esta semana, su estudiante exploró la mecánica de {topic} en su clase de {subject}.",
                "french (français)": f"Cette semaine, votre élève a exploré les mécanismes de {topic} dans sa classe de {subject}.",
                "arabic (العربية)": f"هذا الأسبوع، استكشف طالبك آليات {topic} في فصل {subject}.",
                "chinese (中文)": f"本周，您的学生在{subject}课上探索了{topic}的力学原理。",
                "portuguese (português)": f"Esta semana, seu aluno explorou a mecânica de {topic} na aula de {subject}.",
                "hindi (हिन्दी)": f"इस सप्ताह, आपके छात्र ने अपनी {subject} कक्षा में {topic} के यांत्रिकी का पता लगाया।"
            }

            # Normalize language to lowercase to match keys
            lang_key = language.lower()
            family_message = intro_dict.get(lang_key, intro_dict["english"])

            discussion_questions = [
                f"Ask your child: 'How does {topic} affect things we use every day at home?'",
                "Ask your child to describe the micro-controller or model they constructed in the maker activity."
            ]

            home_activity = (
                f"Spend 10 minutes looking for examples of {topic} in your neighborhood or "
                "around the kitchen. Document your findings together!"
            )

            data = {
                "language_processed": language,
                "family_letter_intro": family_message,
                "discussion_starters": discussion_questions,
                "recommended_home_activity": home_activity
            }

        return {
            "status": "success",
            "agent": "ParentReportAgent",
            "data": data
        }

