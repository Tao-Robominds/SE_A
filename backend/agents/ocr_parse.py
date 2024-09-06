from pathlib import Path
from openai import OpenAI
from backend.plugins.ensure_local_file import EnsureLocalFile

import os
from dotenv import load_dotenv
load_dotenv()


class OCRAgent:
    def __init__(self, request):
        self.request = request
        self.client = OpenAI(
            api_key=os.getenv("MOONSHOT_API_KEY"),
            base_url="https://api.moonshot.cn/v1",
        )

    async def actor(self):
        file_name = EnsureLocalFile(str(self.request))
        file_object = self.client.files.create(file=Path(file_name), purpose="file-extract")
        file_content = self.client.files.content(file_id=file_object.id).json()
        result = file_content.get("content")
    
        return result