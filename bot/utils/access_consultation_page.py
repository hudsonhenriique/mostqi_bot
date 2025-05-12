from playwright.async_api import TimeoutError as PlaywrightTimeoutError

async def access_consultation_page(page):
    try:
        print("Accessing consultation page...")
        await page.goto("https://www.portaldatransparencia.gov.br/pessoa/visao-geral", wait_until="networkidle")  # Espere rede parar
        await page.wait_for_selector("#button-consulta-pessoa-fisica", state="attached", timeout=15000)
    except Exception as e:
        print(f"Erro ao acessar página: {e}")