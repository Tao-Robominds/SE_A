import streamlit as st
st.set_page_config(page_title="NASA System Engineering Workflow", layout="wide")

import json
import os
import tempfile

import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from backend.agents.llama_parse import LlamaParseAgent

def main():
    # Custom CSS to set sidebar width
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            min-width: 20%;
            max-width: 20%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("NASA System Engineering Workflow")

    # Sidebar for file upload
    with st.sidebar:
        st.title("Project Files")
        uploaded_files = st.file_uploader("Upload files and click on 'Process'", accept_multiple_files=True)

        if st.button("Process"):
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    temp_dir = tempfile.mkdtemp()
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    response = parser(file_path)

                    st.success(f"File '{uploaded_file.name}' processed successfully!")
                    st.write(response)

                st.session_state.conversation = "All files processed"
            else:
                st.error("Please upload at least one file before processing.")

    # Get the workflow structure from the JSON file
    workflow_structure = get_workflow_structure()

    # Create main tabs based on the workflow structure
    main_tabs = st.tabs(workflow_structure.keys())

    for i, (main_tab, sub_tabs) in enumerate(workflow_structure.items()):
        with main_tabs[i]:
            st.header(main_tab)
            sub_tab_names = list(sub_tabs.keys())
            sub_tabs_ui = st.tabs(sub_tab_names)
            for j, sub_tab in enumerate(sub_tab_names):
                with sub_tabs_ui[j]:
                    display_tab_content(f"{main_tab}/{sub_tab}")

@st.cache_resource(show_spinner=False)
def parser(file_path):
    agent_instance = LlamaParseAgent(file_path)
    response = agent_instance.actor()
    return response

def get_workflow_structure():
    with open("backend/workflows/processes.json", "r") as f:
        return json.load(f)

def display_tab_content(tab_path):
    workflow_structure = get_workflow_structure()
    main_tab, sub_tab = tab_path.split('/')
    
    if main_tab in workflow_structure and sub_tab in workflow_structure[main_tab]:
        content = workflow_structure[main_tab][sub_tab]
        st.subheader(sub_tab)
        st.write(content)
    else:
        st.write(f"Content for {tab_path} not found in the JSON file.")

if __name__ == "__main__":
    main()
