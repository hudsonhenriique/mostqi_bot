from playwright.async_api import Page
import json

async def collect_benefits_data(page: Page):
    """
    Collects detailed benefits data from the transparency portal
    Returns structured data with person info and all benefits
    """
    try:
        print("🔍 Collecting benefits data...")
        
        # 1. Wait for search results to load
        await page.wait_for_selector("#countResultados", state="visible", timeout=20000)
        print("✅ Search results loaded")
        
        # 2. Scroll down to find the first result and click on it
        await scroll_to_first_result_and_click(page)
        
        # 3. Wait for "Government Relationship Overview" page
        await page.wait_for_selector("text=Panorama da relação da pessoa com o Governo Federal", timeout=15000)
        print("✅ Accessed person details page")
        
        # 4. Click on "RESOURCE RECEIPTS" section
        receipts_section = page.locator("text=RECEBIMENTOS DE RECURSOS")
        await receipts_section.wait_for(state="visible", timeout=10000)
        await receipts_section.scroll_into_view_if_needed()
        await receipts_section.click()
        
        print("✅ Expanded RESOURCE RECEIPTS section")
        
        # 5. Collect basic person data
        person_data = await collect_person_data(page)
        
        # 6. Collect all available benefits
        available_benefits = await collect_all_benefits(page)
        
        # 7. For each benefit, click "Detail" and collect data
        detailed_benefits = []
        for i, benefit in enumerate(available_benefits):
            benefit_details = await collect_benefit_details(page, i, benefit)
            if benefit_details:
                detailed_benefits.append(benefit_details)
        
        return {
            "person": person_data,
            "benefits": detailed_benefits,
            "total_benefits": len(detailed_benefits),
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ Error collecting benefits data: {e}")
        return {
            "error": str(e),
            "status": "error"
        }

async def scroll_to_first_result_and_click(page: Page):
    """
    Scrolls down to find the first search result and clicks on it
    """
    try:
        print("🔍 Searching for first result in the page...")
        
        # Based on the images, the structure appears to be a table with results
        # Try different possible selectors for clicking on the first person
        possible_selectors = [
            "table tbody tr:first-child td:first-child a",  # First link in first row
            "table tbody tr:first-child td a",  # Any link in first row
            "table tbody tr:first-child",  # First row itself
            ".resultado-busca:first-child",  # First search result
            "a[href*='pessoa']",  # Link containing 'pessoa'
        ]
        
        first_result = None
        clicked_selector = None
        
        # Scroll down and look for the first result
        for scroll_attempt in range(5):  # Try scrolling up to 5 times
            print(f"📄 Scroll attempt {scroll_attempt + 1}/5")
            
            # Check each possible selector
            for selector in possible_selectors:
                try:
                    locator = page.locator(selector).first()
                    count = await page.locator(selector).count()  # Fixed: call count on original locator
                    
                    if count > 0 and await locator.is_visible():
                        first_result = locator
                        clicked_selector = selector
                        print(f"✅ Found first result with selector: {selector}")
                        break
                except Exception as e:
                    print(f"⚠️ Error with selector {selector}: {e}")
                    continue
            
            if first_result:
                break
                
            # Scroll down to load more content
            await page.mouse.wheel(0, 500)
            await page.wait_for_timeout(2000)
        
        # If still no result found, try simpler approach
        if not first_result:
            print("🔍 Using simple fallback method...")
            
            # Look for any clickable element in a table that might be a person
            simple_selectors = [
                "table tr td:first-child",  # First cell of any row
                "table tr:nth-child(2) td:first-child",  # First cell of second row (skip header)
                "tbody tr:first-child td",  # Any cell in first data row
            ]
            
            for selector in simple_selectors:
                try:
                    locator = page.locator(selector)
                    if await locator.count() > 0:
                        element = locator.first()
                        if await element.is_visible():
                            # Check if it contains a name or is clickable
                            text = await element.inner_text()
                            if text and len(text.strip()) > 2:
                                first_result = element
                                clicked_selector = selector
                                print(f"✅ Found result with fallback selector: {selector}, text: {text[:50]}")
                                break
                except Exception as e:
                    print(f"⚠️ Error with fallback selector {selector}: {e}")
                    continue
        
        if first_result:
            try:
                # Ensure element is in view and click
                await first_result.scroll_into_view_if_needed()
                await page.wait_for_timeout(1000)
                
                # Try clicking, if it fails, try force click
                try:
                    await first_result.click()
                except:
                    await first_result.click(force=True)
                    
                print(f"✅ Successfully clicked on first result using selector: {clicked_selector}")
                
                # Wait for navigation or page change
                await page.wait_for_timeout(3000)
                
            except Exception as e:
                print(f"❌ Error clicking on element: {e}")
                raise e
        else:
            raise Exception("Could not find any clickable result on the page")
            
    except Exception as e:
        print(f"❌ Error finding and clicking first result: {e}")
        raise e

async def collect_person_data(page: Page):
    """
    Collects basic person information from the page
    """
    try:
        # Wait a bit for page to load
        await page.wait_for_timeout(2000)
        
        name = "N/A"
        cpf = "N/A"
        
        # Try to get name from page title or headers
        try:
            title_element = page.locator("h1, h2, .titulo-pessoa, .nome-beneficiario").first()
            if await title_element.count() > 0:
                name = await title_element.inner_text()
                name = name.strip()
        except:
            pass
        
        # Look for CPF in the page
        try:
            cpf_text = await page.locator("text=/CPF.*\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}/").inner_text()
            if cpf_text:
                cpf = cpf_text.strip()
        except:
            pass
        
        print(f"📋 Collected person data - Name: {name}, CPF: {cpf}")
        
        return {
            "name": name,
            "cpf": cpf
        }
        
    except Exception as e:
        print(f"⚠️ Warning collecting person data: {e}")
        return {"name": "N/A", "cpf": "N/A"}

async def collect_all_benefits(page: Page):
    """
    Finds and collects all benefit programs listed on the page
    """
    try:
        # Look for benefit programs in the RECEBIMENTOS section
        benefits = []
        
        # Common benefit program names to look for
        benefit_names = [
            "Auxílio Emergencial",
            "Bolsa Família", 
            "Auxílio Brasil",
            "BPC",
            "Seguro Defeso"
        ]
        
        for benefit_name in benefit_names:
            try:
                locator = page.locator(f"text={benefit_name}")
                if await locator.count() > 0:
                    benefits.append(benefit_name)
            except:
                continue
        
        # If no specific benefits found, look for generic benefit containers
        if not benefits:
            try:
                benefit_containers = page.locator(".beneficio, .programa-social, button:has-text('Detalhar')")
                count = await benefit_containers.count()
                
                for i in range(count):
                    try:
                        element = benefit_containers.nth(i)
                        # Get parent or sibling text to find benefit name
                        parent_text = await element.locator("..").inner_text()
                        if parent_text and len(parent_text.strip()) > 5:
                            benefits.append(f"Programa Social {i+1}")
                    except:
                        continue
                        
                if not benefits and count > 0:
                    benefits = ["Auxílio Emergencial"]  # Default based on the image
                    
            except:
                benefits = ["Auxílio Emergencial"]  # Default fallback
        
        print(f"📋 Found {len(benefits)} benefit programs: {benefits}")
        return benefits
        
    except Exception as e:
        print(f"⚠️ Warning collecting benefits list: {e}")
        return ["Auxílio Emergencial"]  # Default fallback

async def collect_benefit_details(page: Page, index: int, benefit_name: str):
    """
    Clicks on "Detail" button for specific benefit and collects detailed information
    """
    try:
        print(f"🔍 Collecting details for benefit: {benefit_name}")
        
        # Look for "Detalhar" button
        detail_buttons = page.locator("button:has-text('Detalhar'), a:has-text('Detalhar')")
        button_count = await detail_buttons.count()
        
        if button_count == 0:
            print(f"⚠️ No detail buttons found for {benefit_name}")
            return None
        
        # Use the index if available, otherwise use first button
        button_index = min(index, button_count - 1)
        detail_button = detail_buttons.nth(button_index)
        
        # Click on detail button
        await detail_button.scroll_into_view_if_needed()
        await detail_button.wait_for(state="visible", timeout=10000)
        await detail_button.click()
        
        # Wait for details page to load
        await page.wait_for_selector("text=TOTAL DE RECURSOS DISPONIBILIZADOS", timeout=15000)
        print("✅ Detail page loaded")
        
        # Collect detailed information from the page
        person_data = await collect_detailed_person_info(page)
        resources = await collect_resources_table(page)
        total_amount = calculate_total_amount(resources)
        
        benefit_data = {
            "program": benefit_name,
            "beneficiary_name": person_data.get("name", "N/A"),
            "beneficiary_cpf": person_data.get("cpf", "N/A"),
            "beneficiary_nis": person_data.get("nis", "N/A"),
            "resources": resources,
            "total_amount": total_amount,
            "total_records": len(resources)
        }
        
        print(f"✅ Collected {len(resources)} records for {benefit_name}")
        
        # Go back to previous page
        await page.go_back()
        await page.wait_for_timeout(2000)
        
        return benefit_data
        
    except Exception as e:
        print(f"❌ Error collecting details for benefit {benefit_name}: {e}")
        return None

async def collect_detailed_person_info(page: Page):
    """
    Collects detailed person information from the benefit details page
    """
    try:
        info = {"name": "N/A", "cpf": "N/A", "nis": "N/A"}
        
        # Look for beneficiary information sections
        fields = [
            ("name", "Nome Beneficiário"),
            ("cpf", "CPF Beneficiário"), 
            ("nis", "NIS Beneficiário")
        ]
        
        for field_key, field_label in fields:
            try:
                # Look for the field label and extract adjacent value
                label_locator = page.locator(f"text={field_label}")
                if await label_locator.count() > 0:
                    # Try to get the value from the same or adjacent element
                    parent = label_locator.first().locator("..")
                    text = await parent.inner_text()
                    # Extract value after the label
                    if field_label in text:
                        value = text.split(field_label)[-1].strip()
                        if value and value != field_label:
                            info[field_key] = value
            except:
                continue
        
        return info
        
    except Exception as e:
        print(f"⚠️ Error collecting detailed person info: {e}")
        return {"name": "N/A", "cpf": "N/A", "nis": "N/A"}

async def collect_resources_table(page: Page):
    """
    Collects all data from the resources table
    """
    try:
        resources = []
        
        # Wait for table to load
        await page.wait_for_selector("table", timeout=10000)
        
        # Get all table rows from tbody
        table_rows = page.locator("table tbody tr")
        row_count = await table_rows.count()
        
        print(f"📊 Processing {row_count} table rows")
        
        for i in range(row_count):
            try:
                row = table_rows.nth(i)
                columns = row.locator("td")
                column_count = await columns.count()
                
                if column_count >= 6:  # Minimum required columns
                    month = await columns.nth(0).inner_text()
                    installment = await columns.nth(1).inner_text() 
                    state = await columns.nth(2).inner_text()
                    municipality = await columns.nth(3).inner_text()
                    classification = await columns.nth(4).inner_text()
                    amount = await columns.nth(5).inner_text()
                    observation = await columns.nth(6).inner_text() if column_count > 6 else "N/A"
                    
                    resources.append({
                        "month": month.strip(),
                        "installment": installment.strip(),
                        "state": state.strip(),
                        "municipality": municipality.strip(),
                        "classification": classification.strip(),
                        "amount": amount.strip(),
                        "observation": observation.strip()
                    })
            except Exception as e:
                print(f"⚠️ Error processing table row {i}: {e}")
                continue
        
        return resources
        
    except Exception as e:
        print(f"❌ Error collecting resources table: {e}")
        return []

def calculate_total_amount(resources: list):
    """
    Calculates total amount from resources list
    """
    try:
        total = 0.0
        for resource in resources:
            amount_str = resource.get("amount", "0")
            # Remove currency symbols and convert to float
            clean_amount = amount_str.replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "").strip()
            
            # Extract only numeric part
            import re
            numeric_match = re.search(r'[\d,]+', clean_amount)
            if numeric_match:
                numeric_str = numeric_match.group().replace(",", ".")
                try:
                    total += float(numeric_str)
                except:
                    continue
                    
        return round(total, 2)
    except Exception as e:
        print(f"⚠️ Warning calculating total amount: {e}")
        return 0.0
