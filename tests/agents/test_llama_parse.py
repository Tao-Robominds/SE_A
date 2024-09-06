import warnings
warnings.filterwarnings("ignore")

from pytest import mark
from backend.agents.llama_parse import LlamaParseAgent as Agent
import nest_asyncio
nest_asyncio.apply()
import time

@mark.asyncio
@mark.agent
@mark.llama_parse
class AgentTests:
    async def test_agent_behaviours(self):
        request = """backend/data/projects/bot/img/数字品控/数字品控-06.jpg"""
        begin = time.time()
        agent_instance = Agent(request)
        response = await agent_instance.actor()
        end = time.time()
        print(response)
        print(f"Time taken: {end - begin}")
        assert response is not None