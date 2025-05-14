import requests
import random
import time
import uuid
import os
from pathlib import Path
from typing import Optional
from apscheduler.schedulers.background import BackgroundScheduler
from prompt_generator import generate_prompt
from config.settings import settings

# Mapping of objects to their dataset IDs
OBJECT_TO_DATASET = {
    # 📦 Датасет 1 — "Тропическая атака" (59263)
    'Cannabis': 59263,
    'Cactus': 59263,
    'Pineapple': 59263,
    
    # 🍔 Датасет 2 — "Фастфуд рай" (61315) 61611
    'Burger': 61611,
    'PizzaSlice': 61611,
    'IceCreamCone': 61611,
    
    # ✈️ Датасет 3 — "Механика и мускулы" (59934)
    'Airplane': 59934,
    'Muscle': 59934,
    'CoffeeMug': 59934,
    
    # 🥐 Датасет 4 — "Мягкий сюр" (60509)
    'Banana': 60509,
    'Croissant': 60509,
    'SushiRoll': 60509,
    
    # 🍩 Датасет 5 — "Сочные кругляши" (61318)
    'Watermelon': 61318,
    'Coconut': 61318,
    'Donut': 61318
}

def generate_unique_filename(extension=".png"):
    """Генерация уникального имени файла"""
    return f"{uuid.uuid4()}{extension}"

def save_image(content: bytes) -> str:
    """Сохранение картинки на сервере"""
    filename = generate_unique_filename()
    filepath = settings.STATIC_FOLDER / filename
    with open(filepath, "wb") as f:
        f.write(content)
    return str(filepath)

def generate_public_url(filepath: str) -> str:
    """Генерация публичной ссылки на изображение"""
    filename = Path(filepath).name
    return f"/generated/{filename}"

def cleanup_old_files():
    """Очистка старых файлов"""
    now = time.time()
    for file in settings.STATIC_FOLDER.glob("*"):
        if file.is_file():
            file_age = now - file.stat().st_mtime
            if file_age > settings.MAX_FILE_AGE_SECONDS:
                try:
                    file.unlink()
                    print(f"Deleted old file: {file.name}")
                except Exception as e:
                    print(f"Error deleting {file.name}: {e}")

# Старт планировщика очистки
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_files, 'interval', minutes=1)
scheduler.start()

class LeonardoService:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {settings.LEONARDO_API_KEY}"
        }

    def generate_image(self, animal: str, object: str) -> Optional[str]:
        try:
            # Generate prompt using our prompt generator
            prompt = generate_prompt(animal, object)
            weight = random.choice([0.9, 1.0])
            if not prompt:
                raise ValueError(f"Failed to generate prompt for {animal} and {object}")
                
            print(f"Generated prompt: {prompt}")

            # Get the appropriate userLoraId for the object
            userLoraId = OBJECT_TO_DATASET.get(object)
            if not userLoraId:
                raise ValueError(f"No dataset found for object: {object}")

            # Step 1: Create a generation
            generation_url = f"{settings.LEONARDO_API_URL}/generations"
            generation_payload = {
                "userElements": [
                    {
                        "userLoraId": userLoraId,
                        "weight": weight
                    }
                ],
                "height": settings.IMAGE_HEIGHT,
                "modelId": settings.MODEL_ID,
                "prompt": prompt,
                "width": settings.IMAGE_WIDTH,
                "num_images": 1,
            }

            print("Sending request to Leonardo AI with payload:", generation_payload)
            
            generation_response = requests.post(
                generation_url,
                json=generation_payload,
                headers=self.headers
            )
            
            print("Response status:", generation_response.status_code)
            print("Response content:", generation_response.text)
            
            if generation_response.status_code != 200:
                error_msg = f"Leonardo API returned status {generation_response.status_code}: {generation_response.text}"
                print(f"Error: {error_msg}")
                raise Exception(error_msg)
            
            response_data = generation_response.json()
            if "sdGenerationJob" not in response_data:
                error_msg = "Invalid response format from Leonardo API"
                print(f"Error: {error_msg}")
                raise Exception(error_msg)
            
            generation_id = response_data["sdGenerationJob"]["generationId"]
            print(f"Generation ID: {generation_id}")

            # Step 2: Wait for generation to complete
            max_attempts = 12  # 1 minute maximum wait time
            attempt = 0
            
            while attempt < max_attempts:
                time.sleep(5)  # Wait 5 seconds between checks
                status_url = f"{settings.LEONARDO_API_URL}/generations/{generation_id}"
                status_response = requests.get(status_url, headers=self.headers)
                
                if status_response.status_code != 200:
                    error_msg = f"Failed to check generation status: {status_response.text}"
                    print(f"Error: {error_msg}")
                    raise Exception(error_msg)
                
                status_data = status_response.json()
                if "generations_by_pk" not in status_data:
                    error_msg = "Invalid status response format"
                    print(f"Error: {error_msg}")
                    raise Exception(error_msg)
                
                generation_data = status_data["generations_by_pk"]
                status = generation_data["status"]
                
                print(f"Generation status: {status}")

                if status == "COMPLETE":
                    if not generation_data.get("generated_images"):
                        error_msg = "No images in completed generation"
                        print(f"Error: {error_msg}")
                        raise Exception(error_msg)
                    
                    # Get the image URL from Leonardo
                    image_url = generation_data["generated_images"][0]["url"]
                    print(f"Generated image URL from Leonardo: {image_url}")
                    
                    # Download the image with proper headers
                    image_response = requests.get(
                        image_url,
                        headers={
                            "accept": "image/png",
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                        }
                    )
                    if image_response.status_code != 200:
                        raise Exception(f"Failed to download image from Leonardo: {image_response.status_code}")
                    
                    # Save the image locally
                    saved_path = save_image(image_response.content)
                    public_url = generate_public_url(saved_path)
                    print(f"Saved image locally at: {saved_path}")
                    print(f"Public URL: {public_url}")
                    
                    # Return the full URL including the server address
                    full_url = f"{settings.SERVER_URL}{public_url}"
                    print(f"Returning full URL: {full_url}")
                    return full_url
                    
                elif status == "FAILED":
                    error_message = generation_data.get("error_message", "Unknown error")
                    error_msg = f"Image generation failed: {error_message}"
                    print(f"Error: {error_msg}")
                    raise Exception(error_msg)
                elif status == "PENDING":
                    print("Generation pending, waiting...")
                    attempt += 1
                    continue
                else:
                    error_msg = f"Unexpected generation status: {status}"
                    print(f"Error: {error_msg}")
                    raise Exception(error_msg)

            error_msg = "Generation timed out after 1 minute"
            print(f"Error: {error_msg}")
            raise Exception(error_msg)

        except Exception as e:
            print(f"Error generating image with Leonardo AI: {str(e)}")
            return None 