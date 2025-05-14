from datetime import datetime
from dataclasses import asdict
from bot.utils.image_to_base64 import image_to_base64
from bot.utils.json_helpers import save_json_output
from models.outputs import SearchOutput

async def save_search_result(page, cpf=None, name=None, social_filter=False) -> SearchOutput:
    try:
        # Gera nome com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"result_{timestamp}.png"

        # Tira screenshot
        await page.screenshot(path=file_name)
        print(f"Search completed. Screenshot saved as {file_name}")

        # Converte imagem para base64
        image_base64_str = image_to_base64(file_name)

        # Cria objeto de saída
        result = SearchOutput(
            status="success",
            file=file_name,
            image_base64=image_base64_str,
            query={
                "cpf": cpf,
                "nome": name,
                "filtro_social": social_filter
            }
        )

        # Salva JSON no disco
        file_base = file_name.replace(".png", "")
        save_json_output(asdict(result), file_base)

        return result

    except Exception as e:
        print(f"Error saving search results: {e}")
        return SearchOutput(
            status="error",
            file=None,
            image_base64=None,
            query={
                "cpf": cpf,
                "nome": name,
                "filtro_social": social_filter
            },
            message=str(e)
        )