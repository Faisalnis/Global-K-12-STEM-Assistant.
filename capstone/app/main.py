# app/main.py

import os
import sys

def main():
    """
    Main entry point for the Global K-12 STEM Assistant.
    Launches the Streamlit application.
    """
    print("=" * 60)
    print("Launching Global K-12 STEM Assistant...")
    print("=" * 60)
    
    # Locate the streamlit_app.py in the same folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "streamlit_app.py")
    
    if not os.path.exists(app_path):
        print(f"Error: Could not find streamlit_app.py at {app_path}")
        sys.exit(1)
        
    # Execute the streamlit command
    os.system(f"streamlit run \"{app_path}\"")

if __name__ == "__main__":
    main()
