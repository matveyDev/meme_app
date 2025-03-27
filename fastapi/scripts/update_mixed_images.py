import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from config.db import SessionLocal, engine
from model import Mixed

# Список URL случайных мемов (можно дополнить)
MEME_IMAGES = [
    "https://i.imgur.com/DJZD3zU.png",  # Funny cat meme
    "https://i.imgur.com/XZwWe1R.png",  # Doge meme
    "https://i.imgur.com/9K3D6Zp.png",  # Surprised Pikachu
    "https://i.imgur.com/LZwWe1R.png",  # Drake meme
    "https://i.imgur.com/KZwWe1R.png",  # Distracted boyfriend
    "https://i.imgur.com/MZwWe1R.png",  # Woman yelling at cat
    "https://i.imgur.com/NZwWe1R.png",  # This is fine dog
    "https://i.imgur.com/OZwWe1R.png",  # Expanding brain
    "https://i.imgur.com/PZwWe1R.png",  # Roll Safe
    "https://i.imgur.com/QZwWe1R.png",  # One does not simply
]

def update_mixed_images():
    db = SessionLocal()
    try:
        # Получаем все записи Mixed
        mixes = db.query(Mixed).all()
        
        for i, mix in enumerate(mixes):
            # Выбираем случайное изображение из списка по индексу
            image_url = MEME_IMAGES[i % len(MEME_IMAGES)]
            mix.image = image_url
            print(f"Updating mix {mix.name} with image {image_url}")
        
        # Сохраняем изменения
        db.commit()
        print(f"Successfully updated {len(mixes)} mixes with random images")
        
    except Exception as e:
        print(f"Error updating mixes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_mixed_images() 