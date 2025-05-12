async def individual_consultation(page):
    try:
        print("Clicking on 'Individual Consultation'...")
        await page.wait_for_selector("#button-consulta-pessoa-fisica", state="visible",timeout = 30000)
        await page.click("#button-consulta-pessoa-fisica")
        await page.wait_for_load_state("networkidle")
        
        # Aguarde o campo de busca aparecer após o clique
        await page.wait_for_selector("#termo", state="visible", timeout=15000)  # Aumente o timeout
    except Exception as e:
        print(f"Error in individual consultation: {e}")
        
