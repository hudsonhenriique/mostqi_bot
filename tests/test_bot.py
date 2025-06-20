import pytest
from bot.scraper import run_bot
from models.outputs import SearchOutput

@pytest.mark.asyncio
async def test_run_bot_with_cpf():
    cpf = "12345678900"  # vauelue for testing

    result = await run_bot(cpf=cpf,social_filter=True)

    assert isinstance(result, SearchOutput)
    assert result.status in ("success", "error")

    if result.status == "success":
        assert result.file is not None
        assert result.image_base64 is not None
        assert "cpf" in result.query
        assert result.query["filtro_social"] is True