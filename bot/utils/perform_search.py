async def perform_search(page):
   
    try:
        print("Performing the search...")
        await page.wait_for_selector("#btnConsultarPF", state="visible")
        await page.click("#btnConsultarPF")
        await page.wait_for_selector("#countResultados", state="visible", timeout=60000)
        await page.locator("#countResultados").scroll_into_view_if_needed()
        await page.wait_for_timeout(2000)
    except Exception as e:
        print(f"An error occurred while performing the search: {e}")
