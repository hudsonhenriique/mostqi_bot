import asyncio
from bot.scraper import rodar_bot

if __name__ == "__main__":
    asyncio.run(rodar_bot(cpf="12345678900", filtro_social=True))