import random
from datetime import datetime
import sys
import os
from pathlib import Path
import re

# Добавляем путь к корневой директории fastapi
fastapi_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(fastapi_dir))

from model import Mixed, Base, Spice, Animal, User
from config.db import SessionLocal, engine

def slugify(text):
    # Транслитерация русских букв в латиницу
    translit = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    
    # Переводим в нижний регистр
    text = text.lower()
    
    # Транслитерация
    result = ''
    for char in text:
        result += translit.get(char, char)
    
    # Заменяем все не-буквенно-цифровые символы на дефис
    result = re.sub(r'[^a-z0-9]+', '-', result)
    
    # Убираем начальные и конечные дефисы
    result = result.strip('-')
    
    return result

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Создаем сессию
db = SessionLocal()

try:
    # Сначала создадим тестового пользователя, если его нет
    test_user = db.query(User).filter(User.username == "test_user").first()
    if not test_user:
        test_user = User(
            uid="test123",
            username="test_user",
            mail="test@example.com",
            wallet_address="EQCrXf6gCMDV1XwAdqkG1GjkGwJDMYF9jbHGvwE_ANn2BXMA",
            coins=1000.0
        )
        db.add(test_user)
        db.commit()

    # Создадим несколько специй, если их нет
    spices = db.query(Spice).all()
    if not spices:
        spice_names = ['банан', 'кокос', 'самолет', 'телефон', 'компьютер', 'книга', 'часы', 'очки', 'ключ', 'ручка']
        for spice_name in spice_names:
            spice = Spice(
                name=spice_name,
                image=f"https://example.com/spices/{spice_name}.jpg"
            )
            db.add(spice)
        db.commit()
        spices = db.query(Spice).all()

    # Создадим несколько животных, если их нет
    animals = db.query(Animal).all()
    if not animals:
        animal_names = ['крокодил', 'обезьяна', 'бобёр', 'слон', 'жираф', 'тигр', 'попугай', 'кошка', 'собака', 'хомяк']
        for animal_name in animal_names:
            animal = Animal(
                name=animal_name,
                slug_id=slugify(animal_name)
            )
            db.add(animal)
        db.commit()
        animals = db.query(Animal).all()

    # Генерация 10 случайных миксов
    for _ in range(10):
        # Случайный выбор специи и животного
        spice = random.choice(spices)
        animal = random.choice(animals)
        
        # Создание названия микса
        name = f"{spice.name.capitalize()} {animal.name.capitalize()}"
        
        # Случайное количество поинтов от 1 до 100
        points = random.randint(1, 100)
        
        # Создание нового микса
        mixed = Mixed(
            name=name,
            image=f"https://example.com/mixes/{spice.name}_{animal.name}.jpg",
            points=points,
            spice_id=spice.id,
            animal_slug_id=animal.slug_id,
            user_id=test_user.uid
        )
        
        db.add(mixed)
    
    # Сохранение изменений
    db.commit()
    print("Successfully generated 10 random mixed entries!")

except Exception as e:
    print(f"An error occurred: {e}")
    db.rollback()

finally:
    # Закрываем сессию
    db.close() 