import base64

def image_to_base64(image_path: str, limit: int = 100) -> str:
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        # Retorna apenas os primeiros `limit` caracteres da string Base64
        return encoded_string[:limit] + "..." if len(encoded_string) > limit else encoded_string
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {image_path} was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while converting the image to base64: {e}")