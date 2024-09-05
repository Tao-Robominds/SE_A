import warnings
warnings.filterwarnings("ignore")

from pytest import mark
from backend.agents.ocr_moonshot import OCRAgent as Agent


@mark.asyncio
@mark.agent
@mark.ocr
class AgentTests:
    async def test_agent_behaviours(self):
        request = """backend/data/projects/bot/pdf/数字品控.pdf"""
        agent_instance = Agent(request)
        result = await agent_instance.actor()
        print(result)
        assert result is not None