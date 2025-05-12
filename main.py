import asyncio
from bot.scraper import run_bot

if __name__ == "__main__":
    name = None
    cpf = "12345678900"  
    social_filter = True
    try:
        result = asyncio.run(run_bot(name=name, cpf=cpf, social_filter=social_filter))
        print(result)
    except Exception as e:
        print(f"Error running the bot: {e}")