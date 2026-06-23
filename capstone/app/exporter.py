# app/exporter.py

def compile_curriculum_md(curr_data: dict) -> str:
    """Formats the curriculum alignment data as markdown."""
    md = []
    md.append(f"# 📚 Curriculum Alignment: {curr_data.get('topic', 'STEM Topic')}")
    md.append(f"- **Grade Level**: {curr_data.get('grade_level', 'N/A')}")
    md.append(f"- **STEM Subject**: {curr_data.get('subject', 'N/A')}")
    md.append(f"- **Framework Reference**: {curr_data.get('framework_context', 'NGSS')}")
    md.append(f"- **Output Language**: {curr_data.get('language', 'English')}")
    md.append("\n---")
    
    md.append("\n### 📌 Core Learning Standards")
    standards = curr_data.get("standards_alignment", [])
    if standards:
        for std in standards:
            md.append(f"- **{std.get('code', 'N/A')}**: {std.get('description', '')}")
    else:
        md.append("_No standards alignments generated._")
        
    md.append("\n### 🎯 Key Learning Objectives")
    objectives = curr_data.get("learning_objectives", [])
    if objectives:
        for idx, obj in enumerate(objectives, 1):
            md.append(f"{idx}. {obj}")
    else:
        md.append("_No learning objectives generated._")
        
    md.append("\n### 🔑 Key Vocabulary")
    vocab = curr_data.get("key_vocabulary", [])
    if vocab:
        md.append(", ".join([f"`{v}`" for v in vocab]))
    else:
        md.append("_No vocabulary defined._")
        
    return "\n".join(md)


def compile_lesson_md(lesson_data: dict) -> str:
    """Formats the lesson plan data as markdown."""
    md = []
    md.append(f"# 📝 Lesson Plan: {lesson_data.get('lesson_title', 'Inquiry Lesson')}")
    md.append(f"- **Pedagogical Model**: {lesson_data.get('pedagogical_model', '5E Inquiry Framework')}")
    md.append(f"- **Estimated Duration**: {lesson_data.get('estimated_duration', '60 Minutes')}")
    md.append("\n---")
    
    md.append("\n### 📦 Materials Required")
    materials = lesson_data.get("materials_required", [])
    if materials:
        for mat in materials:
            md.append(f"- {mat}")
    else:
        md.append("_No materials listed._")
        
    md.append("\n### ⏱️ Phase-by-Phase Lesson Agenda")
    sequence = lesson_data.get("lesson_sequence", {})
    if sequence:
        # Standard 5E order or key ordering
        phases = ['engage', 'explore', 'explain', 'elaborate', 'evaluate']
        for p in phases:
            if p in sequence:
                p_data = sequence[p]
                md.append(f"\n#### {p_data.get('title', p.capitalize())}")
                md.append(p_data.get('description', ''))
            elif p.capitalize() in sequence:
                p_data = sequence[p.capitalize()]
                md.append(f"\n#### {p_data.get('title', p.capitalize())}")
                md.append(p_data.get('description', ''))
        # Capture other phases if they aren't standard 5E keys
        for k, v in sequence.items():
            if k.lower() not in phases and k.capitalize() not in phases:
                md.append(f"\n#### {v.get('title', k)}")
                md.append(v.get('description', ''))
    else:
        md.append("_No lesson sequence available._")
        
    md.append("\n### 💡 Differentiation Strategies")
    diff = lesson_data.get("differentiation", {})
    if diff:
        md.append(f"- **Support**: {diff.get('support', 'N/A')}")
        md.append(f"- **Extension**: {diff.get('extension', 'N/A')}")
    else:
        md.append("_No differentiation strategies provided._")
        
    return "\n".join(md)


def compile_robotics_md(robotics_data: dict) -> str:
    """Formats the robotics & maker build data as markdown."""
    md = []
    md.append(f"# 🤖 Robotics & Hands-On Engineering: {robotics_data.get('activity_name', 'Maker Project')}")
    md.append(f"- **Recommended Hardware**: {robotics_data.get('recommended_hardware', 'N/A')}")
    md.append(f"- **Programming Environment**: {robotics_data.get('programming_environment', 'N/A')}")
    md.append("\n---")
    
    md.append("\n### ⚙️ Assembly & Build Steps")
    steps = robotics_data.get("assembly_steps", [])
    if steps:
        for idx, step in enumerate(steps, 1):
            md.append(f"{idx}. {step}")
    else:
        md.append("_No assembly steps provided._")
        
    md.append("\n### 💻 Sample Code Block")
    env = robotics_data.get("programming_environment", "Python")
    code = robotics_data.get("code_sample", "")
    if code:
        md.append(f"```{env.lower() if 'python' in env.lower() or 'c++' in env.lower() else ''}\n{code}\n```")
    else:
        md.append("_No code block generated._")
        
    return "\n".join(md)


def compile_assessment_md(assessment_data: dict) -> str:
    """Formats the assessment quiz and rubric as markdown."""
    md = []
    md.append(f"# ✍️ Assessment & Evaluation Rubric: {assessment_data.get('quiz_title', 'Exit Check')}")
    md.append("\n---")
    
    md.append("\n### ❓ Formative Quiz (Exit Slip)")
    questions = assessment_data.get("questions", [])
    if questions:
        for q in questions:
            md.append(f"\n**Q{q.get('id', '')}: {q.get('question', '')}**")
            for opt in q.get("options", []):
                correct = " *(Correct Answer)*" if opt == q.get("correct_option") else ""
                md.append(f"- {opt}{correct}")
    else:
        md.append("_No quiz questions provided._")
        
    md.append(f"\n**Interactive Exit Slip Prompt**:\n_{assessment_data.get('exit_slip_prompt', 'Write down what you learned today.')}_")
    
    md.append("\n### 📊 Standard Rubric Matrix")
    rubric = assessment_data.get("grading_rubric", [])
    if rubric:
        md.append("| Criteria | Beginning (1 Pt) | Developing (2 Pts) | Exemplary (3 Pts) |")
        md.append("| --- | --- | --- | --- |")
        for r in rubric:
            md.append(f"| **{r.get('criteria', 'Criteria')}** | {r.get('beginning', '')} | {r.get('developing', '')} | {r.get('exemplary', '')} |")
    else:
        md.append("_No rubric defined._")
        
    return "\n".join(md)


def compile_careers_md(career_data: dict) -> str:
    """Formats career pathway mapping as markdown."""
    md = []
    md.append("# 🚀 Real-World STEM Careers & Inspiration")
    md.append("\n---")
    
    md.append("\n### 👩‍🚀 STEM Career Spotlights")
    careers = career_data.get("careers", [])
    if careers:
        for idx, c in enumerate(careers, 1):
            md.append(f"\n#### 💼 {idx}. {c.get('title', 'STEM Career')} (Salary: {c.get('median_salary', 'N/A')})")
            md.append(c.get("description", ""))
            skills = c.get("key_skills", [])
            if skills:
                md.append(f"- **Key Skills**: {', '.join(skills)}")
    else:
        md.append("_No career spotlights generated._")
        
    md.append("\n### 🌟 Spotlight Role Model")
    rm = career_data.get("role_model", {})
    if rm:
        md.append(f"**Name**: {rm.get('name', 'N/A')}")
        md.append(f"- **Background**: {rm.get('background', 'N/A')}")
        md.append(f"- **Inspirational Quote**: *\"{rm.get('quote', '')}\"*")
        md.append(f"- **Lesson Connection**: {rm.get('lesson_connection', 'N/A')}")
    else:
        md.append("_No spotlight role model profile generated._")
        
    return "\n".join(md)


def compile_parent_report_md(parent_data: dict, topic: str = "STEM Topic", subject: str = "STEM") -> str:
    """Formats localized parent take-home report as markdown."""
    md = []
    md.append(f"# 👪 Take-Home Parent Report (Language: {parent_data.get('language_processed', 'English')})")
    md.append("\n---")
    
    md.append("\n### 💌 Family Letter")
    md.append(f"**Subject**: Exciting STEM Exploration: Learning about **{topic}**\n")
    md.append("Dear Family,\n")
    md.append(parent_data.get("family_letter_intro", f"This week, your student explored {topic} in their {subject} class."))
    md.append("\n")
    
    md.append("### 🗣️ Home Discussion Starters")
    starters = parent_data.get("discussion_starters", [])
    if starters:
        for st in starters:
            md.append(f"- {st}")
    else:
        md.append(f"- Ask your child: 'How does {topic} affect things we use every day at home?'")
        
    md.append(f"\n### 🛠️ Recommended Activity\n- {parent_data.get('recommended_home_activity', 'Discuss what was learned in class today.')}")
    md.append("\n\nThank you for partnership in STEM learning!\n\nBest regards,\n*The STEM Instruction Team*")
    
    return "\n".join(md)


def compile_full_package(outputs: dict, grade: str, subject: str, topic: str, lang: str, notes: str) -> str:
    """Compiles all outputs from individual agents into a single, cohesive Markdown handbook."""
    md = []
    md.append(f"# 🌍 Global K-12 STEM Curriculum Package: {topic}")
    md.append("Generated by the AI Multi-Agent K-12 STEM Assistant.")
    md.append("\n## 📋 General Package Metadata")
    md.append(f"- **Target Grade Level**: {grade}")
    md.append(f"- **STEM Core Domain**: {subject}")
    md.append(f"- **Selected STEM Topic**: {topic}")
    md.append(f"- **Output Language**: {lang}")
    if notes:
        md.append(f"- **Custom Objectives / Constraints**: \n  > {notes}")
    md.append("\n" + "=" * 40 + "\n")
    
    md.append(compile_curriculum_md(outputs.get("curriculum", {})))
    md.append("\n" + "=" * 40 + "\n")
    
    md.append(compile_lesson_md(outputs.get("lesson_plan", {})))
    md.append("\n" + "=" * 40 + "\n")
    
    md.append(compile_robotics_md(outputs.get("robotics", {})))
    md.append("\n" + "=" * 40 + "\n")
    
    md.append(compile_assessment_md(outputs.get("assessment", {})))
    md.append("\n" + "=" * 40 + "\n")
    
    md.append(compile_careers_md(outputs.get("careers", {})))
    md.append("\n" + "=" * 40 + "\n")
    
    md.append(compile_parent_report_md(outputs.get("parent_report", {}), topic, subject))
    md.append("\n" + "=" * 40 + "\n")
    
    md.append("## 🛡️ Validation & AI Generation Notice")
    md.append("This package was generated dynamically using a collaborative multi-agent architecture. Curriculum alignments are cross-referenced with a vector database (RAG) of standard science, technology, engineering, and mathematical benchmarks. Local translations have been processed to maintain readability and regional context.")
    
    return "\n".join(md)
