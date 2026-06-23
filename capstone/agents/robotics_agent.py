# agents/robotics_agent.py

from typing import Any, Dict
from models.gemini_client import GeminiClient
from models.llm_utils import load_prompt_template, render_prompt, clean_and_parse_json

class RoboticsAgent:
    """
    RoboticsAgent is responsible for designing hands-on engineering, robotics,
    or physical coding (Arduino, Micro:bit, Raspberry Pi) instructions 
    matching the selected grade level and subject focus.
    """

    def __init__(self):
        self.client = GeminiClient()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes robotics/maker program generation.
        
        Args:
            input_data (dict): Includes grade, subject, topic, language, standards
            
        Returns:
            dict: Structured hardware/electronics activities
        """
        grade = input_data.get("grade", "Middle School")
        subject = input_data.get("subject", "Science")
        topic = input_data.get("topic", "STEM Topic")
        language = input_data.get("language", "English")
        notes = input_data.get("additional_notes", "")
        standards_str = input_data.get("standards", "No standards provided.")

        data = {}
        try:
            template = load_prompt_template("robotics_prompt.txt")
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
            print(f"Error calling Gemini in RoboticsAgent: {e}. Using local fallback.")

        # Double-check parsed results or use hardcoded backups
        if not data or "assembly_steps" not in data:
            # Adjust hardware recommended by grade range
            if "Kindergarten" in grade:
                hardware = "Zero electronics. Focus on cardboard simple machines, blocks, or paper structures."
                code_type = "None (Unplugged Activity)"
                code_snippet = "# Unplugged Activity: Act out commands with arrow cards on the floor!"
            elif "Elementary" in grade:
                hardware = "Micro:bit v2 or basic LEGO Spike / simple DC motors."
                code_type = "MakeCode Blocks (Visual Programming)"
                code_snippet = (
                    "// MakeCode/JavaScript Block Pseudocode\n"
                    "basic.forever(function () {\n"
                    "    if (input.lightLevel() < 100) {\n"
                    "        music.playTone(262, music.beat(BeatFraction.Whole))\n"
                    "    }\n"
                    "})"
                )
            elif "High School" in grade:
                hardware = "Arduino Uno R3 or Raspberry Pi Pico, standard resistors, servo motors, breadboard."
                code_type = "C++ (Arduino IDE) / MicroPython"
                code_snippet = (
                    "// C++ Arduino Code\n"
                    "const int sensorPin = A0;\n"
                    "void setup() {\n"
                    "  pinMode(13, OUTPUT);\n"
                    "  Serial.begin(9600);\n"
                    "}\n"
                    "void loop() {\n"
                    "  int reading = analogRead(sensorPin);\n"
                    "  if (reading > 500) {\n"
                    "    digitalWrite(13, HIGH);\n"
                    "  } else {\n"
                    "    digitalWrite(13, LOW);\n"
                    "  }\n"
                    "  delay(100);\n"
                    "}"
                )
            else: # Middle School default
                hardware = "Micro:bit v2, standard micro-USB cable, single servo motor."
                code_type = "MicroPython (microbit module)"
                code_snippet = (
                    "from microbit import *\n\n"
                    "while True:\n"
                    "    # Reading standard environment variables related to " + topic + "\n"
                    "    if button_a.is_pressed():\n"
                    "        display.show(Image.HAPPY)\n"
                    "        pin0.write_digital(1)\n"
                    "    else:\n"
                    "        display.show(Image.ASLEEP)\n"
                    "        pin0.write_digital(0)\n"
                    "    sleep(100)"
                )

            data = {
                "activity_name": f"Hands-on {topic} Prototype build",
                "recommended_hardware": hardware,
                "programming_environment": code_type,
                "code_sample": code_snippet,
                "assembly_steps": [
                    "Collect all structural components and set up your workspace.",
                    "Connect sensors to input pins and actuators/motors to output pins on the board.",
                    "Upload the code block to the microcontroller to calibrate sensor baselines.",
                    "Assemble the cardboard protection mount to hold the electronics safely during tests."
                ]
            }

        return {
            "status": "success",
            "agent": "RoboticsAgent",
            "data": data
        }

