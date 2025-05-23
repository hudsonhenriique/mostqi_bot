import os
from datetime import datetime
from models.outputs import SearchOutput
from bot.utils.image_to_base64 import image_to_base64
from bot.utils.json_helpers import save_json_output
from integrations.drive import upload_file_to_drive
from integrations.sheets import append_to_sheet

async def save_search_result(page, cpf=None, name=None, social_filter=False) -> SearchOutput:
    try:
        # folder outputs
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'outputs'))
        os.makedirs(output_dir, exist_ok=True)

        # Generate base name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_base = f"result_{timestamp}"

        # screenshot
        await page.wait_for_selector("#countResultados", state="visible", timeout=40000)
        screenshot_path = os.path.join(output_dir, f"{file_base}.png")
        await page.screenshot(path=screenshot_path,full_page=True)
        print(f"📸 Screenshot salvo localmente em: {screenshot_path}")

        image_base64_str = image_to_base64(screenshot_path)

        # JSON output
        result_data = {
            "cpf": cpf,
            "name": name,
            "filtro_social": str(social_filter),
            "timestamp": timestamp
        }
        json_path = save_json_output(result_data, file_base, output_dir)

        # Upload image to Google Drive
        screenshot_drive_url = upload_file_to_drive(screenshot_path, f"{file_base}.png", mime_type='image/png')

        # Upload JSON to Google Drive
        json_drive_url = upload_file_to_drive(json_path, f"{file_base}.json", mime_type='application/json')

        # Add entry to Google Sheets
        sheet_status = append_to_sheet([
            timestamp,
            cpf or "",
            name or "",
            str(social_filter),
            screenshot_drive_url,
            json_drive_url
        ])

        print("✅ Dados adicionados ao Google Sheets.")

        return SearchOutput(
            status="success",
            file=screenshot_path,
            image_base64=image_base64_str,
            file_drive_url=json_drive_url,
            screenshot_drive_url=screenshot_drive_url,
            sheet_append_status="OK" if sheet_status else "Failed",
            query={
                "cpf": cpf,
                "name": name,
                "filtro_social": str(social_filter)
            }
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
