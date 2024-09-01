
from llama_parse import LlamaParse

import os
from dotenv import load_dotenv
load_dotenv()


class LlamaParseAgent:
    def __init__(self, request):
        self.request = request
        self.parser = LlamaParse(
            result_type="markdown",
            language="en",
            use_vendor_multimodal_model=True,
            vendor_multimodal_model_name="openai-gpt-4o-mini",
            vendor_multimodal_api_key=os.getenv("OPENAI_API_KEY"),
            parsing_instruction = "Read the file and extract the content in markdown format."
        )

    def actor(self):
        content = self.parser.load_data(self.request)
        response = content[0].text
    
        return response