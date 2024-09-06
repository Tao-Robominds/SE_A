import streamlit as st
import os
import uuid
import asyncio
from backend.agents.ocr_parse import OCRAgent

async def process_file(file_path):
    agent = OCRAgent(file_path)
    return await agent.actor()

def file_upload():
    st.title("Project Files")
    uploaded_files = st.file_uploader("Upload files and click on 'Process'", accept_multiple_files=True)

    if st.button("Process"):
        if uploaded_files:
            session_id = str(uuid.uuid4())
            project_dir = os.path.join("data", "projects", session_id)
            os.makedirs(project_dir, exist_ok=True)
            
            content_file = os.path.join(project_dir, "content.md")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            async def process_all_files():
                tasks = []
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(project_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    tasks.append(process_file(file_path))
                
                total_files = len(tasks)
                for i, task in enumerate(asyncio.as_completed(tasks), 1):
                    content = await task
                    status_text.text(f"Processed file {i} of {total_files}")
                    
                    # Append the processed content to content.md
                    with open(content_file, "a") as f:
                        f.write(f"\n\n## Processed content for file {i}\n\n")
                        f.write(content)
                    
                    progress_bar.progress(i / total_files)
            
            # Run the async function
            asyncio.run(process_all_files())
            
            progress_bar.progress(1.0)
            status_text.text("Processing complete!")
            st.success(f"All files processed successfully! Content saved in: {content_file}")

            return content_file
        else:
            st.warning("Please upload files before processing.")
            return None
