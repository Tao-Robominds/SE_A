
from llama_parse import LlamaParse

import os
from dotenv import load_dotenv
load_dotenv()


class LlamaParseAgent:
    def __init__(self, request):
        self.request = request
        self.parser = LlamaParse(
            result_type="markdown",
            language="ch_sim",
            use_vendor_multimodal_model=True,
            vendor_multimodal_model_name="openai-gpt-4o-mini",
            vendor_multimodal_api_key=os.getenv("OPENAI_API_KEY"),
            parsing_instruction = """准确提取文档表格结构及所有内容。"""
        )

    async def actor(self):
        content = self.parser.load_data(self.request)
        response = content[0].text
    
        return response