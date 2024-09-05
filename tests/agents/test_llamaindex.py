import warnings
warnings.filterwarnings("ignore")


from pytest import mark
from backend.agents.llamaindex import LlamaIndexAgent as Agent
import nest_asyncio
nest_asyncio.apply()
import time


@mark.agent
@mark.llamaindex
class AgentTests:
    def test_agent_behaviours(self):
        request = """backend/data/projects/streamlit/installation/"""
        begin = time.time()
        agent_instance = Agent(request)
        response = agent_instance.actor()
        end = time.time()
        print(response)
        print(f"Time taken: {end - begin}")
        assert response is not None