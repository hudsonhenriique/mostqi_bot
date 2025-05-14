from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from bot.scraper import run_bot
from models.outputs import SearchOutput

app = FastAPI(title="Bot API", description="API for the bot", version="1.0.0")

class BotRequest(BaseModel):
    cpf: Optional[str] = None
    nome: Optional[str] = None
    filtro_social: bool = True

@app.post("/bot", response_model=SearchOutput)
async def run_bot_endpoint(request: BotRequest):
    if not request.cpf and not request.nome:
        return SearchOutput(
            status="error",
            file=None,
            image_base64=None,
            query={
                "cpf": request.cpf,
                "nome": request.nome,
                "filtro_social": request.filtro_social
            },
            message="Please provide either cpf or nome."
        )

    result = await run_bot(
        cpf=request.cpf,
        name=request.nome,
        social_filter=request.filtro_social
    )
    return result
