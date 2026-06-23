# app/streamlit_app.py

import os
import sys
import time

# Ensure the parent directory is in sys.path to allow clean imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app import config
from app import exporter

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title=config.APP_NAME,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject modern, premium custom CSS
st.markdown("""
<style>
    /* Import modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

    /* Apply typography overrides */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Elegant Title and Subtitle */
    .title-gradient {
        background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.9rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle-text {
        font-size: 1.1rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
    }
    
    /* Styled Premium Adaptive Cards */
    .glass-card {
        background: rgba(128, 128, 128, 0.05);
        border-radius: 14px;
        padding: 1.6rem;
        border: 1px solid rgba(128, 128, 128, 0.12);
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.25s ease-in-out;
    }
    .glass-card:hover {
        border-color: rgba(128, 128, 128, 0.22);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px 0 rgba(0, 0, 0, 0.09);
    }
    
    /* Card Header */
    .card-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.6rem;
    }
    
    /* Premium Badge tags */
    .badge-tag {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(99, 102, 241, 0.04));
        border: 1px solid rgba(99, 102, 241, 0.25);
        color: #6366f1;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-block;
        margin: 4px;
    }
    
    /* Microcontroller Code sample title header bar */
    .code-header {
        background-color: rgba(128, 128, 128, 0.1);
        padding: 8px 14px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border-bottom: 1px solid rgba(128, 128, 128, 0.18);
        font-family: 'Outfit', sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
    }
    
    /* Custom rubric table mapping */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.2rem 0;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(128, 128, 128, 0.15);
    }
    .custom-table th {
        background-color: rgba(99, 102, 241, 0.1);
        color: #6366f1;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        padding: 12px 14px;
        text-align: left;
        border-bottom: 2px solid rgba(99, 102, 241, 0.2);
    }
    .custom-table td {
        padding: 12px 14px;
        border-bottom: 1px solid rgba(128, 128, 128, 0.1);
        font-size: 0.92rem;
        line-height: 1.4;
    }
    .custom-table tr:hover {
        background-color: rgba(128, 128, 128, 0.03);
    }

    /* Tab Styling Overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        transition: all 0.2s ease;
    }

    /* Status indicator label styling */
    .engine-badge {
        font-weight: 600;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "generated" not in st.session_state:
    st.session_state.generated = False
    st.session_state.grade = config.GRADE_LEVELS[2]  # Middle School
    st.session_state.subject = config.SUBJECTS[0]      # Science
    st.session_state.topic = ""
    st.session_state.lang = config.LANGUAGES[0]        # English
    st.session_state.prompt = ""
    st.session_state.outputs = {}

# ==========================================
# SIDEBAR CONTROL PANEL
# ==========================================
st.sidebar.markdown(f"## {config.APP_ICON} {config.APP_NAME}")
st.sidebar.markdown("Configure the STEM educational parameters below to generate localized materials.")

st.sidebar.divider()

# Grade Level Selection (Uses Session State)
grade_options = config.GRADE_LEVELS
default_grade_idx = grade_options.index(st.session_state.grade) if st.session_state.grade in grade_options else 2
selected_grade = st.sidebar.selectbox(
    "Target Grade Level",
    options=grade_options,
    index=default_grade_idx
)

# Subject Selection (Uses Session State)
subject_options = config.SUBJECTS
default_subject_idx = subject_options.index(st.session_state.subject) if st.session_state.subject in subject_options else 0
selected_subject = st.sidebar.selectbox(
    "STEM Subject",
    options=subject_options,
    index=default_subject_idx
)

# Dynamic Topic Selection based on Subject (Uses Session State)
available_topics = config.TOPICS.get(selected_subject, [])
topic_options = available_topics + ["Custom Topic..."]

if st.session_state.topic in available_topics:
    default_topic_idx = available_topics.index(st.session_state.topic)
elif st.session_state.topic and st.session_state.topic not in available_topics:
    default_topic_idx = len(available_topics)  # points to "Custom Topic..."
else:
    default_topic_idx = 0

selected_topic = st.sidebar.selectbox(
    "STEM Topic Focus",
    options=topic_options,
    index=default_topic_idx
)

# Handle Custom Topic input
custom_topic = ""
if selected_topic == "Custom Topic...":
    default_custom = st.session_state.topic if st.session_state.topic not in available_topics else ""
    custom_topic = st.sidebar.text_input(
        "Enter Custom Topic Name",
        value=default_custom,
        placeholder="e.g., Quantum Computing, Renewable Biomass"
    )

# Language Selection (Uses Session State)
lang_options = config.LANGUAGES
default_lang_idx = lang_options.index(st.session_state.lang) if st.session_state.lang in lang_options else 0
selected_lang = st.sidebar.selectbox(
    "Output Language",
    options=lang_options,
    index=default_lang_idx
)

st.sidebar.divider()
st.sidebar.markdown("### 🔌 System Engine Status")

from models.gemini_client import GeminiClient
client_check = GeminiClient()

if client_check.is_mock_mode():
    st.sidebar.markdown('<span class="engine-badge" style="background-color: rgba(241, 196, 15, 0.15); color: #f1c40f; border: 1px solid rgba(241, 196, 15, 0.3);">⚠️ Mock Fallback Engine</span>', unsafe_allow_html=True)
    st.sidebar.caption("`GEMINI_API_KEY` is not set. Operating in offline simulation mode.")
else:
    st.sidebar.markdown('<span class="engine-badge" style="background-color: rgba(46, 204, 113, 0.15); color: #2ecc71; border: 1px solid rgba(46, 204, 113, 0.3);">🟢 Live Gemini API Active</span>', unsafe_allow_html=True)
    st.sidebar.caption("Connected to Google Gemini 1.5 Flash.")

# ==========================================
# MAIN APPLICATION LAYOUT
# ==========================================
st.markdown(f'<div class="title-gradient">{config.APP_NAME}</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Empowering educators worldwide with dynamic, curriculum-aligned K-12 STEM modules powered by RAG and Collaborating Agents.</div>', unsafe_allow_html=True)

st.markdown("### 🛠️ Interactive AI Assistant Console")
user_prompt = st.text_area(
    "Specify learning goals, target classroom context, or special material constraints:",
    value=st.session_state.prompt,
    placeholder=(
        "Example: I want a 45-minute lesson focusing on hands-on inquiry. "
        "We have access to cardboard, straws, and glue, but no digital devices. "
        "Include adaptations for visual learners."
    ),
    height=100
)

# Determine active topic name
topic_name = custom_topic if (selected_topic == "Custom Topic..." and custom_topic) else selected_topic

col_action1, col_action2 = st.columns([1, 4])
with col_action1:
    generate_btn = st.button("🚀 Generate STEM Module", use_container_width=True, type="primary")

st.divider()

# ==========================================
# GENERATION ENGINE - MULTI-AGENT EXECUTION
# ==========================================
if generate_btn:
    if not topic_name:
        st.error("Please select a topic or enter a custom topic name before generating.")
    else:
        # Construct input payload
        input_payload = {
            "grade": selected_grade,
            "subject": selected_subject,
            "topic": topic_name,
            "language": selected_lang,
            "additional_notes": user_prompt
        }
        
        # Elegant multi-stage loading block showing real agent coordination
        with st.status("🚀 Launching Multi-Agent STEM Generation Engine...", expanded=True) as status_box:
            
            # Step 1: Curriculum Alignment (retrieves RAG standards)
            status_box.write("📚 Querying vector database & aligning standards (CurriculumAgent)...")
            from agents.curriculum_agent import CurriculumAgent
            curriculum_agent = CurriculumAgent()
            curriculum_result = curriculum_agent.run(input_payload)
            
            # Extract retrieved standards to feed downstream agents
            standards_list = curriculum_result.get("data", {}).get("standards_alignment", [])
            standards_formatted_str = ""
            if standards_list:
                standards_formatted_str = "\n".join([
                    f"- {std.get('code')}: {std.get('description')}" 
                    for std in standards_list if std.get('code') and std.get('description')
                ])
            else:
                standards_formatted_str = "No specific standards retrieved."
            
            # Enrich next agents' payload
            enriched_input = dict(input_payload)
            enriched_input["standards"] = standards_formatted_str
            
            # Step 2: Lesson Plan
            status_box.write("📝 Designing inquiry-based 5E lesson sequence (LessonPlannerAgent)...")
            from agents.lesson_planner_agent import LessonPlannerAgent
            lesson_planner = LessonPlannerAgent()
            lesson_result = lesson_planner.run(enriched_input)
            
            # Step 3: Robotics Build
            status_box.write("🤖 Designing hardware assembly & code logic (RoboticsAgent)...")
            from agents.robotics_agent import RoboticsAgent
            robotics_agent = RoboticsAgent()
            robotics_result = robotics_agent.run(enriched_input)
            
            # Step 4: Assessment
            status_box.write("✍️ Formulating exit ticket & matrix rubric (AssessmentAgent)...")
            from agents.assessment_agent import AssessmentAgent
            assessment_agent = AssessmentAgent()
            assessment_result = assessment_agent.run(enriched_input)
            
            # Step 5: Career Mapping
            status_box.write("🚀 Identifying STEM careers & diverse role models (CareerAgent)...")
            from agents.career_agent import CareerAgent
            career_agent = CareerAgent()
            career_result = career_agent.run(enriched_input)
            
            # Step 6: Parent Letter (localized)
            status_box.write("👪 Composing translated family take-home letter (ParentReportAgent)...")
            from agents.parent_report_agent import ParentReportAgent
            parent_report_agent = ParentReportAgent()
            parent_report_result = parent_report_agent.run(enriched_input)
            
            # Aggregate outputs in session state
            outputs = {
                "curriculum": curriculum_result.get("data", {}),
                "lesson_plan": lesson_result.get("data", {}),
                "robotics": robotics_result.get("data", {}),
                "assessment": assessment_result.get("data", {}),
                "careers": career_result.get("data", {}),
                "parent_report": parent_report_result.get("data", {})
            }
            
            # Save parameters to session state to maintain state on downloads
            st.session_state.generated = True
            st.session_state.grade = selected_grade
            st.session_state.subject = selected_subject
            st.session_state.topic = topic_name
            st.session_state.lang = selected_lang
            st.session_state.prompt = user_prompt
            st.session_state.outputs = outputs
            
            status_box.update(label="✅ STEM Curriculum Package Generated Successfully!", state="complete", expanded=False)
        
        st.toast("Success! Multi-agent STEM module compiled.", icon="🔥")

# ==========================================
# DISPLAY GENERATED OUTPUTS
# ==========================================
if st.session_state.generated:
    outputs = st.session_state.outputs
    
    # Header Info Pannel and Package Download
    col_header_title, col_header_dl = st.columns([3, 1])
    with col_header_title:
        st.success(f"**Viewing STEM Resource**: {st.session_state.topic} ({st.session_state.subject}) for **{st.session_state.grade}** in **{st.session_state.lang}**.")
        if client_check.is_mock_mode():
            st.info("⚡ **Mock Fallback Engine Active**: Operating offline. Generation details are structured simulations.")
        else:
            st.success("✨ **Live Gemini API Active**: Fully generated via Google Gemini 1.5 Flash client.")
    
    with col_header_dl:
        # Package compiler download button
        full_markdown_text = exporter.compile_full_package(
            outputs,
            st.session_state.grade,
            st.session_state.subject,
            st.session_state.topic,
            st.session_state.lang,
            st.session_state.prompt
        )
        st.download_button(
            label="🎁 Download Complete Package",
            data=full_markdown_text,
            file_name=f"stem_bundle_{st.session_state.topic.lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
            type="primary"
        )
        
    st.write("")
    
    # Tab Declaration
    tab_curriculum, tab_lesson, tab_robotics, tab_assessment, tab_careers, tab_parent = st.tabs([
        "📚 Curriculum Alignment",
        "📝 Lesson Plan",
        "🤖 Robotics & Maker",
        "✍️ Assessment & Rubric",
        "🚀 Careers in STEM",
        "👪 Parent Report"
    ])
    
    # ------------------------------------------
    # 1. CURRICULUM ALIGNMENT TAB
    # ------------------------------------------
    with tab_curriculum:
        curr_data = outputs.get("curriculum", {})
        
        # Sub-header with Download Tab Button
        col_tab_t, col_tab_d = st.columns([3, 1])
        with col_tab_t:
            st.markdown(f"### 📚 Standards-Aligned Curriculum: {st.session_state.topic}")
            st.caption(f"Framework Reference Context: **{curr_data.get('framework_context', 'Next Generation Science Standards (NGSS)')}**")
        with col_tab_d:
            tab_markdown = exporter.compile_curriculum_md(curr_data)
            st.download_button(
                label="📥 Download Curriculum (MD)",
                data=tab_markdown,
                file_name=f"curriculum_{st.session_state.topic.lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
                key="dl_curr_tab"
            )
            
        st.write("")
        
        col_c1, col_c2 = st.columns([3, 2])
        
        with col_c1:
            st.markdown("#### 📌 Core Learning Standards")
            standards = curr_data.get("standards_alignment", [])
            if standards:
                for std in standards:
                    st.markdown(f"""
                    <div class="glass-card">
                        <div class="card-title" style="color: #6366f1; font-weight:700;">📌 {std.get('code')}</div>
                        <div style="font-size: 0.95rem; line-height: 1.5;">{std.get('description')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No standards alignments returned. Verify configuration parameters.")
                
        with col_c2:
            # Display Objectives in checklist style
            st.markdown("#### 🎯 Key Learning Objectives")
            objectives = curr_data.get("learning_objectives", [])
            if objectives:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                for idx, obj in enumerate(objectives, 1):
                    st.markdown(f"""
                    <div style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px;">
                        <span style="background-color: rgba(99, 102, 241, 0.15); color: #6366f1; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 700; flex-shrink: 0;">{idx}</span>
                        <span style="font-size: 0.95rem; line-height: 1.4;">{obj}</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Display vocabulary in badged layout
            st.markdown("#### 🔑 Key Vocabulary")
            vocab = curr_data.get("key_vocabulary", [])
            if vocab:
                st.markdown('<div class="glass-card" style="padding: 1.2rem;">', unsafe_allow_html=True)
                vocab_html = "".join([f'<span class="badge-tag">{v}</span>' for v in vocab])
                st.markdown(f"<div>{vocab_html}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
        st.markdown("> [!NOTE]\n> *Curriculum standards are queried from the ChromaDB vector database (RAG context) by **CurriculumAgent**.*")
        
    # ------------------------------------------
    # 2. LESSON PLAN TAB
    # ------------------------------------------
    with tab_lesson:
        lesson_data = outputs.get("lesson_plan", {})
        
        # Sub-header with Download Tab Button
        col_tab_t, col_tab_d = st.columns([3, 1])
        with col_tab_t:
            st.markdown(f"### 📝 Step-by-Step Lesson Plan")
            st.markdown(f"#### 🏷️ {lesson_data.get('lesson_title', 'STEM Inquiry Investigation')}")
        with col_tab_d:
            tab_markdown = exporter.compile_lesson_md(lesson_data)
            st.download_button(
                label="📥 Download Lesson Plan (MD)",
                data=tab_markdown,
                file_name=f"lesson_plan_{st.session_state.topic.lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
                key="dl_lesson_tab"
            )
            
        st.write("")
        
        # Key Lesson Metrics
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1rem;">
                <div style="font-size: 0.85rem; color:#888;">ESTIMATED DURATION</div>
                <div style="font-size: 1.6rem; font-weight: 700; color:#6366f1; margin-top: 4px;">⏱️ {lesson_data.get('estimated_duration', '60 Minutes')}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1rem;">
                <div style="font-size: 0.85rem; color:#888;">PEDAGOGICAL MODEL</div>
                <div style="font-size: 1.6rem; font-weight: 700; color:#a855f7; margin-top: 4px;">🎯 {lesson_data.get('pedagogical_model', '5E Framework')}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1rem;">
                <div style="font-size: 0.85rem; color:#888;">MATERIALS REQUIRED</div>
                <div style="font-size: 1.6rem; font-weight: 700; color:#ec4899; margin-top: 4px;">📦 {len(lesson_data.get('materials_required', []))} Items</div>
            </div>
            """, unsafe_allow_html=True)
            
        col_l1, col_l2 = st.columns([1, 2])
        
        with col_l1:
            st.markdown("#### 📦 Required Materials")
            materials = lesson_data.get("materials_required", [])
            if materials:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                for item in materials:
                    st.markdown(f"- **{item}**")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No materials listed.")
                
        with col_l2:
            st.markdown("#### ⏱️ Phase-by-Phase Lesson Agenda (5E Model)")
            seq = lesson_data.get("lesson_sequence", {})
            if seq:
                # Loop through standard 5E keys in order
                phases_ordered = ['engage', 'explore', 'explain', 'elaborate', 'evaluate']
                for p_key in phases_ordered:
                    p_val = seq.get(p_key) or seq.get(p_key.capitalize())
                    if p_val:
                        with st.expander(f"⏱️ {p_val.get('title', p_key.capitalize())}", expanded=True):
                            st.write(p_val.get('description'))
            else:
                st.info("No lesson sequence steps generated.")
                
        st.markdown("#### 💡 Differentiation Strategies")
        diff = lesson_data.get("differentiation", {})
        if diff:
            col_diff1, col_diff2 = st.columns(2)
            with col_diff1:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #3b82f6;">
                    <div class="card-title" style="color: #3b82f6;">♿ Support Accommodations</div>
                    <div style="font-size: 0.95rem; line-height: 1.4;">{diff.get('support')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_diff2:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 4px solid #10b981;">
                    <div class="card-title" style="color: #10b981;">🚀 Extension Challenges</div>
                    <div style="font-size: 0.95rem; line-height: 1.4;">{diff.get('extension')}</div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("> [!NOTE]\n> *Generated dynamically via **LessonPlannerAgent** using core standards as references.*")
        
    # ------------------------------------------
    # 3. ROBOTICS & MAKER TAB
    # ------------------------------------------
    with tab_robotics:
        robotics_data = outputs.get("robotics", {})
        
        # Sub-header with Download Tab Button
        col_tab_t, col_tab_d = st.columns([3, 1])
        with col_tab_t:
            st.markdown(f"### 🤖 Robotics & Hands-On Engineering")
            st.markdown(f"#### 🛠️ Build Activity: {robotics_data.get('activity_name', 'STEM Maker Build')}")
        with col_tab_d:
            tab_markdown = exporter.compile_robotics_md(robotics_data)
            st.download_button(
                label="📥 Download Robotics Activity (MD)",
                data=tab_markdown,
                file_name=f"robotics_{st.session_state.topic.lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
                key="dl_robotics_tab"
            )
            
        st.write("")
        
        col_r1, col_r2 = st.columns([2, 3])
        
        with col_r1:
            st.markdown("#### ⚙️ Hardware / Crafts Checklist")
            st.markdown(f"""
            <div class="glass-card">
                <div class="card-title" style="color:#ec4899;">📦 Hardware/Components</div>
                <div style="font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem;">{robotics_data.get('recommended_hardware', 'N/A')}</div>
                <div class="card-title" style="color:#ec4899; margin-top: 1.2rem;">💻 Coding Environment</div>
                <div class="badge-tag" style="margin: 0; background: rgba(236,72,153,0.1); border-color: rgba(236,72,153,0.3); color:#ec4899;">{robotics_data.get('programming_environment', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### ⚙️ Assembly & Build Steps")
            steps = robotics_data.get("assembly_steps", [])
            if steps:
                for idx, step in enumerate(steps, 1):
                    st.markdown(f"""
                    <div style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 12px;">
                        <span style="background-color: rgba(236, 72, 153, 0.15); color: #ec4899; border-radius: 4px; padding: 2px 8px; font-weight: 700; font-size: 0.85rem; flex-shrink:0;">STEP {idx}</span>
                        <span style="font-size: 0.95rem; line-height: 1.4;">{step}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No assembly instructions listed.")
                
        with col_r2:
            st.markdown("#### 💻 Logic & Sample Code")
            env = robotics_data.get("programming_environment", "Python")
            
            # Syntax color matcher
            lang_match = "python"
            if "c++" in env.lower() or "arduino" in env.lower():
                lang_match = "cpp"
            elif "makecode" in env.lower() or "javascript" in env.lower():
                lang_match = "javascript"
            
            st.markdown(f"""
            <div class="code-header">
                <span>💻 {env} Script</span>
                <span style="font-size: 0.75rem; color: #888888;">Copy and flash to microcontroller</span>
            </div>
            """, unsafe_allow_html=True)
            st.code(robotics_data.get("code_sample", ""), language=lang_match)
            
        st.markdown("> [!NOTE]\n> *Activity designed dynamically by **RoboticsAgent** to ensure safety, alignment, and cost limitations.*")
        
    # ------------------------------------------
    # 4. ASSESSMENT & RUBRIC TAB
    # ------------------------------------------
    with tab_assessment:
        assessment_data = outputs.get("assessment", {})
        
        # Sub-header with Download Tab Button
        col_tab_t, col_tab_d = st.columns([3, 1])
        with col_tab_t:
            st.markdown(f"### ✍️ Assessment & Evaluation Rubric")
            st.markdown(f"#### ❓ Quiz Title: {assessment_data.get('quiz_title', 'Exit Diagnostic Check')}")
        with col_tab_d:
            tab_markdown = exporter.compile_assessment_md(assessment_data)
            st.download_button(
                label="📥 Download Rubric & Quiz (MD)",
                data=tab_markdown,
                file_name=f"assessment_{st.session_state.topic.lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
                key="dl_assessment_tab"
            )
            
        st.write("")
        
        col_a1, col_a2 = st.columns([2, 3])
        
        with col_a1:
            st.markdown("#### ❓ Formative Concept Check")
            questions = assessment_data.get("questions", [])
            
            if questions:
                for q in questions:
                    st.markdown(f"**Q{q.get('id')}: {q.get('question')}**")
                    for option in q.get("options", []):
                        is_correct = option == q.get("correct_option")
                        style = "font-weight: 600; color: #10b981;" if is_correct else ""
                        check = " ✅" if is_correct else ""
                        st.markdown(f"""
                        <div style="margin-left: 1.2rem; padding: 4px 8px; border-radius: 4px; {style} font-size: 0.95rem;">
                            • {option}{check}
                        </div>
                        """, unsafe_allow_html=True)
                    st.write("")
            else:
                st.info("No concept questions generated.")
                
            # Exit slip prompt
            st.markdown("#### 🎟️ Formative Exit Ticket")
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #f59e0b;">
                <div class="card-title" style="color: #f59e0b;">🎟️ Exit Slip Prompt</div>
                <div style="font-style: italic; font-size: 1rem; line-height: 1.4;">"{assessment_data.get('exit_slip_prompt')}"</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_a2:
            st.markdown("#### 📊 Standard Rubric Matrix")
            rubric_list = assessment_data.get("grading_rubric", [])
            
            if rubric_list:
                rubric_html = """
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th>Criteria</th>
                            <th>Beginning (1 Pt)</th>
                            <th>Developing (2 Pts)</th>
                            <th>Exemplary (3 Pts)</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                for r in rubric_list:
                    rubric_html += f"""
                        <tr>
                            <td><strong>{r.get('criteria')}</strong></td>
                            <td>{r.get('beginning')}</td>
                            <td>{r.get('developing')}</td>
                            <td>{r.get('exemplary')}</td>
                        </tr>
                    """
                rubric_html += """
                    </tbody>
                </table>
                """
                st.markdown(rubric_html, unsafe_allow_html=True)
            else:
                st.info("No evaluation rubric generated.")
                
        st.markdown("> [!NOTE]\n> *Assessment checks and rubric maps are built by **AssessmentAgent**.*")
        
    # ------------------------------------------
    # 5. CAREERS IN STEM TAB
    # ------------------------------------------
    with tab_careers:
        career_data = outputs.get("careers", {})
        
        # Sub-header with Download Tab Button
        col_tab_t, col_tab_d = st.columns([3, 1])
        with col_tab_t:
            st.markdown(f"### 🚀 Real-World STEM Careers & Inspiration")
            st.caption("Connecting target curriculum constructs to modern job opportunities.")
        with col_tab_d:
            tab_markdown = exporter.compile_careers_md(career_data)
            st.download_button(
                label="📥 Download Career Map (MD)",
                data=tab_markdown,
                file_name=f"careers_{st.session_state.topic.lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
                key="dl_careers_tab"
            )
            
        st.write("")
        
        # Career list spotlights
        st.markdown("#### 💼 Real-World Career Pathways")
        careers = career_data.get("careers", [])
        if careers:
            career_cols = st.columns(len(careers))
            for idx, c in enumerate(careers):
                with career_cols[idx]:
                    skills = c.get('key_skills', [])
                    skills_badges = "".join([f'<span class="badge-tag" style="background: rgba(168, 85, 247, 0.08); border-color: rgba(168, 85, 247, 0.25); color: #a855f7;">{s}</span>' for s in skills])
                    st.markdown(f"""
                    <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div class="card-title" style="color: #a855f7;">💼 {c.get('title')}</div>
                            <div style="font-size: 0.92rem; line-height:1.45; margin-bottom: 0.75rem;">{c.get('description')}</div>
                        </div>
                        <div>
                            <div style="font-weight: 700; color: #10b981; font-size: 1.05rem; margin-bottom: 0.5rem; margin-top:0.8rem;">💰 Range: {c.get('median_salary')}</div>
                            <div style="margin-top: 0.5rem;">{skills_badges}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No careers generated.")
            
        st.write("")
        
        # Role model spotlight
        st.markdown("#### 🌟 Role Model Spotlight")
        rm = career_data.get("role_model", {})
        if rm:
            st.markdown(f"""
            <div class="glass-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.04), rgba(236, 72, 153, 0.04)); border-color: rgba(99, 102, 241, 0.15);">
                <div class="card-title" style="color: #ec4899;">🌟 STEM Pioneer</div>
                <h4 style="margin: 0.2rem 0; font-family: 'Outfit', sans-serif; font-size:1.4rem;">{rm.get('name')}</h4>
                <div style="font-size: 0.95rem; margin-bottom: 0.75rem; line-height: 1.45;"><strong>Background</strong>: {rm.get('background')}</div>
                <div style="background: rgba(128, 128, 128, 0.08); border-left: 3px solid #ec4899; padding: 12px 16px; margin: 12px 0; border-radius: 6px; font-style: italic; line-height:1.4; font-size: 0.95rem;">
                    "{rm.get('quote')}"
                </div>
                <div style="font-size: 0.95rem; margin-top: 0.75rem; line-height:1.45;"><strong>Topic Connection</strong>: {rm.get('lesson_connection')}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("> [!NOTE]\n> *Role model profiles prioritize minority, female, and historically underrepresented pioneers, curated by **CareerAgent**.*")
        
    # ------------------------------------------
    # 6. PARENT REPORT TAB
    # ------------------------------------------
    with tab_parent:
        parent_data = outputs.get("parent_report", {})
        
        # Sub-header with Download Tab Button
        col_tab_t, col_tab_d = st.columns([3, 1])
        with col_tab_t:
            st.markdown(f"### 👪 Take-Home Parent Letter")
            st.caption(f"Translated to community language: **{parent_data.get('language_processed', st.session_state.lang)}**")
        with col_tab_d:
            tab_markdown = exporter.compile_parent_report_md(parent_data, st.session_state.topic, st.session_state.subject)
            st.download_button(
                label="📥 Download Parent Report (MD)",
                data=tab_markdown,
                file_name=f"parent_report_{st.session_state.topic.lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
                key="dl_parent_tab"
            )
            
        st.write("")
        
        col_p1, col_p2 = st.columns([3, 2])
        
        with col_p1:
            st.markdown("#### 💌 Home Correspondence")
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #14b8a6;">
                <div class="card-title" style="color: #14b8a6;">👪 Letter to Families</div>
                <div style="background: rgba(128,128,128,0.03); padding: 1.2rem; border-radius: 8px; border: 1px dashed rgba(128,128,128,0.18); margin-bottom: 0.5rem; font-family: 'Inter', sans-serif; line-height: 1.6; font-size:0.95rem;">
                    <p><strong>Subject:</strong> Exciting STEM Exploration: Learning about {st.session_state.topic}</p>
                    <hr style="border: 0; border-top: 1px solid rgba(128,128,128,0.15); margin: 0.8rem 0;" />
                    <p>Dear Family,</p>
                    <p>{parent_data.get('family_letter_intro')}</p>
                    <p>Best regards,<br/><em>The STEM Instruction Team</em></p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_p2:
            st.markdown("#### 🗣️ Home Conversation Starters")
            starters = parent_data.get("discussion_starters", [])
            if starters:
                for ds in starters:
                    st.markdown(f"""
                    <div style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px; background: rgba(128,128,128,0.04); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(128,128,128,0.08);">
                        <span style="font-size: 1.15rem; flex-shrink: 0;">🗣️</span>
                        <span style="font-size: 0.92rem; line-height:1.4;">{ds}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No conversation starters generated.")
                
            st.markdown("#### 🛠️ Joint 10-Minute Home Activity")
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #f59e0b;">
                <div class="card-title" style="color: #f59e0b;">🛠️ Collaborative Activity</div>
                <div style="font-size: 0.92rem; line-height: 1.45;">{parent_data.get('recommended_home_activity')}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("> [!NOTE]\n> *Parent reports are generated and translated by **ParentReportAgent** to foster student-family STEM discussions.*")
        
else:
    # Beautiful welcome page when no module has been generated yet
    st.info("👈 Select your parameters in the sidebar, add custom prompt constraints if needed, and hit **Generate STEM Module** to start!")
    
    col_mock1, col_mock2 = st.columns(2)
    with col_mock1:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title" style="color:#6366f1;">🌍 Global Context & Localization</div>
            Enable curriculum-aligned support across multiple world languages including Spanish, French, Arabic, Chinese, Portuguese, and Hindi. Fully translated outputs are ready for global community deployments.
        </div>
        <div class="glass-card">
            <div class="card-title" style="color:#a855f7;">🤖 Hands-on Maker Integration</div>
            Integrate electronics components, block pseudocode (micro:bit, Arduino MakeCode), or unplugged physical structures directly into standard standard alignments.
        </div>
        """, unsafe_allow_html=True)
        
    with col_mock2:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title" style="color:#ec4899;">📊 Differentiated Learning Paths</div>
            Scaffold content dynamically for levels ranging from early Kindergarten simple machines to Advanced High School level programming and mathematical models.
        </div>
        <div class="glass-card">
            <div class="card-title" style="color:#10b981;">👪 Parental Engagement Bridges</div>
            Generate localized home letters, discussion starters, and family activities designed in the target community language to bring learning home.
        </div>
        """, unsafe_allow_html=True)
