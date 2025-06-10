from playwright.async_api import async_playwright
from bot.utils.access_consultation_page import access_consultation_page
from bot.utils.individual_consultation import individual_consultation
from bot.utils.close_cookie_banner import close_cookie_banner
from bot.utils.save_search_result import save_search_result
from bot.utils.perform_search import perform_search
from bot.utils.fill_search_data import fill_search_data
from bot.utils.collect_benefits import collect_benefits_data
from models.outputs import SearchOutput


async def run_bot(name=None, cpf=None, social_filter=False) -> SearchOutput:
    if not (name or cpf):
        raise ValueError("Name or CPF must be provided.")

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = await browser.new_context(
            viewport=None,
            no_viewport=True,
        )  
        page = await context.new_page()

        try:
            # Step 1: Access consultation page and handle cookie banner
            await access_consultation_page(page)
            await close_cookie_banner(page)
            
            # Step 2: Navigate to individual consultation
            await individual_consultation(page)
            await close_cookie_banner(page)
            
            # Step 3: Fill search data (CPF/Name and social filter)
            await fill_search_data(page, cpf=cpf, name=name, social_filter=social_filter)
            
            # Step 4: Perform search to get results list
            await perform_search(page)
            
            # Step 5: Collect detailed benefits data (click "Detalhar", extract table data)
            benefits_data = await collect_benefits_data(page)
            print(f"✅ Benefits data collection completed. Found {benefits_data.get('total_benefits', 0)} programs")
            
            # Step 6: Save results with benefits data included
            result = await save_search_result(
                page, 
                cpf=cpf, 
                name=name, 
                social_filter=social_filter,
                benefits_data=benefits_data
            )
            
            return result

        except Exception as error:
            print(f"❌ An error occurred during automation: {error}")
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
                message=str(error)
            )

        finally:
            await browser.close()
            print("Browser closed")
