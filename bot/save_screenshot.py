async def save_screenshot(page, filename):
    # Save a screenshot of the page
    await page.screenshot(path=filename)
    print(f"Screenshot saved as {filename}")
    return filename
