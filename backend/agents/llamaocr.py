import asyncio
from pathlib import Path
from openai import OpenAI
from llama_parse import LlamaParse
from backend.plugins.ensure_local_file import EnsureLocalFile
from backend.agents.llama_parse import LlamaParseAgent
from backend.agents.ocr_parse import OCRAgent
import os
from dotenv import load_dotenv

load_dotenv()

class LlamaOCRAgent:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ocr_client = OpenAI(
            api_key=os.getenv("MOONSHOT_API_KEY"),
            base_url="https://api.moonshot.cn/v1",
        )
        self.llama_parser = LlamaParse(
            result_type="markdown",
            use_vendor_multimodal_model=True,
            vendor_multimodal_model_name="openai-gpt-4o-mini",
            vendor_multimodal_api_key=os.getenv("OPENAI_API_KEY"),
        )

    async def ocr_process(self):
        file_name = EnsureLocalFile(str(self.file_path))
        file_object = self.ocr_client.files.create(file=Path(file_name), purpose="file-extract")
        file_content = self.ocr_client.files.content(file_id=file_object.id).json()
        return file_content.get("content")

    async def llama_process(self):
        content = self.llama_parser.load_data(self.file_path)
        return content[0].text if content else ""

    async def actor(self):
        ocr_task = asyncio.create_task(self.ocr_process())
        llama_task = asyncio.create_task(self.llama_process())

        ocr_result, llama_result = await asyncio.gather(ocr_task, llama_task)

        combined_result = f"OCR Result:\n\n{ocr_result}\n\nLlama Parse Result:\n\n{llama_result}"
        return combined_result
