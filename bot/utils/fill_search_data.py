async def fill_search_data(page, cpf=None, name=None, social_filter=False):
    try:
        print("Filling in the search data...")
        
        # Espere o campo estar visível (já deveria estar garantido por individual_consultation)
        await page.wait_for_selector("#termo", state="visible", timeout=15000)
        
        if cpf:
            await page.fill("#termo", cpf)
        elif name:
            await page.fill("#termo", name)

        # Filtro social
        if social_filter:
            print("Applying social program filter...")
            await page.wait_for_selector("button:has-text('Refine a Busca')", state="visible", timeout=5000)
            await page.click("button:has-text('Refine a Busca')")
            
            checkbox_selector = "#beneficiarioProgramaSocial"
            await page.wait_for_selector(checkbox_selector, state="visible", timeout=5000)
            await page.locator(checkbox_selector).scroll_into_view_if_needed()
            
            try:
                await page.check(checkbox_selector, force=True)
            except Exception as e:
                print(f"Using alternative method to check: {e}")
                await page.click(f"label[for='{checkbox_selector.lstrip('#')}']")

    except Exception as e:
        print(f"Search data filling failed: {str(e)}")
        

