import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
Settings.llm = OpenAI(
        model="gpt-4o-mini",
        temperature=0,
        system_prompt="""基于知识库回答问题，保持您的回答简要准确，必须基于事实——不要凭空想象。""",
    )

class LlamaIndexAgent:
    def __init__(self, request):
        self.request = request

    def perceiver(self):
        content = SimpleDirectoryReader(input_dir=self.request, recursive=True)
        query = content.load_data()
        return query

    def actor(self):
        query = self.perceiver()
        index = VectorStoreIndex.from_documents(query)
        return index