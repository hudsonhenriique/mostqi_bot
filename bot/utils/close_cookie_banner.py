async def close_cookie_banner(page):
    try:
        print("Trying to close the cookie banner...")
        await page.wait_for_selector('button:has-text("Aceitar")', timeout=3000)
        await page.click('button:has-text("Aceitar")')
        print("Cookie banner successfully closed.")
    except Exception as e:
        print("Error while closing the cookie banner:", str(e))
