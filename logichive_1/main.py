import streamlit as st
import importlib.util
import sys
import os

# Page Configuration
st.set_page_config(
    page_title="LogicHive Interview Prep",
    page_icon="🐝",
    layout="wide"
)

# Import the page modules
# Since the filenames have spaces or start with numbers, we need to import them dynamically or rename them.
# However, the user asked to connect existing files.
# Let's try to import them assuming they are in the same directory.

def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Load the modules
try:
    # Get the directory where main.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct absolute paths to the sibling files
    interview_path = os.path.join(current_dir, "100interview.py")
    system_arch_path = os.path.join(current_dir, "systemarch.py")

    interview_module = load_module("interview_100", interview_path)
    system_arch_module = load_module("system_arch", system_arch_path)
except FileNotFoundError:
    st.error(f"Could not find the page files. looked in {current_dir}")
    st.stop()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Interview Questions", "System Architecture"])

if page == "Interview Questions":
    interview_module.app()
elif page == "System Architecture":
    system_arch_module.app()
