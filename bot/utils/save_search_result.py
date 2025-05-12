from datetime import datetime
from bot.utils.image_to_base64 import image_to_base64
from models.outputs import SearchOutput

async def save_search_result(page, cpf=None, name=None, social_filter=False) -> SearchOutput:
    try:
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"result_{timestamp}.png"
        
        
        await page.screenshot(path=file_name)
        print(f"Search completed. Screenshot saved as {file_name}")

        image_to_base64 = image_to_base64(file_name)

        return SearchOutput( 
            status= "sucsses",
            file = file_name,
            image_base64= image_to_base64,
            query = {
                "cpf": cpf,
                "nome": name,
                "filtro_social": social_filter
            }
        )

    except Exception as e:
        print(f"Error saving search results: {e}")
        return SearchOutput( 
            status = "error",
            file= None,
            image_base64= None,
            query = {
                "cpf": cpf,
                "nome": name,
                "filtro_social": social_filter
            }
        )
