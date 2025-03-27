from sqlalchemy.types import TypeDecorator, String
import re


class EmailType(TypeDecorator):
    impl = String(255)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                raise ValueError("Invalid email format")
        return value


class SlugType(TypeDecorator):
    impl = String(255)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Convert to lowercase and replace spaces with hyphens
            value = value.lower().replace(' ', '-')
            # Remove any characters that aren't alphanumeric or hyphens
            value = re.sub(r'[^a-z0-9-]', '', value)
        return value


class TONWalletType(TypeDecorator):
    impl = String(255)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Временно отключаем валидацию для тестирования
            return value
        return value
