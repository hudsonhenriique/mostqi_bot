import os
from datetime import datetime
from models.outputs import SearchOutput
from bot.utils.image_to_base64 import image_to_base64
from bot.utils.json_helpers import save_json_output

async def save_search_result(page, cpf=None, name=None, social_filter=False) -> SearchOutput:
    try:
        
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'outputs'))
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_base = f"result_{timestamp}"

        screenshot_path = os.path.join(output_dir, f"{file_base}.png")
        await page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot salvo como: {screenshot_path}")

        image_base64_str = image_to_base64(screenshot_path)

        result = SearchOutput(
            status="success",
            file=screenshot_path,
            image_base64=image_base64_str,
            query={
                "cpf": cpf,
                "name": name,
                "filtro_social": str(social_filter)
            }
        )

        save_json_output(result.model_dump(), file_base, output_dir)
        return result

    except Exception as e:
        print(f"❌ Erro ao salvar resultados: {e}")
        return SearchOutput(
            status="error",
            file=None,
            image_base64=None,
            query={
                "cpf": cpf,
                "name": name,
                "filtro_social": str(social_filter)
            },
            message=str(e)
        )
