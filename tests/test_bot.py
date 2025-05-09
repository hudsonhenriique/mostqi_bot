import pytest
from bot.scraper import run_bot
from models.search_input import SearchInput

@pytest.mark.asyncio
async def test_run_bot_with_cpf():
    input_data = SearchInput(
        cpf="12345678900"
    )
    result = await run_bot(input_data)
    assert result.status in ("success", "error")
