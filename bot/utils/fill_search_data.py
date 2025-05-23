from playwright.async_api import Page

async def fill_search_data(page: Page, cpf=None, name=None, social_filter=False):
    try:
        print("📝 Filling in the search data...")

        await page.wait_for_selector("#termo", state="visible", timeout=20000)
        field = page.locator("#termo")
        await field.scroll_into_view_if_needed()
        if cpf:
            await field.fill(cpf)
            await field.dispatch_event("blur")
        elif name:
            await field.fill(name)

        if social_filter:
            print("🔍 Applying social program filter...")
            checkbox_selector = "#beneficiarioProgramaSocial"
            
            refine_button = page.locator('button[aria-controls="box-busca-refinada"]')
            await refine_button.wait_for(state="visible", timeout=5000)
            await refine_button.click()
            await page.wait_for_selector('#box-busca-refinada', state="visible", timeout=5000)
            checkbox = page.locator(checkbox_selector)
            await checkbox.wait_for(state="visible", timeout=10000)
            
            await checkbox.set_checked(True, force=True)
           
            if not await checkbox.is_checked():
                raise Exception("❌ Unable to set social filter!")
            print("✅ Social filter marked successfully.")

        print("✅ Search data filled successfully.")

    except Exception as e:
        print(f"❌ Search data filling failed: {str(e)}")
        raise e
