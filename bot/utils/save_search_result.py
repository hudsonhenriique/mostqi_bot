import os
from datetime import datetime
from models.outputs import SearchOutput
from bot.utils.image_to_base64 import image_to_base64
from bot.utils.json_helpers import save_json_output
from integrations.drive import upload_file_to_drive
from integrations.sheets import append_to_sheet

async def save_search_result(page, cpf=None, name=None, social_filter=False, benefits_data=None) -> SearchOutput:
    try:
        
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'outputs'))
        os.makedirs(output_dir, exist_ok=True)

       
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_base = f"result_{timestamp}"

        
        if benefits_data and benefits_data.get("status") == "success":
            
            try:
                await page.wait_for_selector("text=TOTAL DE RECURSOS DISPONIBILIZADOS", state="visible", timeout=10000)
                print("📋 Taking screenshot of detailed benefits data...")
            except:
                
                await page.wait_for_selector("#countResultados", state="visible", timeout=40000)
                print("📋 Taking screenshot of search results...")
        else:
            
            await page.wait_for_selector("#countResultados", state="visible", timeout=40000)
            print("📋 Taking screenshot of search results...")

   
        screenshot_path = os.path.join(output_dir, f"{file_base}.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"📸 Screenshot saved locally at: {screenshot_path}")

        image_base64_str = image_to_base64(screenshot_path)

        result_data = {
            "query_info": {
                "cpf": cpf,
                "name": name,
                "social_filter": str(social_filter),
                "timestamp": timestamp
            },
            "benefits_data": benefits_data or {
                "status": "no_data",
                "message": "No benefits data collected"
            },
            "summary": {
                "total_benefits_found": benefits_data.get("total_benefits", 0) if benefits_data else 0,
                "collection_status": benefits_data.get("status", "unknown") if benefits_data else "no_collection",
                "has_detailed_data": bool(benefits_data and benefits_data.get("benefits"))
            }
        }
        
        json_path = save_json_output(result_data, file_base, output_dir)

       
        screenshot_drive_url = upload_file_to_drive(screenshot_path, f"{file_base}.png", mime_type='image/png')

        
        json_drive_url = upload_file_to_drive(json_path, f"{file_base}.json", mime_type='application/json')

       
        benefits_summary = "No benefits data"
        if benefits_data and benefits_data.get("benefits"):
            programs = [benefit.get("program", "Unknown") for benefit in benefits_data["benefits"]]
            benefits_summary = f"{len(programs)} programs: {', '.join(programs[:3])}" # First 3 programs
            if len(programs) > 3:
                benefits_summary += f" (+{len(programs)-3} more)"

        sheet_status = append_to_sheet([
            timestamp,
            cpf or "",
            name or "",
            str(social_filter),
            benefits_summary,
            screenshot_drive_url,
            json_drive_url
        ])

        print("✅ Data added to Google Sheets.")

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
                "filtro_social": str(social_filter),
                "benefits_collected": benefits_data.get("total_benefits", 0) if benefits_data else 0
            }
        )

    except Exception as e:
        print(f"❌ Error saving results: {e}")
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
