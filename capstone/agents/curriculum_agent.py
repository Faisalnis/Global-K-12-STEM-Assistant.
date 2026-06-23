# agents/curriculum_agent.py

from typing import Any, Dict
from models.gemini_client import GeminiClient
from models.llm_utils import load_prompt_template, render_prompt, clean_and_parse_json

class CurriculumAgent:
    """
    CurriculumAgent is responsible for aligning the target STEM topic 
    with standard educational benchmarks (e.g., NGSS, Common Core, IB) 
    and generating key learning objectives and concepts.
    """

    def __init__(self):
        self.client = GeminiClient()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the curriculum generation logic.
        
        Args:
            input_data (dict): Includes:
                - grade (str): Grade level (e.g., Middle School)
                - subject (str): Subject (e.g., Science)
                - topic (str): Specific topic (e.g., Gravity)
                - language (str): Language for outputs
                - additional_notes (str): Any custom prompts
                
        Returns:
            dict: Structured curriculum alignment data
        """
        grade = input_data.get("grade", "Middle School (Grades 6-8)")
        subject = input_data.get("subject", "Science")
        topic = input_data.get("topic", "Forces and Motion")
        language = input_data.get("language", "English")
        notes = input_data.get("additional_notes", "")
        
        # Standard standards mapping logic integrated with RAG Retriever
        standards = []
        try:
            from rag.retriever import Retriever
            retriever = Retriever()
            # Perform query combining parameters to search vector store
            query_str = f"{subject} {topic} {grade}"
            retrieved_items = retriever.retrieve(query_str, top_k=2)
            
            for item in retrieved_items:
                meta = item.get("metadata", {})
                standards.append({
                    "code": meta.get("code", "N/A"),
                    "description": item.get("document", "")
                })
        except Exception as e:
            print(f"Warning: RAG search failed: {e}. Falling back to default data.")

        # Fallback dataset if RAG search is empty
        if not standards:
            if subject.lower() == "science":
                standards = [
                    {
                        "code": "MS-PS2-2",
                        "description": "Plan an investigation to provide evidence that the change in an object's motion depends on the sum of the forces on the object and the mass of the object."
                    },
                    {
                        "code": "MS-PS2-1",
                        "description": "Apply Newton's Third Law to design a solution to a problem involving the motion of two colliding objects."
                    }
                ]
            elif subject.lower() == "technology":
                standards = [
                    {
                        "code": "CSTA-2-AP-10",
                        "description": "Use flowcharts and/or pseudocode to address complex problems as algorithms."
                    }
                ]
            elif subject.lower() == "engineering":
                standards = [
                    {
                        "code": "MS-ETS1-2",
                        "description": "Evaluate competing design solutions using a systematic process to determine how well they meet the criteria and constraints of the problem."
                    }
                ]
            else: # Mathematics
                standards = [
                    {
                        "code": "CCSS.MATH.CONTENT.8.F.A.1",
                        "description": "Understand that a function is a rule that assigns to each input exactly one output."
                    }
                ]

        # Format standards for RAG Context
        rag_context_str = "\n".join([f"- {s['code']}: {s['description']}" for s in standards])

        # Load prompt template and generate
        data = {}
        try:
            template = load_prompt_template("curriculum_prompt.txt")
            prompt = render_prompt(template, {
                "grade": grade,
                "subject": subject,
                "topic": topic,
                "language": language,
                "additional_notes": notes,
                "rag_context": rag_context_str
            })
            raw_response = self.client.generate(prompt)
            data = clean_and_parse_json(raw_response)
        except Exception as e:
            print(f"Error calling Gemini in CurriculumAgent: {e}. Using local fallback.")

        # Double-check parsed results or use hardcoded backups
        if not data or "standards_alignment" not in data:
            data = {
                "grade_level": grade,
                "subject": subject,
                "topic": topic,
                "language": language,
                "standards_alignment": standards,
                "learning_objectives": [
                    f"Understand the fundamental mechanics of {topic} within the context of {grade}.",
                    f"Conduct hands-on tests to observe how variables affect {topic}.",
                    f"Apply critical thinking skills to analyze structural outputs related to {topic}."
                ],
                "key_vocabulary": [topic, "Acceleration", "System Equilibrium", "Variables", "Inquiry"],
                "framework_context": "Next Generation Science Standards (NGSS) & IB Primary/Middle Years Programme"
            }

        return {
            "status": "success",
            "agent": "CurriculumAgent",
            "data": data
        }

