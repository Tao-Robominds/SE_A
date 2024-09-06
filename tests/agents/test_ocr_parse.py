import warnings
warnings.filterwarnings("ignore")

from pytest import mark
from backend.agents.ocr_parse import OCRAgent as Agent


@mark.asyncio
@mark.agent
@mark.ocr_parse
class AgentTests:
    async def test_agent_behaviours(self):
        request = """backend/data/projects/bot/img/数字品控/数字品控-06.jpg"""
        agent_instance = Agent(request)
        result = await agent_instance.actor()
        print(result)
        assert result is not None