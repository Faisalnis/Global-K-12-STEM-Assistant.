# app/config.py

import os

# Application Metadata
APP_NAME = "Global K-12 STEM Assistant"
APP_ICON = "🌍"

# Supported Grade Levels
GRADE_LEVELS = [
    "Kindergarten",
    "Elementary School (Grades 1-5)",
    "Middle School (Grades 6-8)",
    "High School (Grades 9-12)"
]

# Supported STEM Subjects
SUBJECTS = [
    "Science",
    "Technology",
    "Engineering",
    "Mathematics"
]

# Standard STEM Topics grouped by Subject
TOPICS = {
    "Science": [
        "Physics & Forces",
        "Chemistry & Matter",
        "Biology & Ecosystems",
        "Earth & Space Science",
        "Environmental Science & Climate"
    ],
    "Technology": [
        "Intro to Programming (Python/Scratch)",
        "Digital Literacy & Internet Safety",
        "Cybersecurity Basics",
        "Artificial Intelligence & Machine Learning",
        "Web Development"
    ],
    "Engineering": [
        "Simple Machines & Structures",
        "Robotics & Arduino/Micro:bit",
        "Civil & Structural Engineering",
        "Aerospace & Flight Mechanics",
        "Renewable Energy Systems"
    ],
    "Mathematics": [
        "Arithmetic & Number Sense",
        "Algebraic Thinking",
        "Geometry & Spatial Reasoning",
        "Probability & Data Analysis",
        "Calculus & Functions"
    ]
}

# Supported Languages
LANGUAGES = [
    "English",
    "Spanish (Español)",
    "French (Français)",
    "Arabic (العربية)",
    "Chinese (中文)",
    "Portuguese (Português)",
    "Hindi (हिन्दी)"
]
