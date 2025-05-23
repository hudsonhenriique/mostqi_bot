from playwright.async_api import Page

async def perform_search(page: Page):
    try:
        print("🔍 Performing the search...")
        
        try:
            await page.locator(".br-modal-close").click(timeout=2000)
        except:
            pass

        button = page.locator("#btnConsultarPF")
        await button.wait_for(state="visible", timeout=15000)
        await page.wait_for_timeout(2000)
        await button.click(force=True)
 
        
        print("✅ Search button clicked successfully.")
        await page.wait_for_selector("#countResultados", state="visible", timeout=40000)
    
    except Exception as e:
        print(f"❌ An error occurred while performing the search: {e}")
        raise e
