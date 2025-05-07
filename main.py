import asyncio
from bot.scraper import rodar_bot

if __name__ == "__main__":
    nome = None
    cpf = "12345678900"  # Exemplo de CPF
    filtro_social = True
    try:
        resultado = asyncio.run(rodar_bot(nome=nome, cpf=cpf, filtro_social=filtro_social))
        print(resultado)
    except Exception as e:
        print(f"Erro ao executar o bot: {e}")