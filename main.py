import sys
import asyncio

# Workaround for Windows to use the ProactorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from models.outputs import SearchOutput
from bot.scraper import run_bot
import json
from typing import Optional

app = FastAPI()

class BotRequest(BaseModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    social_filter: bool = True

@app.post("/bot", response_model=SearchOutput)
async def run_bot_endpoint(request: BotRequest = Body(...)):
    try:
        return await run_bot(
            name=request.name,
            cpf=request.cpf,
            social_filter=request.social_filter
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def async_main(cpf: Optional[str], name: Optional[str], social_filter: bool = True):
    try:
        output = await run_bot(name=name, cpf=cpf, social_filter=social_filter)
        print(json.dumps(output.model_dump(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import argparse

    # Argument parser for CLI
    parser = argparse.ArgumentParser(description="Run the bot as API or CLI")
    parser.add_argument("--api", action="store_true", help="Start the API server")
    parser.add_argument("--cpf", type=str, help="CPF to search (CLI mode)")
    parser.add_argument("--name", type=str, help="Name to search (CLI mode)")
    parser.add_argument("--social_filter", action="store_true", help="Enable social filter")
    
    args = parser.parse_args()

    if args.api:
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8080)
    else:
        # Verificação modificada para aceitar CPF ou Nome
        if not args.cpf and not args.name:
            print("❌ CPF or Name is required in CLI mode. Use --cpf <number> or --name <name>")
            sys.exit(1)
        asyncio.run(async_main(
            cpf=args.cpf,
            name=args.name,
            social_filter=args.social_filter
        ))