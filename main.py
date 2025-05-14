import asyncio
import json
from bot.scraper import run_bot
from models.outputs import SearchOutput

def main():
    name = None
    cpf = "12345678900"
    social_filter = True

    try:
        
        output = asyncio.run(run_bot(name=name, cpf=cpf, social_filter=social_filter))
    except Exception as e:
        print(f"Error running the bot: {e}")
        return None

    # Retorna o JSON limpo
    return output.to_clean_dict()

if __name__ == "__main__":
    output = main()
    if output:
        # Converte o dicionário para JSON formatado
        print(json.dumps(output, indent=2, ensure_ascii=False))