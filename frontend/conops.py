import streamlit as st
import os
from frontend.components.file_upload import file_upload

def main():
    st.set_page_config(page_title="Concept of Operations", layout="wide")
    st.title("Concept of Operations")

    # Sidebar for file upload and processing
    with st.sidebar:
        content_file = file_upload()

    # Main content area
    if content_file and os.path.exists(content_file):
        with open(content_file, "r") as f:
            content = f.read()
        st.markdown(content)
    else:
        st.info("Please upload files and process them first.")

if __name__ == "__main__":
    main()