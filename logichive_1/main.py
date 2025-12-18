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
    # Adjust paths as necessary. Assuming main.py is in the same dir as the other files.
    interview_module = load_module("interview_100", "100interview.py")
    system_arch_module = load_module("system_arch", "systemarch.py")
except FileNotFoundError:
    st.error("Could not find the page files. Please ensure '100interview.py' and 'systemarch.py' are in the same directory.")
    st.stop()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Interview Questions", "System Architecture"])

if page == "Interview Questions":
    interview_module.app()
elif page == "System Architecture":
    system_arch_module.app()
