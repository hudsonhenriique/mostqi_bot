from datetime import datetime
def generate_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"result_{timestamp}.png"