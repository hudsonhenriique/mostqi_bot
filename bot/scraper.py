from playwright.async_api import async_playwright
from datetime import datetime

async def rodar_bot(nome=None, cpf=None, filtro_social=False):
    if not (nome or cpf):
        raise ValueError("É necessário fornecer nome ou CPF.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            print("Acessando a página de consulta...")
            await page.goto("https://www.portaldatransparencia.gov.br/pessoa/visao-geral")
            await page.wait_for_timeout(2000)

            try:
                print("Verificando se há banner de cookies...")
                await page.wait_for_selector('button:has-text("Aceitar")', timeout=3000)
                await page.click('button:has-text("Aceitar")')
                print("Banner de cookies fechado.")
            except Exception as e:
                print("Nenhum banner de cookies encontrado ou ele já foi fechado:", str(e))

            print("Clicando em 'Consulta de pessoa física'...")
            await page.wait_for_selector("#button-consulta-pessoa-fisica", state="visible")
            await page.click("#button-consulta-pessoa-fisica")
            await page.wait_for_timeout(2000)

            try:
                print("Verificando se há banner de cookies...")
                await page.wait_for_selector('button:has-text("Aceitar")', timeout=3000)
                await page.click('button:has-text("Aceitar")')
                print("Banner de cookies fechado.")
            except Exception as e:
                print("Nenhum banner de cookies encontrado ou ele já foi fechado:", str(e))

            print("Preenchendo os dados de busca...")
            if cpf:
                await page.fill('#termo', cpf)
            elif nome:
                await page.fill('#termo', nome)

            if filtro_social:
                print("Expandindo a seção 'Refine a Busca'...")
                await page.wait_for_selector("button:has-text('Refine a Busca')", state="visible")
                await page.click("button:has-text('Refine a Busca')")

                await page.wait_for_selector("#beneficiarioProgramaSocial", state="visible")
                await page.locator("#beneficiarioProgramaSocial").scroll_into_view_if_needed()
                await page.wait_for_timeout(500)

                print("Marcando o filtro 'Beneficiário de Programa Social'...")
                try:
                    await page.check("#beneficiarioProgramaSocial", force=True)
                except Exception as e:
                    print("Checkbox bloqueado, tentando clicar no label:", str(e))
                    await page.click("label[for='beneficiarioProgramaSocial']")

            print("Realizando a busca...")
            await page.wait_for_selector("#btnConsultarPF", state="visible")
            await page.click("#btnConsultarPF")
            await page.wait_for_selector("#countResultados", state="visible", timeout=60000)
            await page.locator("#countResultados").scroll_into_view_if_needed()
            await page.wait_for_timeout(2000)

            # Nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"resultado_{timestamp}.png"

            await page.screenshot(path=file_name)
            print(f"Busca concluída. Screenshot salva como {file_name}")

            return {
                "status": "sucesso",
                "arquivo": file_name,
                "consulta": {"cpf": cpf, "nome": nome, "filtro_social": filtro_social}
            }

        except Exception as e:
            print("❌ Ocorreu um erro durante a automação:", str(e))
            return {
                "status": "erro",
                "mensagem": str(e)
            }

        finally:
            await browser.close()
            print("Navegador fechado.")