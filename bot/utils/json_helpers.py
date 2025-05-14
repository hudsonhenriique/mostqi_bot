import json

def save_json_output(data: dict, file_base: str):
    try:
        file_name = f"{file_base}.json"
        with open(file_name, "w", encoding="utf-8") as json_file:
            # Salva o JSON formatado com indentação
            json.dump(data, json_file, indent=2, ensure_ascii=False)
        print(f"JSON output saved to {file_name}")
    except Exception as e:
        print(f"Error saving JSON output: {e}")