from playwright.async_api import async_playwright

async def rodar_bot(nome=None, cpf=None, filtro_social=False):
    if not (nome or cpf):
        raise ValueError("É necessário fornecer nome ou CPF.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  
        page = await browser.new_page()

        
        await page.goto("https://www.portaltransparencia.gov.br/")
        print("Página carregada com sucesso.")

       
        await page.screenshot(path="evidencia.png")
        print("Screenshot salva.")

        await browser.close()