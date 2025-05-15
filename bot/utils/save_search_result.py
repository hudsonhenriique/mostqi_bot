import os
from datetime import datetime
from models.outputs import SearchOutput
from bot.utils.image_to_base64 import image_to_base64
from bot.utils.json_helpers import save_json_output
from integrations.drive import upload_file_to_drive
from integrations.sheets import append_to_sheet

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

        result_data = {
            "status": "success",
            "file": None,
            "image_base64": None,
            "query": {
                "cpf": cpf,
                "name": name,
                "filtro_social": str(social_filter)
            }
        }

        json_path = save_json_output(result_data, file_base, output_dir)

        screenshot_drive_url = upload_file_to_drive(screenshot_path, f"{file_base}.png", mime_type="image/png")
        file_drive_url = upload_file_to_drive(json_path, f"{file_base}.json", mime_type="application/json")

        sheet_values = [timestamp, cpf or "-", name or "-", str(social_filter), screenshot_drive_url, file_drive_url]
        sheet_response = append_to_sheet(sheet_values)

        return SearchOutput(
            status="success",
            file=json_path,
            image_base64=image_base64_str,
            file_drive_url=file_drive_url,
            screenshot_drive_url=screenshot_drive_url,
            sheet_append_status=sheet_response.get("updates", {}).get("updatedCells"),
            query=result_data["query"]
        )

    except Exception as e:
        print(f"❌ Erro ao salvar resultados: {e}")
        return SearchOutput(
            status="error",
            file=None,
            image_base64=None,
            file_drive_url=None,
            screenshot_drive_url=None,
            sheet_append_status=None,
            query={
                "cpf": cpf,
                "name": name,
                "filtro_social": str(social_filter)
            },
            message=str(e)
        )